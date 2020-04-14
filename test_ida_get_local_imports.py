#coding:utf-8

import idaapi
import idautils

import json


def set_import_function_color(addr):
    if addr != idaapi.BADADDR:
        SetColor(addr,CIC_ITEM,0x00CD00)

def write_line_to_file(file_path, line_data):
    with open(file_path, 'w') as f:
        f.write(line_data)
        f.write('\n')


def get_specify_import_modules_info(local_module_list):

    module_info_list = list()


    number_of_import_modules = idaapi.get_import_module_qty()


    for i in xrange(0, number_of_import_modules):
        print(i)
        module_info = dict()
        module_name = idaapi.get_import_module_name(i)
        print(module_name)



        if module_name in local_module_list:

            print("local module: %s"  %(module_name))
            module_info["index"] = i
            module_info["name"] = module_name
            print(module_info)
            module_info_list.append(module_info)


    print(module_info_list)
    return module_info_list


def get_import_funcs(import_module_index):

    import_funcs_info = []

    def imports_callback(ea, name, ord):


        import_funcs_info.append(('0x%x' % (ea), name))

        set_import_function_color(ea)
        return True


    idaapi.enum_import_names(import_module_index, imports_callback)

    return import_funcs_info



# C:/test.exe --> test
def get_pre_basename(file_path):

    file_basename = os.path.basename(file_path)
    file_prename = os.path.splitext(file_basename)[0]

    return file_prename


def get_local_dll_path(root_dir):
    root_dir_abs = os.path.abspath(root_dir)
    if os.path.exists(root_dir_abs) == False:
        raise RuntimeError('The path(%s) does not exist!')

    dll_path_list = list()
    for root, dirs, files in os.walk(root_dir_abs):
        for file in files:
            if '.dll' == file[-4:] :
                dll_path_list.append(os.path.join(root, file).replace('\\','/'))

    return dll_path_list




def get_local_module_name_list(root_dir):

    dll_path_list =  get_local_dll_path(root_dir)

    module_name_list = list()
    for dll_path in dll_path_list:
        module_name = get_pre_basename(dll_path)
        module_name_list.append(module_name)


    return module_name_list



def dump_dict_to_file(file_path, dict_data):
    with open(file_path, 'w') as f:
        json.dump(dict_data, f)






def main():
    root_dir = idautils.GetIdbDir()

    local_module_name_list = get_local_module_name_list(root_dir)

    local_import_module_info_list = get_specify_import_modules_info(local_module_name_list)

    import_module_funcs = dict()
    for module_info in local_import_module_info_list:
        funcs = get_import_funcs(module_info["index"])
        import_module_funcs[module_info["name"]] = funcs


    dump_dict_to_file(os.path.join(root_dir, 'imports.json'), import_module_funcs)






if __name__ == '__main__':
    # TODO 根据参数，决定递归遍历的目录
    main()


