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
module: libvirt_storage_pool

short_description: Manages Libvirt Storage Pools

version_added: "2.4"

description:
    - "NA"

options:
    uri:
        description:
            - The libvirt connection uri
        required: true
    name:
        description:
            - The name of the Storage Pool
        required: true
    path:
        description:
            - The Path of the Storage Pool
        required: true
    state:
       description:
           - Whether storage pool should be created or removed.
       required: true


extends_documentation_fragment:
    - cloud

author:
    - Petros Petrou (@ppetrou)
'''

EXAMPLES = '''
# Add a Storage Pool
- name: Add a Storage Pool
  libvirt_storage_pool:
    uri: qemu:///system
    name: pool01
    path: /pools/pool01
    state: present

# Remove a Storage Pool
- name: Remove a Storage Pool
  libvirt_storage_pool:
    uri: qemu:///system
    name: pool01
    path: /pools/pool01
    state: absent

'''

RETURN = '''
message:
    description: Descriptive message of outcome
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.libvirt_storage_util import *

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        uri=dict(type='str', required=True),
        name=dict(type='str', required=True),
        path=dict(type='str', required=True),
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
    uri = module.params['uri']
    name =  module.params['name']
    path = module.params['path']
    state = module.params['state']

    try:
        # Initialize Libvirt Storage Util
        libvirt_storage_util = LibVirtStorageUtil(uri)

        # Check is requesting to create storage pool
        if state == "present":
            new_pool = Pool(name, path)
            libvirt_storage_util.create_pool(new_pool)
        elif state == "absent":
            # Remove Storage Pool
            libvirt_storage_util.delete_pool(name)

        result['message'] = "OK"
        # TODO Check if the state changed in the result object and report back
        result['changed'] = True

    except ExStoragePoolExists as ex_pool_exists:
        result['message'] = "Storage Pool Exists"
        result['changed'] = False
    except ExStoragePoolNotFound as ex_pool_not_found:
        result['message'] = "Storage Pool {0} Not Found".format(name)
        result['changed'] = False
    except Exception as ex:
        result['message'] = str(type(ex).__name__)
        module.fail_json(msg=str(ex), **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
