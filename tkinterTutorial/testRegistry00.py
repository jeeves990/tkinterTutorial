from winreg import *
import os
from tkinter import *

roots_hives = {
    "HKEY_CLASSES_ROOT": HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_USER": HKEY_CURRENT_USER,
    "HKEY_LOCAL_MACHINE": HKEY_LOCAL_MACHINE,
    "HKEY_USERS": HKEY_USERS,
    "HKEY_PERFORMANCE_DATA": HKEY_PERFORMANCE_DATA,
    "HKEY_CURRENT_CONFIG": HKEY_CURRENT_CONFIG,
    "HKEY_DYN_DATA": HKEY_DYN_DATA
}

class readReg():
    def __init__(self):
        for (hivename, hive) in roots_hives.items():
            print("hivename [{0}]: hive [{1}]".format(hivename, hive))
            aReg = ConnectRegistry(None, hive)
            self.recurse(aReg)
        pass

    def recurse(self, reg):
        
        return


readReg()

def parse_key(key):
    key = key.upper()
    parts = key.split('\\')
    root_hive_name = parts[0]
    root_hive = roots_hives.get(root_hive_name)
    partial_key = '\\'.join(parts[1:])

    if not root_hive:
        raise Exception('root hive "{}" was not found'.format(root_hive_name))

    return partial_key, root_hive


def get_sub_keys(key):
    partial_key, root_hive = parse_key(key)

    with ConnectRegistry(None, root_hive) as reg:
        with OpenKey(reg, partial_key) as key_object:
            sub_keys_count, values_count, last_modified = QueryInfoKey(key_object)
            try:
                for i in range(sub_keys_count):
                    sub_key_name = EnumKey(key_object, i)
                    yield sub_key_name
            except WindowsError:
                pass


def get_values(key, fields):
    partial_key, root_hive = parse_key(key)

    with ConnectRegistry(None, root_hive) as reg:
        with OpenKey(reg, partial_key) as key_object:
            data = {}
            for field in fields:
                try:
                    value, type = QueryValueEx(key_object, field)
                    data[field] = value
                except WindowsError:
                    pass

            return data


def get_value(key, field):
    values = get_values(key, [field])
    return values.get(field)


def join(path, *paths):
    path = path.strip('/\\')
    paths = map(lambda x: x.strip('/\\'), paths)
    paths = list(paths)
    result = os.path.join(path, *paths)
    result = result.replace('/', '\\')
    return result


class Keep00:
    def __init__(self):
        self.doit()
        """
        this successfully writes the "DisplayName" value (and a dummy, if not "DisplayName")
        for a given hive,
        BUT ONLY ON THE FIRST LEVEL
        """
        

    def doit(self):
        aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        (numsubkeys, numvalues, lastmod) = QueryInfoKey(aKey)
        print("# subkeys: {0}, # values: {1}".format(numsubkeys, numvalues))

        i = 0
        keyname = EnumKey(aKey, i)
        print(keyname)
        for i in range(0, numsubkeys -1):
            try:
        
                asubkey = OpenKey(aKey, keyname)
                try:
                    val = QueryValueEx(asubkey, "DisplayName")
                    print("\t{0}".format(str(val)))
                except:
                    print("-----{0}_____".format(keyname))
                i += 1
                keyname = EnumKey(aKey, i)
            except WindowsError:
                break


if __name__ == '__main__':
    #Keep00()
    pass