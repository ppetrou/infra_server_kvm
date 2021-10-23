#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: gfs_fs

short_description: Manages Filesystems of Cloud Images using guestfish Python API

version_added: "2.4"

description:
    - "NA"

options:
    image_paths:
        description:
            - The paths of the cloud images that contain the physical volumes
        required: true
    device:
        description:
            - The name of the device to create the filesystem
        required: true
    device_type:
        description:
            - The type of the device lvm or standard
        required: true
    fstype:
        description:
            - The filesystem type
        required: true
    use_image_mkfs_xfs:
        description:
            - Option to use the cloud image mkfs.xfs binary rather than the guestfish one. Helpful for XFS incompatibilities
        required: true
    force:
        description:
            - Force the creation of the filesystem regardless if the device is initialized
        required: false
    mountpoint:
        description:
            - The mountpoint to mount the filesystem
        required: true
    state:
       description:
           - Whether the filesystem should be created or removed.
       required: true


extends_documentation_fragment:
    - cloud

author:
    - Petros Petrou (@ppetrou)
'''

EXAMPLES = '''
# Create a filesystem in /dev/vda1
- name: Create a filesystem in /dev/vda1
  gfs_fs:
    image_paths:
      - /cloud_images/vda.qcow2
    device: vda1
    device_type: standard
    fstype: xfs
    force: false
    mountpoint: /mount01
    state: present

# Remove a filesystem in /dev/vda2
- name: Remove a filesystem in /dev/vda2
  gfs_fs:
    image_paths:
      - /cloud_images/vda.qcow2
    device: vda2
    state: absent

# Create a filesystem in /dev/vg_root/vg01
- name: Create a filesystem in /dev/vg_root/vg01
  gfs_fs:
    image_paths:
      - /cloud_images/vda.qcow2
      - /cloud_images/vdb.qcow2
    device: vg_root/vg01
    device_type: lvm
    fstype: xfs
    force: false
    mountpoint: /mount01
    state: present

# Create a filesystem in /dev/vg_root/vg01 overriding existing one.
- name: Create a filesystem in /dev/vg_root/vg01 overriding existing one.
  gfs_fs:
    image_paths:
      - /cloud_images/vda.qcow2
      - /cloud_images/vdb.qcow2
    device: vg_root/vg01
    device_type: lvm
    fstype: xfs
    force: true
    mountpoint: /mount01
    state: present
'''

RETURN = '''
device_name:
    description: Device Name
    type: str
    returned: always
message:
    description: Descriptive message of outcome
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.guestfish_lib import *

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        image_paths=dict(type='list', required=True),
        device=dict(type='str', required=True),
        device_type=dict(type='str', required=True, choices=['standard','lvm']),
        fstype=dict(type='str', required=False),
        use_image_mkfs_xfs=dict(type='bool', required=False, default=False),
        force=dict(type='bool', required=False, default=False),
        mountpoint=dict(type='str', required=True),
        state=dict(type='str', required=True, choices=['present', 'absent', 'resize'])
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # Get the Module Parameters
    image_paths =  module.params['image_paths']
    device = module.params['device']
    device_type = module.params['device_type']
    fstype = module.params['fstype']
    use_image_mkfs_xfs = module.params['use_image_mkfs_xfs']
    force = module.params['force']
    mountpoint = module.params['mountpoint']
    state = module.params['state']

    # Module Logic
    gfs_result = None

    try:
        # Initialize GuestFish Util
        gfs_util = GFSLibUtil(image_paths)

        # Check is requesting to create a filesystem
        if state == "present":
            gfs_result = gfs_util.create_fs(device, device_type, fstype, force, use_image_mkfs_xfs, mountpoint)
        elif state == "absent":
            # Remove Filesystem
            gfs_result = gfs_util.delete_fs(device, device_type)
        elif state == "resize":
            gfs_result = gfs_util.resize_fs(device, device_type, fstype, use_image_mkfs_xfs, mountpoint)

        result['message'] = str(gfs_result)
        # TODO Check if the state changed in the result object and report back
        result['changed'] = True

    except ExFilesystemExistsError as ex_fs_exists:
        module.fail_json(msg=str(ex_fs_exists), **result)
    except ExFilesystemDoesNotExistError as ex_fs_does_not_exists:
        result['changed'] = False
        result['message'] = str(ex_fs_does_not_exists)
    except ExDeviceDoesNotExistError as ex_dev_does_not_exist:
        module.fail_json(msg=str(ex_dev_does_not_exist), **result)
    except ExFilesystemCreateError as ex_fs_add:
        module.fail_json(msg=str(ex_fs_add), **result)
    except ExFilesystemDelError as ex_fs_remove:
        module.fail_json(msg=str(ex_fs_remove), **result)
    except ExFilesystemResizeError as ex_fs_resize:
        module.fail_json(msg=str(ex_fs_resize), **result)
    except Exception as ex:
        module.fail_json(msg=str(ex), **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
