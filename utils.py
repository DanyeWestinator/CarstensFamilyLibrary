import hashlib
from os.path import isfile, isdir
from os import listdir, path

import psutil

folder_count = 0


def get_files(root: str, recurseDepth = 0) -> set:
    """
    Lists all files contained within a path.
    Recursively traverses subdirectories
    :param root: The root directory to search from
    :return: returns a set of absolute path strings to files
    """
    # get all objects in this folder
    try:
        files = listdir(root)
    except PermissionError:
        return set()
    # if there are no files, return an empty set
    if len(files) == 0:
        return set()
    found = set()
    for obj in files:
        obj = root + "\\" + obj
        obj = obj.replace("\\\\", "\\")
        # if we recurse, and the object is a folder
        if recurseDepth >= 1 and isdir(obj):
            # print(obj, "was folder")
            global folder_count
            folder_count += 1
            found = found.union(get_files(obj, recurseDepth - 1))

            found.add(obj)
        if isdir(obj):
            obj += "\\"
            found.add(obj)
        if isfile(obj):
            found.add(obj)
            pass

    return found


def hash_file(path: str, buffer=40960) -> str:
    """
    Gets the md5 hash of a file by path
    Loads
    :param path: The absolute file path to hash
    :param buffer: The number of bytes in the buffer
    :return: returns the string of the md5 hash for the file
    """

    #Don't hash directories
    if isdir(path):
        return
    with open(path, "rb") as f:
        hash = hashlib.md5()
        for chunk in iter(lambda: f.read(buffer), b""):
            hash.update(chunk)
        return str(hash.hexdigest())


def _list_drives() -> [str]:
    """
    Lists all the drives
    uses psutil (must be imported)
    :return: Returns all drives attached to this computer
    """
    all = [f.device for f in psutil.disk_partitions()]
    drives = [d for d in all if path.exists(f"{d}\\CFL.txt")]
    return drives


def list_in_string(target, search):
    s = target.lower()
    for item in search:
        if item in s:
            return True

    return False
