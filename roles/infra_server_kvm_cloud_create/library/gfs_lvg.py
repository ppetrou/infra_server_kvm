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

short_description: Manages Volume Groups of Cloud Images using guestfish Python API

version_added: "2.4"

description:
    - "NA"

options:
    image_paths:
        description:
            - The paths of the cloud images that contain the physical volumes
        required: true
    pvs:
        description:
            - The physical volumes to be added
        required: true
    vg:
        description:
            - The name of the volume group
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
# Create a VG named vg00
- name: Create a VG named vg00
  gfs_lvg:
    image_paths:
      - /cloud_images/vda.qcow2
      - /cloud_images/vdb.qcow2
    pvs:
      - /dev/vda
      - /dev/vdb
    vg: vg00
    state: present

# Remove a VG named vg00
- name: Create a VG named vg00
  gfs_lvg:
    image_paths:
      - /cloud_images/vda.qcow2
      - /cloud_images/vdb.qcow2
    vg: vg00
    state: absent

# Create a VG named vg01
- name: Create a VG named vg01
  gfs_lvg:
    image_paths:
      - /cloud_images/vda.qcow2
    pvs:
      - /dev/vda
    vg: vg01
    state: present

'''

RETURN = '''
vg_name:
    description: Volume Group Name
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
        pvs=dict(type='list', required=False),
        vg=dict(type='str', required=True),
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
    pvs = module.params['pvs']
    vg = module.params['vg']
    state = module.params['state']

    # Module Logic
    gfs_result = None

    try:
        # Initialize GuestFish Util
        gfs_util = GFSLibUtil(image_paths)

        # Check is requesting to add a partition
        if state == "present":
            gfs_result = gfs_util.add_vg(vg, pvs)
        elif state == "absent":
            # Remove partition
            gfs_result = gfs_util.delete_vg(vg)

        result['message'] = str(gfs_result)
        # TODO Check if the state changed in the result object and report back
        result['changed'] = True

    except ExVolumeGroupExistsError as ex_vg_exists:
        result['changed'] = False
        result['message'] = str(ex_vg_exists)
    except ExVolumeGroupDoesNotExistError as ex_vg_does_not_exist:
        module.fail_json(msg=str(ex_vg_does_not_exist), **result)
    except ExVolumeGroupAddError as ex_vg_add:
        module.fail_json(msg=str(ex_vg_add), **result)
    except ExVolumeGroupDelError as ex_vg_remove:
        module.fail_json(msg=str(ex_vg_remove), **result)
    except Exception as ex:
        module.fail_json(msg=str(ex), **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
