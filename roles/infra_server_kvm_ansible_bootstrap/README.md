infra_server_kvm_ansible_bootstrap
=========

Bootstraps a KVM to be used with ansible

Requirements
------------

The following packages need to be installed in the Hypervisor

- qemu-kvm
- libvirt
- libguestfs-tools

Role Variables
--------------

DEFAULT VARS

```
# Ansible Username
vm_ansible_user: ansible

# Ansible Password
vm_ansible_password: ansible123

# Ansible KVM Name to bootstrap
vm_name: rhel7-coredns
```

ROLE VARS

```
DO NOT alter the values of the role variables unless you know what you are doing.
The only variables you need to update is vm_root_dir which is the folder that will store
the Virtual Machines and the vm_root_disk_filename which is the name of the boot disk of the KVM.

# Directories
vm_root_dir: /home/ppetrou/VirtualMachines
vm_keys_dir: "{{ vm_root_dir }}/keys"
vm_dir: "{{ vm_root_dir }}/{{ vm_name }}"

# VM Files
vm_root_disk_filename: "vda.qcow2"
vm_root_disk_filepath: "{{ vm_dir }}/{{ vm_root_disk_filename }}"
```

Dependencies
------------

NA

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```
  ---
  - hosts: hypervisor
    become: yes
    roles:
      - role: infra_server_kvm_ansible_bootstrap
        vars:
          vm_ansible_user: ansible
          vm_ansible_password: ansible123
          vm_name: rhel7-coredns
```


License
-------

BSD

Author Information
------------------

```
Petros Petrou
ppetrou@gmail.com
```
