#!/usr/bin/env python3

import ansible_runner
import time

# KVM Templates
centos8xs = {"vm_desc": "Centos 8 (XS)",
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
             "vm_default_partition": { "device": "vda", "part_num": 1, "fstype": "xfs", "size": 24, "unit": "GiB" },
             "vm_partitions": [],
             "vm_volume_groups": [],
             "vm_logical_volumes": [],
             "vm_filesystems": [] }

centos8s = { "vm_desc": "Centos 8 (S)",
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
             "vm_default_partition": { "device": "vda", "part_num": 1, "fstype": "xfs", "size": 24, "unit": "GiB" },
             "vm_partitions": [],
             "vm_volume_groups": [],
             "vm_logical_volumes": [],
             "vm_filesystems": [] }

centos8m = { "vm_desc": "Centos 8 (M)",
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
             "vm_default_partition": { "device": "vda", "part_num": 1, "fstype": "xfs", "size": 24, "unit": "GiB" },
             "vm_partitions": [],
             "vm_volume_groups": [],
             "vm_logical_volumes": [],
             "vm_filesystems": [] }

centos8l = { "vm_desc": "Centos 8 (L)",
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
             "vm_default_partition": { "device": "vda", "part_num": 1, "fstype": "xfs", "size": 48, "unit": "GiB" },
             "vm_partitions": [],
             "vm_volume_groups": [],
             "vm_logical_volumes": [],
             "vm_filesystems": [] }

centos8xl = { "vm_desc": "Centos 8 (XL)",
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
              "vm_default_partition": { "device": "vda", "part_num": 1, "fstype": "xfs", "size": 48, "unit": "GiB" },
              "vm_partitions": [],
              "vm_volume_groups": [],
              "vm_logical_volumes": [],
              "vm_filesystems": [] }           

vm_templates = [centos8xs, centos8s, centos8m, centos8l, centos8xl]

# Base Vars
play_book = "create-vm-cloud.yml"

# Render TUI
print("Infra Server KVM")
print("================")
print("")
vm_index = 1
for vm_template in vm_templates:
    menu_item = "{0}. {1}\t{2}".format(vm_index, vm_template["vm_desc"].ljust(15), vm_template["vm_spec"])
    print(menu_item)
    vm_index = vm_index + 1
print("0. Exit")

wrong_input = True

while (wrong_input):
    try:
        config_selection = int(input("Select KVM Configuration: "))
        if (config_selection > len(vm_templates)):
            raise Exception("Invalid Input")
        wrong_input = False
    except:
        print("Invalid Input. Only numbers 1 to {0} is allowed.".format(len(vm_templates)))

if config_selection == 0:
    print("Bye :)")
    exit()
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

# Get the start time
start_time = time.time()

# private_data_dir is the Runner Input Directory Hierarchy
# Call infra_server_kvm_cloud role using ansible runner
r = ansible_runner.run(private_data_dir=".", playbook=play_book, extravars=extra_vars)

# Get the end time
end_time = time.time()

#Calculate duration
provisioning_duration = end_time - start_time

# Print outcome
print("Status: {0}".format(r.status))
print("Return Code: {0}".format(r.rc))
print("Provisiong Time: {0}(s)".format(int(provisioning_duration)))
