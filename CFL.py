import utils
from CFL_drive import CFL_drive
from sys import argv

cfl_instance = None


class CFL:
    _hashedPaths = {}
    """
    filepath : hash
    """

    _drives = []
    _drive_blacklist = []
    """
    All drives that this CFL instance is scanning / tracking
    """

    def __init__(self):
        """
        Boot loop for the main CFL program.
        Takes full index of all attached files.
        Goal is to verify file integrity.
        \nWe can NEVER lose a file
        """

        #Does Python do singletons? Lmao Dane in 2/19/2023 really liked Unity
        global cfl_instance
        if cfl_instance is None:
            cfl_instance = self

        #handling command line arguments
        if len(argv) >= 1:
            self._handle_args()

        # Gets all attached drives
        self._drives = utils._list_drives()

        for d in self._drives:
            print(f"Indexing drive {d}")
            drive = CFL_drive(d)



    def __del__(self):
        global cfl_instance
        cfl_instance = None

    def _hash_library(self):
        pass

    def _display_help(self):
        line = "Help menu for the Carstens Family Library!"
        print(f"\n\n{'-' * len(line)}\n{line}")
        print("--(kudos for using the command line btw)--\n\n")
        print("Run CFL.py without arguments to automatically run a full index")
        print("-h / -help : Display help")

    def _handle_args(self):
        # Iterate through all args when called
        for arg in argv[1:]:
            # All command line arguments
            if arg.startswith("-"):
                # help
                if utils.list_in_string(arg, ["h", "help"]):
                    self._display_help()
                if utils.list_in_string(arg, ["d", "dup", "duplicate"]):
                    print("Displaying dups")


if __name__ == "__main__":
    x = CFL()
