#!/usr/bin/env python3

import ansible_runner
import time

# KVM Templates
centos8xs = {"vm_desc": "Centos 8 Stream (XS)",
             "vm_spec": "1 vCPU, 4GB RAM, 32GB Disk, 1 Management NIC DHCP",
             "vm_name": "centos8-xsmall-lab1",
             "vm_hostname": "centos8-xsmall-lab1.lab.local",
             "vm_osinfo_id": "http://centos.org/centos-stream/8",
             "vm_cloud_image": "CentOS-Stream-GenericCloud-8-20210603.0.x86_64.qcow2",
             "vm_mem": 4096,
             "vm_mem_current": 2048,
             "vm_cpu": 1,
             "vm_disks": [{ "device": "vda", "size": "32G", "bootable": True }],
             "vm_mac_prefix": "bc:ae:80",
             "vm_interfaces": [],
             "vm_default_partition": { "device": "vda", "part_num": 1, "fstype": "xfs", "size": 31, "unit": "GiB" },
             "vm_partitions": [],
             "vm_volume_groups": [],
             "vm_logical_volumes": [],
             "vm_default_filesystem": { "device": "vda1", "mountpoint": "/", "fstype": "xfs", "type": "standard" },
             "vm_filesystems": [] }

centos8s = { "vm_desc": "Centos 8 Stream (S)",
             "vm_spec": "2 vCPU, 4GB RAM, 32GB Disk, 1 Management NIC DHCP",
             "vm_name": "centos8-small-lab1",
             "vm_hostname": "centos8-small-lab1.lab.local",
             "vm_osinfo_id": "http://centos.org/centos-stream/8",
             "vm_cloud_image": "CentOS-Stream-GenericCloud-8-20210603.0.x86_64.qcow2",
             "vm_mem": 4096,
             "vm_mem_current": 2048,
             "vm_cpu": 2,
             "vm_disks": [{ "device": "vda", "size": "32G", "bootable": True }],
             "vm_mac_prefix": "bc:ae:80",
             "vm_interfaces": [],
             "vm_default_partition": { "device": "vda", "part_num": 1, "fstype": "xfs", "size": 31, "unit": "GiB" },
             "vm_partitions": [],
             "vm_volume_groups": [],
             "vm_logical_volumes": [],
             "vm_default_filesystem": { "device": "vda1", "mountpoint": "/", "fstype": "xfs", "type": "standard" },
             "vm_filesystems": [] }

centos8m = { "vm_desc": "Centos 8 Stream (M)",
             "vm_spec": "4 vCPU, 8GB RAM, 32GB Disk, 1 Management NIC DHCP",
             "vm_name": "centos8-medium-lab1",
             "vm_hostname": "centos8-medium-lab1.lab.local",
             "vm_osinfo_id": "http://centos.org/centos-stream/8",
             "vm_cloud_image": "CentOS-Stream-GenericCloud-8-20210603.0.x86_64.qcow2",
             "vm_mem": 8192,
             "vm_mem_current": 4096,
             "vm_cpu": 4,
             "vm_disks": [{ "device": "vda", "size": "32G", "bootable": True }],
             "vm_mac_prefix": "bc:ae:80",
             "vm_interfaces": [],
             "vm_default_partition": { "device": "vda", "part_num": 1, "fstype": "xfs", "size": 31, "unit": "GiB" },
             "vm_partitions": [],
             "vm_volume_groups": [],
             "vm_logical_volumes": [],
             "vm_default_filesystem": { "device": "vda1", "mountpoint": "/", "fstype": "xfs", "type": "standard" },
             "vm_filesystems": [] }

centos8l = { "vm_desc": "Centos 8 Stream (L)",
             "vm_spec": "4 vCPU, 16GB RAM, 64GB Disk, 1 Management NIC DHCP",
             "vm_name": "centos8-large-lab1",
             "vm_hostname": "centos8-large-lab1.lab.local",
             "vm_osinfo_id": "http://centos.org/centos-stream/8",
             "vm_cloud_image": "CentOS-Stream-GenericCloud-8-20210603.0.x86_64.qcow2",
             "vm_mem": 16384,
             "vm_mem_current": 8192,
             "vm_cpu": 4,
             "vm_disks": [{ "device": "vda", "size": "64G", "bootable": True }],
             "vm_mac_prefix": "bc:ae:80",
             "vm_interfaces": [],
             "vm_default_partition": { "device": "vda", "part_num": 1, "fstype": "xfs", "size": 63, "unit": "GiB" },
             "vm_partitions": [],
             "vm_volume_groups": [],
             "vm_logical_volumes": [],
             "vm_default_filesystem": { "device": "vda1", "mountpoint": "/", "fstype": "xfs", "type": "standard" },
             "vm_filesystems": [] }

centos8xl = { "vm_desc": "Centos 8 Stream (XL)",
              "vm_spec": "4 vCPU, 32GB RAM, 64GB Disk, 1 Management NIC DHCP",
              "vm_name": "centos8-xlarge-lab1",
              "vm_hostname": "centos8-xlarge-lab1.lab.local",
              "vm_osinfo_id": "http://centos.org/centos-stream/8",
              "vm_cloud_image": "CentOS-Stream-GenericCloud-8-20210603.0.x86_64.qcow2",
              "vm_mem": 32768,
              "vm_mem_current": 16384,
              "vm_cpu": 4,
              "vm_disks": [{ "device": "vda", "size": "64G", "bootable": True }],
              "vm_mac_prefix": "bc:ae:80",
              "vm_interfaces": [],
              "vm_default_partition": { "device": "vda", "part_num": 1, "fstype": "xfs", "size": 63, "unit": "GiB" },
              "vm_partitions": [],
              "vm_volume_groups": [],
              "vm_logical_volumes": [],
              "vm_default_filesystem": { "device": "vda1", "mountpoint": "/", "fstype": "xfs", "type": "standard" },
              "vm_filesystems": [] }           

vm_templates = [centos8xs, centos8s, centos8m, centos8l, centos8xl]

# Base Vars
play_book = "create-vm-cloud.yml"

# Template Vars
kvm_queue = []

# Render TUI
start_provisioning = False

while (not start_provisioning):

    wrong_input = True
    wrong_task_input = True

    print("Infra Server KVM")
    print("================")
    print("1. Provision New KVM")
    print("2. View Provisioning Queue")
    print("3. Start Provisioning")
    print("0. Exit")

    while (wrong_task_input):
        try:
            task_selection = int(input("Select Task: "))
            if (task_selection > 3):
                raise Exception("Invalid Input")
            wrong_task_input = False
        except:
            print("Invalid Input. Only numbers 1 to 3 are allowed.")

    if task_selection == 0:
        print("Bye :)")
        exit()

    if task_selection == 1:
        print("")
        vm_index = 1
        for vm_template in vm_templates:
            menu_item = "{0}. {1}\t{2}".format(vm_index, vm_template["vm_desc"].ljust(15), vm_template["vm_spec"])
            print(menu_item)
            vm_index = vm_index + 1
        print("0. Back")

        wrong_kvm_input = True

        while (wrong_kvm_input):
            try:
                config_selection = int(input("Select KVM Configuration: "))
                if (config_selection > len(vm_templates)):
                    raise Exception("Invalid Input")
                wrong_kvm_input = False
            except:
                print("Invalid Input. Only numbers 1 to {0} are allowed.".format(len(vm_templates)))

        if config_selection == 0:
            pass
        else:
            extra_vars = vm_templates[config_selection - 1]

            vm_name = input("Enter KVM Name (Enter for {0}): ".format(extra_vars["vm_name"]))
            if (vm_name == ""):
                vm_name = extra_vars["vm_name"]

            vm_name_hyphened = vm_name.replace(" ","-")

            vm_hostname = input("Enter KVM Hostname (Enter for {0}.lab.local): ".format(vm_name_hyphened))
            if (vm_hostname == ""):
                vm_hostname = "{0}.lab.local".format(vm_name_hyphened)
            
            # Update KVM Configuration
            extra_vars.update({"vm_name": vm_name_hyphened, "vm_hostname": vm_hostname })
            kvm_queue.append(extra_vars)
    
    if task_selection == 2:
        print("")
        print("KVM Provisioning Queue")
        print("======================")
        if len(kvm_queue) == 0:
            print("Queue Empty!")

        kvm_queue_index = 1
        for kvm_conf in kvm_queue:
            print("{0}\t{1}\t{2}\t{3}".format(kvm_queue_index, kvm_conf["vm_name"],kvm_conf["vm_desc"], kvm_conf["vm_spec"]))
            kvm_queue_index = kvm_queue_index + 1
        print("")

    if task_selection == 3:
        prov_results = []
        start_provisioning = True
        
        # Get the start time
        start_time = time.time()

        # private_data_dir is the Runner Input Directory Hierarchy
        # Call infra_server_kvm_cloud role using ansible runner
        for kvm_conf in kvm_queue: 
            kvm_start_time = time.time()
            r = ansible_runner.run(private_data_dir=".", playbook=play_book, extravars=kvm_conf)
            kvm_end_time = time.time()
            kvm_provisioning_duration = kvm_end_time - kvm_start_time    
            prov_results.append({"kvm": kvm_conf["vm_name"], "status": r.status, "rc": r.rc, "provtime": kvm_provisioning_duration})

        # Get the end time
        end_time = time.time()

        #Calculate duration
        provisioning_duration = end_time - start_time

        # Print outcome
        print("{0}\t{1}\t{2}\t{3}".format("KVM".ljust(20),"STATUS".ljust(15),"RC".ljust(5),"PROVISIONING TIME"))
        for res in prov_results:
            print("{0}\t{1}\t{2}\t{3}(s)".format(res["kvm"].ljust(20), res["status"].ljust(15), str(res["rc"]).ljust(5), int(res["provtime"])))
        
        print("")
        print("Total Provisining Time: {0}(s)".format(int(provisioning_duration)))
        
 
