from ansible.errors import AnsibleError
from ansible.errors import AnsibleFilterError

def pvs_dict_to_imagepath_list(vm_dir, pvs_dict, format):
    image_path_list = []

    for p in pvs_dict:
        tmp_path = vm_dir + "/" + p['device'] + "." + format
        image_path_list.append(tmp_path)

    for image_path in image_path_list:
        if image_path_list.count(image_path) > 1:
            raise AnsibleFilterError("Duplicate Image Path Found. Please make sure there are no duplicate entries in vm_lvm_storage")

    return image_path_list

def pvs_dict_to_pvs_list(pvs_dict):
    pvs_list = []

    for p in pvs_dict:
        parts = p['parts']
        for part in parts:
          tmp_pvs = p['device'] + str(part)
          pvs_list.append(tmp_pvs)

    for pvs in pvs_list:
        if pvs_list.count(pvs) > 1:
            raise AnsibleFilterError("Duplicate PVS Found. Please make sure there are no duplicate entries in vm_lvm_storage")

    return pvs_list

class FilterModule(object):
    '''
    custom jinja2 filters for working with collections
    '''

    def filters(self):
        return {
            'pvs_dict_to_imagepath_list': pvs_dict_to_imagepath_list,
            'pvs_dict_to_pvs_list': pvs_dict_to_pvs_list
        }
