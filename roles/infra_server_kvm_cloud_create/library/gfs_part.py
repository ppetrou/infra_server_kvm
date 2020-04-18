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
module: gfs_part

short_description: Manages partition tables of Cloud Images using guestfish Python API

version_added: "2.4"

description:
    - "NA"

options:
    image_path:
        description:
            - The path of the cloud image that contains the device
        required: true
    device:
        description:
            - The device to manage partitions
        required: true
    number:
        description:
            - The number of the partition
        required: true
    size:
       description:
           - The size of the partition
       required: true
    unit:
       description:
           - The storage unit of the partition
       required: true
    resize:
       description:
           - Resize the partition if exists
       required: true
    state:
       description:
           - Whether partition should be created or removed.
       required: true


extends_documentation_fragment:
    - cloud

author:
    - Petros Petrou (@ppetrou)
'''

EXAMPLES = '''
# Add a 10G partition
- name: Add a 10G partition
  gfs_part:
    device: /dev/vda
    number: 2
    size: 10
    unit: GiB
    state: present

# Resize the existing partition 3 to 5GiB
- name: Resize the existing partition 3 to 5GiB
  gfs_part:
    device: /dev/vda
    number: 3
    size: 5
    unit: GiB
    resize: true
    state: present

# Remove partition number 2
- name: Remove partition number 2
  gfs_part:
    device: /dev/vda
    number: 2
    state: absent

'''

RETURN = '''
part_num:
    description: The partition number handled
    type: int
    returned: always
part_device:
    description: The partition device handled
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
        image_path=dict(type='str', required=True),
        device=dict(type='str', required=True),
        number=dict(type='int', required=True),
        size=dict(type='int', required=False, default=0),
        unit=dict(type='str', required=False, default='Byte', choices=['Byte', 'KiB', 'MiB', 'GiB']),
        resize=dict(type='bool', required=False, default=False),
        state=dict(type='str', required=True, choices=['present', 'absent'])
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
    image_path =  module.params['image_path']
    device = module.params['device']
    number = module.params['number']
    size = module.params['size']
    unit = module.params['unit']
    resize = module.params['resize']
    state = module.params['state']

    # Module Logic
    gfs_result = None

    try:
        # Initialize GuestFish Util
        gfs_util = GFSLibUtil([image_path])

        # Check is requesting to add a partition
        if state == "present":
            if resize == True:
                # Resize partition
                gfs_result = gfs_util.resize_partition(device, number, size, unit)
            else:
                # Add a partition
                try:
                    gfs_result = gfs_util.add_partition(device, size, unit)
                except ExUnrecognizedDiskLabelError as ex_disk_label_error:
                    # Intialize Partition Table
                    gfs_util.initialize_partition_table(device, "mbr")
                    # Re-try to Add Partition
                    gfs_result = gfs_util.add_partition(device, size, unit)
        elif state == "absent":
            # Remove partition
            gfs_result = gfs_util.delete_partition(device, number)

        result['message'] = str(gfs_result)
        # TODO Check if the state changed in the result object and report back
        result['changed'] = True

    except ExPartitionAddError as ex_part_add:
        module.fail_json(msg=str(ex_part_add), **result)
    except ExPartitionDelError as ex_part_del:
        module.fail_json(msg=str(ex_part_del), **result)
    except ExPartitionResizeError as ex_part_resize:
        module.fail_json(msg=str(ex_part_resize), **result)
    except ExPartitionDoesNotExistError as ex_part_not_exists:
        module.fail_json(msg=str(ex_part_not_exists), **result)
    except Exception as ex:
        module.fail_json(msg=str(ex), **result)

    result['message'] = str(result)
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
