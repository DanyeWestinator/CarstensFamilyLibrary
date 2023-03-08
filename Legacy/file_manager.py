import hashlib
from os.path import isfile, isdir
from os import listdir

folder_count = 0




def get_files(root: str, recursive=True) -> set:
    """
    Lists all files contained within a path.
    Recursively traverses subdirectories
    :param root: The root directory to search from
    :return: returns a set of absolute path strings to files
    """
    # get all objects in this folder
    files = listdir(root)
    # if there are no files, return an empty set
    if len(files) == 0:
        return set()
    found = set()
    for obj in files:
        obj = root + "\\" + obj
        # if we recurse, and the object is a folder
        if recursive and isdir(obj):
            # print(obj, "was folder")
            global folder_count
            folder_count += 1
            found = found.union(get_files(obj))

        if isfile(obj):
            found.add(obj)
            print(f"{obj} hashed to {hash_file(obj)}")
            pass
            # print(obj)
        # print(obj)
    print(f"Found {len(files)} files")

    return found


def hash_file(path: str, buffer = 4096) -> str:
    """
    Gets the md5 hash of a file
    Loads
    :param path: The file path to hash
    :param buffer: The number of bytes in the buffer
    :return: returns the string of the md5 hash for the file
    """
    with open(path, "rb") as f:
        hash = hashlib.md5()
        for chunk in iter(lambda: f.read(buffer), b""):
            hash.update(chunk)
        return str(hash.hexdigest())

def serialize():
    """
    Writes the current file dict to memory
    :return: void
    """


class File:
    def __init__(self, path : str):
        self.hash = hash_file(path)

    pass


class FileManager:
    # Key : hash
    # Value : set() of paths that contain that file, including filenames
    file_dict = {}

    def __init__(self):
        pass

if __name__ == "__main__":
    #found = get_files("D:\\Personal Documents\\Pictures\\Pictures", False)
    found = get_files("F:\\DCIM\\100CANON", False)
    print(f"Found {len(found)} files, and {folder_count} folders")
    print("9f6d132658eabc58f7f5a4dd375a5f34" == "9f6d132658eabc58f7f5a4dd375a5f34")