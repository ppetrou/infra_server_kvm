#!/usr/bin/env python3

from simpleline import App
from simpleline.render.screen import UIScreen
from simpleline.render.screen_handler import ScreenHandler
from simpleline.render.widgets import TextWidget, EntryWidget, CheckboxWidget
from simpleline.render.containers import ListRowContainer, ListColumnContainer, WindowContainer, Container
from simpleline.render.prompt import Prompt
from simpleline.render.adv_widgets import ErrorDialog
from simpleline.errors import SimplelineError
from simpleline.input.input_handler import InputHandler
from simpleline.render.screen import InputState
from simpleline.render.adv_widgets import GetInputScreen, YesNoDialog

from datetime import datetime

import yaml
import os
import copy

import ansible_runner
import time

class ConfigParser():
    
    def __init__(self):
        super().__init__()
    
    def parse_configs(self, config_path):

        kvm_configs = []

        for config in os.listdir(config_path):
            if config.endswith(".yml"):
                with open(config_path + "/" + config, "r") as stream:
                    yaml_config = yaml.safe_load(stream)
                    # Append Extra Keys
                    yaml_config.update({"ex_vm_completed": False})
                    kvm_configs.append(yaml_config)
        
        return kvm_configs 

class KVMHolder():
    kvms = []

    @staticmethod
    def add_kvm(kvm):
        KVMHolder.kvms.append(kvm)
    
    @staticmethod
    def remove_kvm(kvm):
        KVMHolder.kvms.remove(kvm)

# UI Screens
class KVMConfigurationViewEditList(UIScreen):

    def __init__(self):
        super().__init__(title=u"KVM Configuration View/Edit")
           
    def refresh(self, args=None):
        super().refresh()

        self.kvm_num_range = range(1, len(args) + 1)
        self.key_list = []
        for k in self.kvm_num_range:
            self.key_list.append(str(k))

        kvm_column = ListColumnContainer(columns=1, numbering=True)
        
        # Menu Items
        for kvm in args:
            vm_desc = kvm["vm_desc"]
            vm_spec = kvm["vm_spec"]           
            vm_name = kvm["vm_name"]
            vm_hostname = kvm["vm_hostname"]

            kvm_text = "{0} - {1} | VM Name: {2}\tVM Hostname: {3}".format(vm_desc, vm_spec, vm_name, vm_hostname)

            tmp_widget = TextWidget(kvm_text)
            kvm_column.add(tmp_widget)

        self.window.add(kvm_column)
    
    def prompt(self, args=None):
        prompt = super().prompt()

        # Add Help Option
        prompt.add_help_option("Help")
        return prompt
        
    def input(self, args, key):

        if key in self.key_list:
            # Get selected KVM from the KVM List
            selected_kvm_config = args[int(key)-1]

            delete_config = YesNoDialog("Do you want to delete the KVM Config?")
            ScreenHandler.push_screen_modal(delete_config)
            delete_reply = delete_config.answer

            skip_edit = False

            if delete_reply:
                KVMHolder.remove_kvm(selected_kvm_config)
                skip_edit = True

            if not skip_edit:
                customize_config = YesNoDialog("Do you want to update the KVM Config?")
                ScreenHandler.push_screen_modal(customize_config)
                edit_reply = customize_config.answer

                if edit_reply:
                    kvm_custom_config = KVMCustomConfiguration()
                    ScreenHandler.push_screen_modal(kvm_custom_config, args=selected_kvm_config)
            
            return InputState.PROCESSED_AND_REDRAW
                
        return key

# UI Screens
class KVMConfigurationList(UIScreen):

    def __init__(self):
        super().__init__(title=u"Available KVM Configurations")
           
    def refresh(self, args=None):
        super().refresh()

        self.kvm_num_range = range(1, len(args) + 1)
        self.key_list = []
        for k in self.kvm_num_range:
            self.key_list.append(str(k))

        kvm_column = ListColumnContainer(columns=1, numbering=True)
        
        # Menu Items
        for kvm in args:
            vm_desc = kvm["vm_desc"]
            vm_spec = kvm["vm_spec"]           
            vm_name = kvm["vm_name"]
            vm_hostname = kvm["vm_hostname"]
            vm_completed = kvm["ex_vm_completed"]

            kvm_text = "{0} - {1}".format(vm_desc, vm_spec)

            tmp_widget = TextWidget(kvm_text)
            kvm_column.add(tmp_widget)

        self.window.add(kvm_column)
    
    def prompt(self, args=None):
        prompt = super().prompt()

        # Add Help Option
        prompt.add_help_option("Help")
        return prompt
        
    def input(self, args, key):

        if key in self.key_list:
            # Get selected KVM from the KVM List
            selected_kvm_config = copy.deepcopy(args[int(key)-1])

            customize_config = YesNoDialog("Do you want to update the KVM Config?")
            ScreenHandler.push_screen_modal(customize_config)
            edit_reply = customize_config.answer           

            if edit_reply:
                kvm_custom_config = KVMCustomConfiguration()
                ScreenHandler.push_screen_modal(kvm_custom_config, args=selected_kvm_config)
            
            KVMHolder.add_kvm(selected_kvm_config)

            return InputState.PROCESSED_AND_REDRAW
                
        return key
       
class KVMCustomConfiguration(UIScreen):
    def __init__(self):
        super().__init__(title=u"KVM Custom Configuration")
    
    def refresh(self, args=None):
        super().refresh()

        main_columns = ListColumnContainer(columns=1, numbering=True)

        add_kvm_widget = EntryWidget(title="KVM Name", value=args["vm_name"])
        remove_kvm_widget = EntryWidget(title="KVM Hostname", value=args["vm_hostname"])

        main_columns.add(add_kvm_widget)
        main_columns.add(remove_kvm_widget)

        self.window.add(main_columns)
    
    def input(self, args, key):

        if key == "1":
            kvm_name_input = GetInputScreen("Enter KVM Name")
            ScreenHandler.push_screen_modal(kvm_name_input)
            kvm_name_value = kvm_name_input.value
            args.update({"vm_name": kvm_name_value})
            return InputState.PROCESSED_AND_REDRAW
        
        if key == "2":
            kvm_hostname_input = GetInputScreen("Enter KVM Hostname")
            ScreenHandler.push_screen_modal(kvm_hostname_input)
            kvm_hostname_value = kvm_hostname_input.value
            args.update({"vm_hostname": kvm_hostname_value})
            return InputState.PROCESSED_AND_REDRAW
            
        return key

class MainMenu(UIScreen):

    def __init__(self):
        super().__init__(title=u"Main Menu")
    
    def refresh(self, args=None):
        super().refresh()

        menu_column = ListColumnContainer(columns=1)

        # Menu Items
        config_kvm_widget = TextWidget("Add KVM")
        network_kvm_widget = TextWidget("View/Edit KVM")

        menu_column.add(config_kvm_widget)
        menu_column.add(network_kvm_widget)
       
        self.window.add(menu_column)
    
    def prompt(self, args=None):
        prompt = super().prompt()

        # Remove continue option
        prompt.remove_option('c')

        # Add Help Option
        prompt.add_help_option("Help")

        # Add start provisioning option
        prompt.add_option("p", "to provision")
        return prompt
        
    def input(self, args, key):
        if key == "1":
            kvm_conf_list = KVMConfigurationList()
            ScreenHandler.push_screen(kvm_conf_list, args=args) 
            return InputState.PROCESSED
        
        if key == "2":
            kvm_conf_edit = KVMConfigurationViewEditList()
            ScreenHandler.push_screen(kvm_conf_edit, args=KVMHolder.kvms) 
            return InputState.PROCESSED
        
        if key == "p":
            play_book_cloud_create = "create-vm-cloud.yml"
            play_book_ansible_bootstrap = "bootstrap-ansible.yml"
            play_book_snapshot = "create-snapshot.yml"

            date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            generated_inventory = "/tmp/hosts_{0}".format(date_time)
            
            prov_results = []
            ansible_bootstrap_results = []
            snapshot_results = []
            start_provisioning = True
        
            # Get the start time
            start_time = time.time()

            for kvm_conf in KVMHolder.kvms: 
                kvm_start_time = time.time()
                r = ansible_runner.run(private_data_dir=".", playbook=play_book_cloud_create, extravars=kvm_conf)
                kvm_end_time = time.time()
                kvm_provisioning_duration = kvm_end_time - kvm_start_time   
                prov_results.append({"kvm": kvm_conf["vm_name"], "status": r.status, "rc": r.rc, "provtime": kvm_provisioning_duration})
            
            for kvm_conf in KVMHolder.kvms:
                ansible_bootstrap_start_time = time.time()
                r = ansible_runner.run(private_data_dir=".", playbook=play_book_ansible_bootstrap, extravars={ "vm_name": kvm_conf["vm_name"], "generated_inventory_path": generated_inventory})
                ansible_bootstrap_kvm_end_time = time.time()
                kvm_boostrap_duration = ansible_bootstrap_kvm_end_time - ansible_bootstrap_start_time   
                ansible_bootstrap_results.append({"kvm": kvm_conf["vm_name"], "status": r.status, "rc": r.rc, "bootstrap_time": kvm_boostrap_duration})
            
            for kvm_conf in KVMHolder.kvms:
                snaphost_start_time = time.time()
                r = ansible_runner.run(private_data_dir=".", playbook=play_book_snapshot, extravars={ "domain_name": kvm_conf["vm_name"]})
                snapshot_end_time = time.time()
                snapshost_duration = snapshot_end_time - snaphost_start_time   
                snapshot_results.append({"kvm": kvm_conf["vm_name"], "status": r.status, "rc": r.rc, "snapshot_time": snapshost_duration})

            # Get the end time
            end_time = time.time()

            #Calculate duration
            provisioning_duration = end_time - start_time

            # Print outcome
            print("{0}\t{1}\t{2}\t{3}".format("KVM".ljust(20),"STATUS".ljust(15),"RC".ljust(5),"PROVISIONING TIME"))
            for res in prov_results:
                print("{0}\t{1}\t{2}\t{3}(s)".format(res["kvm"].ljust(20), res["status"].ljust(15), str(res["rc"]).ljust(5), int(res["provtime"])))
            
            print("\n")

            print("{0}\t{1}\t{2}\t{3}".format("KVM".ljust(20),"STATUS".ljust(15),"RC".ljust(5),"ANSIBLE BOOTSTRAP TIME"))
            for res in ansible_bootstrap_results:
                print("{0}\t{1}\t{2}\t{3}(s)".format(res["kvm"].ljust(20), res["status"].ljust(15), str(res["rc"]).ljust(5), int(res["bootstrap_time"])))

            print("\n")

            print("{0}\t{1}\t{2}\t{3}".format("KVM".ljust(20),"STATUS".ljust(15),"RC".ljust(5),"SNAPSHOT TIME"))
            for res in snapshot_results:
                print("{0}\t{1}\t{2}\t{3}(s)".format(res["kvm"].ljust(20), res["status"].ljust(15), str(res["rc"]).ljust(5), int(res["snapshot_time"])))

            print("")
            print("Total Provisining Time: {0}(s)".format(int(provisioning_duration)))
            print("You can find an auto-generated ansible inventory in {0}".format(generated_inventory))
            print("A snapshot named 'init' has been auto-created for each KVM. You can use this to revert the KVMs to the original provisioned state at any time :)")

            return InputState.PROCESSED_AND_CLOSE 
            
        return key


if __name__ == "__main__":

    # Read the KVM Configuration
    c_parser = ConfigParser()
    kvms = c_parser.parse_configs("./tui/configs")

    # Initialize application (create scheduler and event loop).
    App.initialize()

    # Create our screen.
    screen = MainMenu()

    # Schedule screen to the screen scheduler.
    # This can be called only after App.initialize().
    ScreenHandler.schedule_screen(screen, args=kvms)

    # Run the application. You must have some screen scheduled
    # otherwise it will end in an infinite loop.
    App.run()


