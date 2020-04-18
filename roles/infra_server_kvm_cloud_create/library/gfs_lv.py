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
module: gfs_lvg

short_description: Manages Logical Volumes of Cloud Images using guestfish Python API

version_added: "2.4"

description:
    - "NA"

options:
    image_paths:
        description:
            - The paths of the cloud images that contain the physical volumes
        required: true
    lv:
        description:
            - The name of the logical volume
        required: true
    vg:
        description:
            - The name of the volume group
        required: true
    size:
        description:
            - The size of the volume group
        required: true
    state:
       description:
           - Whether the volume group should be created or removed.
       required: true


extends_documentation_fragment:
    - cloud

author:
    - Petros Petrou (@ppetrou)
'''

EXAMPLES = '''
# Create a Logical Volume named lv00
- name: Create a Logical Volume named lv00
  gfs_lv:
    image_paths:
      - /cloud_images/vda.qcow2
      - /cloud_images/vdb.qcow2
    lv: vol00
    vg: vg00
    size: 2048
    state: present

# Remove a Logical Volume named lv00
- name: Remove a Logical Volume named lv00
  gfs_lv:
    image_paths:
      - /cloud_images/vda.qcow2
      - /cloud_images/vdb.qcow2
    vg: lv00
    state: absent

# Create a Logical Volume named lv01
- name: Create a Logical Volume named lv01
  gfs_lvg:
    image_paths:
      - /cloud_images/vda.qcow2
    lv: vol00
    vg: vg00
    size: 2048
    state: present

'''

RETURN = '''
lvol_name:
    description: Logical Volume Name
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
        lv=dict(type='str', required=True),
        vg=dict(type='str', required=True),
        size=dict(type='int', required=False),
        unit=dict(type='str', required=False, default='MiB', choices=['Byte', 'KiB', 'MiB', 'GiB']),
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
    image_paths =  module.params['image_paths']
    lv = module.params['lv']
    vg = module.params['vg']
    size = module.params['size']
    unit = module.params['unit']
    state = module.params['state']

    # Module Logic
    gfs_result = None

    try:
        # Initialize GuestFish Util
        gfs_util = GFSLibUtil(image_paths)

        # Check is requesting to add a partition
        if state == "present":
            gfs_result = gfs_util.add_lv(lv, vg, size, unit)
        elif state == "absent":
            # Remove partition
            gfs_result = gfs_util.delete_lv(lv, vg)

        result['message'] = str(gfs_result)
        # TODO Check if the state changed in the result object and report back
        result['changed'] = True

    except ExLogicalVolumeExistsError as ex_lv_exists:
        module.fail_json(msg=str(ex_lv_exists), **result)
    except ExLogicalVolumeDoesNotExistError as ex_lv_does_not_exist:
        module.fail_json(msg=str(ex_lv_does_not_exist), **result)
    except ExLogicalVolumeAddError as ex_lv_add:
        module.fail_json(msg=str(ex_lv_add), **result)
    except ExLogicalVolumeDelError as ex_lv_remove:
        module.fail_json(msg=str(ex_lv_remove), **result)
    except Exception as ex:
        module.fail_json(msg=str(ex), **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
