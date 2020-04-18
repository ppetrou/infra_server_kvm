infra_server_kvm_fcos_create
=========

Provisions Fedora CoreOS using the QEMU Provided Image

Requirements
------------

Required Packages in Hypervisor:
- qemu-kvm
- libvirt
- virt-install


Role Variables
--------------

DEFAULT VARS

```
# VM Name. It is the name in the hypervisor.
vm_name: coreos-dev-01

# OS Info Id. It must match the Cloud OS. Run "osinfo-query os" for the correct value. You need to use the 'ID' NOT 'Short ID'.
vm_osinfo_id: http://fedoraproject.org/fedora/31

# Cloud Image File Name
vm_coreos_image: fedora-coreos-31.20200113.3.1-qemu.x86_64.qcow2

# Max RAM in MiB. Not other Unit is supported at the moment.
vm_mem: 4096

# Current RAM in MiB. Not other Unit is supported at the moment.
vm_mem_current: 4096

# Number of CPUs
vm_cpu: 4

# Virtual Disks. Size is set in Gigabytes G. No other Unit is supported at the moment.
# At least on disk MUST be set as bootable otherwise the system will fail to boot.
vm_disks: [
  { device: "vda", file: "vda.qcow2", format: "qcow2", size: "10", bootable: true, swap: false },
  { device: "vdb", file: "vdb.qcow2", format: "qcow2", size: "2", bootable: false, swap: true }
]

# Virtual NICs. ONLY bridged interfaces are supported.
vm_interfaces: [
  { ifname: "eth0", bridge: "br0", mac: "96:01:b7:9d:03:8a", bootproto: dhcp, ip_addr: None, gateway: None, dns_servers: [] },
  { ifname: "eth1", bridge: "br0", mac: "7e:9c:81:27:12:b6", bootproto: dhcp, ip_addr: None, gateway: None, dns_servers: [] }
]
```

ROLE VARS

DO NOT alter the values of the role variables unless you know what you are doing.
The only variable you need to update is vm_root_dir which is the folder that will store
the Virtual Machines.

```
# Cloud Image Location
vm_coreos_cloud_image_location: /home/ppetrou/IMG/qcow2
vm_coreos_cloud_image_path: "{{ vm_coreos_cloud_image_location }}/{{ vm_coreos_image }}"

# VM Directories
vm_root_dir: /home/ppetrou/VirtualMachines
vm_dir: "{{ vm_root_dir }}/{{ vm_name }}"
vm_disk_file: "{{ vm_dir }}/{{ vm_disks[0].file }}"
vm_keys_dir: "{{ vm_root_dir }}/keys"

# Ignition
vm_ignition_file: config.ign
vm_ignition_filepath: "{{ vm_dir }}/{{ vm_ignition_file }}"

# Virt Install
vm_virt_install_sh_filepath: "{{ vm_dir }}/virt-install.sh"
```


Dependencies
------------

NA


Example Playbook
----------------

```
  ---
  - hosts: hypervisor
    become: yes
    roles:
      - role: infra_server_kvm_fcos_create
        vars:
          vm_name: coreos-dev-01
          vm_osinfo_id: http://fedoraproject.org/fedora/31
          vm_coreos_image: fedora-coreos-31.20200113.3.1-qemu.x86_64.qcow2
          vm_mem: 4096
          vm_mem_current: 4096
          vm_cpu: 4
          vm_disks: [
            { device: "vda", file: "vda.qcow2", format: "qcow2", size: "10240", bootable: true, swap: false },
            { device: "vdb", file: "vdb.qcow2", format: "qcow2", size: "2048", bootable: false, swap: true }
          ]
          vm_interfaces: [
            { ifname: "eth0", bridge: "br0", mac: "96:01:b7:9d:03:8a", bootproto: dhcp, ip_addr: None, gateway: None, dns_servers: [] },
            { ifname: "eth1", bridge: "br0", mac: "7e:9c:81:27:12:b6", bootproto: dhcp, ip_addr: None, gateway: None, dns_servers: [] }
          ]
```

License
-------

LGPL

Author Information
------------------

```
Petros Petrou
ppetrou@gmail.com
```
