Role Name
=========

Installs a KVM using Kickstart and a DVD iso using virt-install

Requirements
------------

The following packages need to be installed in the Hypervisor

- qemu-kvm
- libvirt
- virt-install
- libguestfs-tools


Role Variables
--------------

```
# VM Name. It is the name in the hypervisor.
vm_name: rhel7-dev-01

# OS Info Id. It must match the Cloud OS. Run "osinfo-query os" for the correct value. You need to use the 'ID' NOT 'Short ID'.
vm_osinfo_id: http://redhat.com/rhel/7.6

# OS ISO File Name
vm_iso_image: rhel-server-7.6-x86_64-dvd.iso

# Max RAM in MiB. Not other Unit is supported at the moment.
vm_mem: 4096

# Current RAM in MiB. Not other Unit is supported at the moment.
vm_mem_current: 4096

# Number of CPUs
vm_cpu: 4

# Virtual Disks. Size is set in MiBs. No other Unit is supported at the moment.
# At least on disk MUST be set as bootable otherwise the system will fail to boot.
vm_disks:
  - { device: "vda", format: "qcow2", size: 20480, bootable: true, swap: false }
  - { device: "vdb", format: "qcow2", size: 4096,  bootable: false, swap: true}

# Virtual NICs. ONLY bridged interfaces are supported.
# Leave the mac attribute empty if you need to auto-generate the MAC address based on the
# vm_mac_prefix variable.  
vm_mac_prefix: "bc:ae:80"
vm_interfaces:
  - { ifname: "eth0", bridge: "bridge0", mac: "96:01:b7:9d:03:8a", bootproto: dhcp, ip_addr: None, gateway: None, dns_servers: None }
  - { ifname: "eth1", bridge: "bridge0", mac: "7e:9c:81:27:12:b6", bootproto: dhcp, ip_addr: None, gateway: None, dns_servers: None }

# Virtual Disk Partitions.
# DO NOT leave this variable empty as kickstart will fail to setup the partitions.
vm_partitions:
  - { mount: "/home", fstype: "xfs",  size: 5120,  name: "home", vgname: "vg_vda" }
  - { mount: "/var",  fstype: "xfs",  size: 2048,  name: "var",  vgname: "vg_vda" }
  - { mount: "/",     fstype: "xfs",  size: 10240, name: "root", vgname: "vg_vda" }
  # Swap partitions can only live in a logical volume which takes the whole of a volume group. Needs to be fixed!!
  # Do not set a size it will take the whole of the volume group. Let it as -1.
  - { mount: "swap",  fstype: "swap", size: -1,  name: "swap", vgname: "vg_vdb" }

# OS packages
# The packages to be installed during installation. It is the list in the packages sections of kickstart.
vm_os_packages: [ net-tools, gfs2-utils]
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
      - role: infra_server_kvm_ks_create
        vars:
          vm_name: rhel7-dev-01
          vm_osinfo_id: http://redhat.com/rhel/7.6
          vm_iso_image: rhel-server-7.6-x86_64-dvd.iso
          vm_mem: 4096
          vm_mem_current: 4096
          vm_cpu: 4
          vm_disks: [
            { device: "vda", format: "qcow2", size: 20480, bootable: true, swap: false },
            { device: "vdb", format: "qcow2", size: 4096,  bootable: false, swap: true}
          ]
          vm_mac_prefix: "bc:ae:80"
          vm_interfaces: [
            { ifname: "eth0", bridge: "bridge0", mac: "96:01:b7:9d:03:8a", bootproto: dhcp, ip_addr: None, gateway: None, dns_servers: None },
            { ifname: "eth1", bridge: "bridge0", mac: "7e:9c:81:27:12:b6", bootproto: dhcp, ip_addr: None, gateway: None, dns_servers: None }
          ]
          vm_partitions: [
            { mount: "/home", fstype: "xfs",  size: 5120,  name: "home", vgname: "vg_vda" },
            { mount: "/var",  fstype: "xfs",  size: 2048,  name: "var",  vgname: "vg_vda" },
            { mount: "/",     fstype: "xfs",  size: 10240, name: "root", vgname: "vg_vda" },
            { mount: "swap",  fstype: "swap", size: -1,  name: "swap", vgname: "vg_vdb" }
          ]
          vm_os_packages: [ net-tools, gfs2-utils ]
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
