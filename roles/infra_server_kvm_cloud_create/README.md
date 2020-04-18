infra_server_kvm_cloud_create
=========

Provisions a KVM using a vendor provided Cloud Image and libguestfs for home lab use ONLY.
This role is NOT designed for provisioning PRODUCTION VMs. Its components though (e.g. GuestFish Modules) can be considered Production ready and adapted / reused in Production.

NOTES

* Only the root user with password 'root' will be created.
Any other user needs to be added manually.
* An SSH private/public key for the root user will also be generated and injected to image. It will be stored in the value of vm_keys_dir variable.


!WARNING!

The role does NOT validate whether the variable values are correct.
Please make sure you are passing a valid VM Configuration otherwise the role might
fail or provision an unusuable VM.

e.g.

```

The following is an invalid configuration. Although we have defined two virtual Disks vda and vdb
we are trying to partition a device named vdc which does not exist!!

# At least on disk MUST be set as bootable otherwise the system will fail to boot.
vm_disks: [
  { device: "vda", size: 40G, bootable: true },
  { device: "vdb", size: 30G, bootable: false }
]

vm_partitions: [
  { device: "vda", part_num: 2, size: 2,  unit: GiB },
  { device: "vda", part_num: 3, size: 5,  unit: GiB },
  { device: "vdc", part_num: 1, size: 5,  unit: GiB },
  { device: "vdc", part_num: 2, size: 10, unit: GiB }
]
```

PENDING TASKS

* Test for min ansible version required. It has been developed / tested in 2.8 but should work fine in earlier versions.


Requirements
------------

Required Packages in Hypervisor:
- qemu-kvm
- libvirt
- virt-install
- libguestfs-tools
- python3-libguestfs


Red Hat Subscription:
-  A valid Red Hat Developer Subscription is required if you are provisioning a KVM with LVM Storage.
lvm2 package needs to be added to the image so lvm is operational post install.
- You need to set valid credentials in the encrypted file vars/sm_cred.yml. The default vault password is 'cloud'.

Python Intepreter:
- Python 3

Supported Hypervisors:

- KVM

Supported Cloud Images:

| Cloud Image	| Supported | Tested 	|
|---	|---	|---	|
|[RHEL 7](https://access.redhat.com/downloads/content/69/ver=/rhel---7/7.7/x86_64/product-software) | yes | yes	|   	
| RHEL 8  	 | no | no, but should work |
| Centos 7   | no | no, but should work |
| Centos 8   | no | no, but should work |
| Fedora 30+ | no | no, but should work |


Role Variables
--------------

DEFAULT VARS

```
# VM Name. It is the name in the hypervisor.
vm_name: rhel7-dev-lab

# Hostname
vm_hostname: rhel7-dev-lab.lab.local

# OS Info Id. It must match the Cloud OS. Run "osinfo-query os" for the correct value. You need to use the 'ID' NOT 'Short ID'.
vm_osinfo_id: http://redhat.com/rhel/7.7

# Cloud Image File Name
vm_cloud_image: rhel-server-7.7-update-1-x86_64-kvm.qcow2

# Max RAM in MiB. Not other Unit is supported at the moment.
vm_mem: 4096

# Current RAM in MiB. Not other Unit is supported at the moment.
vm_mem_current: 4096

# Number of CPUs
vm_cpu: 4

# Virtual Disks. Size is set in Gigabytes G. No other Unit is supported at the moment.
# At least on disk MUST be set as bootable otherwise the system will fail to boot.
vm_disks: [
  { device: "vda", size: 40G, bootable: true },
  { device: "vdb", size: 30G, bootable: false }
]

# The MAC address prefix to be used in mac address auto-generation if we do not provide one manually.
vm_mac_prefix: "bc:ae:80"

# Virtual NICs. ONLY bridged interfaces are supported.
# Leave the mac attribute empty if you need to auto-generate the MAC address based on the
# vm_mac_prefix variable.
vm_interfaces: [
  { ifname: "eth0", bridge: "br0", mac: "bc:ae:80:9b:b9:e8", bootproto: static, ip_addr: 192.168.100.200, netmask: None, gateway: 192.168.100.1, dns_servers: [] }
]

# The default partition of the Cloud Image.
# It is usually 7.8GiB by default and needs to get resized to something larger.
# YOU CANNOT SET THIS VALUE TO LESS THAN 7.8GiB as it cannot shrink.
vm_default_partition: { device: "vda", part_num: 1, size: 10, unit: GiB }

# Virtual Disk Partitions.
# DO NOT RE-SET THE DEFAULT PARTITION HERE. It has been set in vm_default_partition above.
# Leave this variable as an empty list if you do not need any partitions.
vm_partitions: [
  { device: "vda", part_num: 2, size: 2,  unit: GiB },
  { device: "vda", part_num: 3, size: 5,  unit: GiB },
  { device: "vdb", part_num: 1, size: 5,  unit: GiB },
  { device: "vdb", part_num: 2, size: 10, unit: GiB }
]

# Volume Groups
# Make sure you set the correct parts per device. Parts are the partition number found
# in vm_parititions
# Leave this variable as an empty list if you do not need any volume groups.
vm_volume_groups: [
  { vg: vg_root, pvs: [ { device: "vda", parts: [2] }, { device: "vdb", parts: [1, 2] } ] }
]

# Logical Volumes
# Make sure the vg attribute is an existing Volume Group in the vm_volume_groups variable
# Leave this variable as an empty list if you do not need any logical volumes.
vm_logical_volumes: [
  { lv: lv1, vg: vg_root, size: 2, unit: GiB },
  { lv: lv2, vg: vg_root, size: 4, unit: GiB }
]

# Filesystems
# Make sure you use the correct device name. /dev/ is not required and will be handled by
# the roles internally.
# For standard partitions you need the named of the device plus the partition number e.g. vdb2.
# For LVM Storage you need the path of the logical volume without /dev e.g. /vg_name/lv_name
# For Swap filesystems mark the fstype as "swap".
# type can be "standard" or "lvm"
# Leave this variable as an empty list if you do not need any filesystems.
vm_filesystems: [
  { device: "vda3",        mountpoint: "swap", fstype: "swap", type: "standard" },
  { device: "vg_root/lv1", mountpoint: "/lv1", fstype: "xfs",  type: "lvm" },
  { device: "vg_root/lv2", mountpoint: "/lv2", fstype: "xfs",  type: "lvm" }
]

```

ROLE VARS

DO NOT alter the values of the role variables unless you know what you are doing.
The only variable you need to update is vm_root_dir which is the folder that will store
the Virtual Machines.


```
# Cloud Image Location
cloud_image_loc: /home/ppetrou/IMG/qcow2
cloud_image_path: "{{ cloud_image_loc }}/{{ vm_cloud_image }}"

# Cloud Image default partition
cloud_image_default_partition : /dev/sda1
cloud_image_default_disk: /dev/sda
cloud_image_default_device_prefix: /dev/sd

# VM Directories
vm_root_dir: /home/ppetrou/VirtualMachines
vm_keys_dir: "{{ vm_root_dir }}/keys"
vm_dir: "{{ vm_root_dir }}/{{ vm_name }}"

# VM Files
vm_tmp_disk: "{{ vm_dir }}/tmp.qcow2"

# Disk Format
vm_disk_format: qcow2

```

ENCRYPTED VARS

```
vars/sm_cred.yml

# RHN Username
sm_username: user@domain.com
# RHN Password
sm_password: password

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
      - role: infra_server_kvm_cloud_create
        vars:
          vm_name: rhel7-dev-lab
          vm_hostname: rhel7-dev-lab.lab.local
          vm_osinfo_id: http://redhat.com/rhel/7.7
          vm_cloud_image: rhel-server-7.7-update-1-x86_64-kvm.qcow2
          vm_mem: 4096
          vm_mem_current: 4096
          vm_cpu: 4
          vm_disks: [
            { device: "vda", size: 40G, bootable: true },
            { device: "vdb", size: 30G, bootable: false }
          ]
          vm_mac_prefix: "bc:ae:80"
          vm_interfaces: [
            { ifname: "eth0", bridge: "br0", mac: "bc:ae:80:9b:b9:e8", bootproto: static, ip_addr: 192.168.100.200, netmask: None, gateway: 192.168.100.1, dns_servers: [] }
          ]
          default_partition: { device: "vda", part_num: 1, fstype: "xfs", size: 10, unit: GiB }
          vm_partitions: [
            { device: "vda", part_num: 2, fstype: "xfs", size: 2,  unit: GiB },
            { device: "vda", part_num: 3, fstype: "xfs", size: 5,  unit: GiB },
            { device: "vdb", part_num: 1, fstype: "xfs", size: 5,  unit: GiB },
            { device: "vdb", part_num: 2, fstype: "xfs", size: 10, unit: GiB }
          ]
          vm_volume_groups: [
            { vg: vg_root, pvs: [ { device: "vda", parts: [2] }, { device: "vdb", parts: [1, 2] } ] }
          ]
          vm_logical_volumes: [
            { lv: lv1, vg: vg_root, size: 2048, unit: MiB },
            { lv: lv2, vg: vg_root, size: 4096, unit: MiB }
          ]
          vm_filesystems: [
            { device: "vda3",        mountpoint: "swap", fstype: "swap", type: "standard" },
            { device: "vg_root/lv1", mountpoint: "/lv1", fstype: "xfs",  type: "lvm" },
            { device: "vg_root/lv2", mountpoint: "/lv2", fstype: "xfs",  type: "lvm" }
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
