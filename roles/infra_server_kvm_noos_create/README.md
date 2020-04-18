Role Name
=========

Provisions a KVM without installing an OS

Requirements
------------

The following packages need to be installed in the Hypervisor

- qemu-kvm
- libvirt


Role Variables
--------------

```
# VM Name
vm_name: rhel7-dev-01

# OS Info Id. It must match the Cloud OS. Run "osinfo-query os" for the correct value. You need to use the 'ID' NOT 'Short ID'.
vm_osinfo_id: http://redhat.com/rhel/7.6

# Max RAM in MiB. Not other Unit is supported at the moment.
vm_mem: 4096

# Current RAM in MiB. Not other Unit is supported at the moment.
vm_mem_current: 4096

# Number of CPUs
vm_cpu: 2

# Virtual Disks. Size is set in Gigabytes G. No other Unit is supported at the moment.
# At least on disk MUST be set as bootable otherwise the system will fail to boot.
vm_disks: [
  { device: "vda", file: "vda.qcow2", size: "10G", bootable: true },
  { device: "vdb", file: "vdb.qcow2", size: "2G", bootable: false}
]

# The MAC address prefix to be used in mac address auto-generation if we do not provide one manually.
vm_mac_prefix: "bc:ae:80"

# Virtual NICs. ONLY bridged interfaces are supported.
# Leave the mac attribute empty if you need to auto-generate the MAC address based on the
# vm_mac_prefix variable.
vm_interfaces: [
  { bridge: "br0", mac: "bc:ae:80:9b:b9:e8" }
]
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
      - role: infra_server_kvm_noos_create
        vars:
          vm_name: rhel7-dev-01
          vm_osinfo_id: http://redhat.com/rhel/7.6
          vm_mem: 4096
          vm_mem_current: 4096
          vm_cpu: 2
          vm_disks: [
            { device: "vda", file: "vda.qcow2", size: "10G", bootable: true },
            { device: "vdb", file: "vdb.qcow2", size: "2G", bootable: false}
          ]
          vm_mac_prefix: "bc:ae:80"
          vm_interfaces: [
            { bridge: "br0", mac: "bc:ae:80:9b:b9:e8" }
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
