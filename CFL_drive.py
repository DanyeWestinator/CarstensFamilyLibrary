import utils


class CFL_drive:
    _hashedPaths = {}
    """
    filepath : hash
    Only for this drive
    """
    _pathedHashes = {}
    """
    hash : filepath
    Inverse drive for constant time lookups
    """
    _properties = {}
    """
    The properties of this drive, saved on disk. Each line starts with <> and contains one property. 
    Each property is key : val
     Thankfully, python duck types things
    """
    _CFL_comments = []
    """
    All comments stored in this drive's CFL.txt
    """
    _root_paths = []
    """
    All root CFL folder structures on this drive
    """
    _lines = []
    """
    The lines of CFL.txt, in order
    """

    def __init__(self, letter):
        self._drive_letter = letter
        self._parse_cfl()
        self._index_files()

    def _index_files(self):
        """
        Indexes all files on a drive. Only indexes files below any "root" folder indicated by CFL.txt
        :return: Returns all filepaths (no directories), along with their MD5 hash value
        """
        print("Starting index...")
        j = 0
        found = 0
        for root in self._root_paths:
            files = utils.get_files(root, 5)
            for file in files:
                if file.endswith("\\"):
                    continue

                if j % 15 == 0:
                    print(f"{j} of {len(files)}!")
                hsh = utils.hash_file(file)
                if hsh is None:
                    continue
                if hsh in self._pathedHashes.keys():
                    found += 1
                    #print(f"Found {file} in hashes already!!!. Now found {found}")
                    self._add_file_hash(file, hsh)
                else:
                    self._add_file_hash(file, hsh)
                j += 1
            j = 0

        for item in self._hashedPaths.keys():
            print(f"File: {item} hashed to {self._hashedPaths[item]}")

    def _add_file_hash(self, file, hash):
        self._hashedPaths[file] = hash
        self._pathedHashes[hash] = file

    def _parse_cfl(self):
        """
        Parses the CFL.txt for the given drive.
        Contains all root folders for CFL-backed-up files
        Each <file> line is tab separated.
        \n<file> *path* *hash*
        :return:
        """

        # CFL.txt lives at the root of the drive
        cfl_path = f"{self._drive_letter}\\CFL.txt"

        with open(cfl_path) as f:
            for line in f:
                # clean each line, add it in order to the list of lines
                line = line.strip()
                line = line.replace("    ", "\t")
                self._lines.append(line)

                if r"#" in line:
                    line = line.replace("#", "")
                    self._CFL_comments.append(line)
                    continue
                if line.startswith("<var>"):
                    # The properties contained in this variable line
                    # Root drive, drive name, etc
                    props = line.replace("<var>", "").split(":")

                    props = [p.strip() for p in props]
                    key = props[0]
                    val = props[1]
                    self._properties[key] = val
                    if "root" in key:
                        path = f"{self._drive_letter}\\{val}"
                        path = path.replace("\\\\", "\\")
                        self._root_paths.append(path)
                        print(f"Added {self._root_paths[-1]}")
                    print(f"Set property '{key}' to '{val}' in drive {self._drive_letter}")
                # file lines
                if line.startswith("<file>"):
                    line = line.replace("<file>", "")
                    split = line.split("\t")
                    path = split[0].strip()
                    hash = split[1].strip()
                    self._pathedHashes[hash] = path
                    self._hashedPaths[path] = hash

                    print(f"FILE BASED {path} hashed to: {hash}")

    def _change_line(self, line, newline):
        """
        Changes the line of the CFL to the new line
        :param line: Changes the first line containing this substring
        :param newline: The entirety of the new line entry
        :return: void
        """
        i = 0
        for old in self._lines:
            if line.lower() in old.lower():
                break
            i += 1
        print(f"Changed line {i} '{self._lines[i]}' to {newline}")
        self._lines[i] = newline

    def _write_CFL(self):
        """
        Overwrites the contents of CFL.txt with the contents of self._lines
        """
        f = open(f"{self._drive_letter}\\CFL.txt", "w")
        s = ""
        for line in self._lines:
            s += line.strip() + "\n"
        f.write(s)
