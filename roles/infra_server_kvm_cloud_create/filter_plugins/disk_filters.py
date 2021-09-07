from ansible.errors import AnsibleError
from ansible.errors import AnsibleFilterError

def disk_list_to_imagepath_list(vm_root_dir, vm_name,  disk_list, format):
    image_path_list = []

    for d in disk_list:
        tmp_path = vm_root_dir + "/" + vm_name + '_' + d['device'] + "." + format
        image_path_list.append(tmp_path)

    return image_path_list

    return pvs_list

class FilterModule(object):
    '''
    custom jinja2 filters for working with collections
    '''

    def filters(self):
        return {
            'disk_list_to_imagepath_list': disk_list_to_imagepath_list
        }
