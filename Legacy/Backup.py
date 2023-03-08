# On run Backup.py,
# all drives to back up will have their files checked,
# then all files we don't currently store will be backed up
import os
import PIL.Image

from utils import get_files, hash_file
import hashlib
from os.path import isfile, isdir
from os import listdir
import shutil

CFL_PICTURE_ROOT = "D:\\CarstensFamilyLibrary\\pictures"
months = {
    1 : "January",
    2 : "February",
    3 : "March",
    4 : "April",
    5 : "May",
    6 : "June",
    7 : "July",
    8 : "August",
    9 : "September",
    10 : "October",
    11 : "November",
    12 : "December"
}
LIBRARY_FILES = {}

def _check_year_exists(year : int):
    #checks if the folder for a given year exists
    files = listdir(CFL_PICTURE_ROOT)
    # if there are no files, return False
    if len(files) == 0:
        return False
    for obj in files:
        obj = CFL_PICTURE_ROOT + "\\" + obj
        # if the object is a folder and the year is in the string
        if isdir(obj) and str(year) in obj:
            return True
    return False
def _check_month_exists(year : int, month : str):
    if _check_year_exists(year) == False:
        return False
    if type(month) == int:
        month = months[month]
    yearpath = f"{CFL_PICTURE_ROOT}\\{year}\\"
    files = listdir(yearpath)
    # if there are no files, return False
    if len(files) == 0:
        return False
    for obj in files:
        obj = yearpath + obj
        # if the object is a folder and the year is in the string
        if isdir(obj) and month in obj:
            return True
    return False
def _create_year(year):
    #creates the given year folder if it doesn't exist

    #if the year exists, do nothing
    if _check_year_exists(year):
        return
    os.mkdir(f"{CFL_PICTURE_ROOT}\\{year}")
def _create_month(year, month):
    if _check_month_exists(year, month) == True:
        return
    month_int = "00"
    if type(month) == int:
        month_int = ""
        if month < 10:
            month_int = "0"
        month_int += str(month)
        month = months[month]

    yearpath = f"{CFL_PICTURE_ROOT}\\{year}\\"
    _create_year(year)
    month_path = f"{yearpath}{month_int}_{month}"
    os.mkdir(month_path)

def _get_monthpath(year, month : int):
    yearpath = f"{CFL_PICTURE_ROOT}\\{year}\\"
    zed = ""
    if month < 10:
        zed = "0"
    month_path = f"{yearpath}{zed}{month}_{months[month]}\\"
    return month_path

def _get_name_from_exif(path):
    try:
        img = PIL.Image.open(path)
    except OSError:
        print(path, " threw OSERROR")
        img = None
    exif = img._getexif()
    date = str(exif[306])
    date = date.replace(" ", "_")
    filetype = path.split(".")[-1].lower()
    name = f"{date}.{filetype}"
    name = name.replace(":", "_")

    return name
def _is_image(path):
    filetype = path.split(".")[-1].lower()
    allowed = {"jpg", "png"}
    if filetype in allowed:
        return True
    print(f"filetype: {filetype}")
    return False
def Copy_image(src, rename = False):
    name = ""
    #print(src)
    if rename == True:
        name = _get_name_from_exif(src)
    #print("Name:", name)
    year = int(name.split("_")[0])
    month = int(name.split("_")[1])
    _create_month(year, month)
    month_path = _get_monthpath(year, month)
    dest = month_path + name
    #print("month path:", month_path)
    #print("src:", src)
    #print("filename:", dest)

    #copy the file
    shutil.copy(src, dest)




def Backup(drive):
    root = f"{drive}:\\"
    for file in get_files(root):
        #Needs to scan all files in drive
        # First, hash the file to check if exists
        file_hash = hash_file(file)
        #If file in library already, skip
        if file_hash in LIBRARY_FILES.keys():
            continue
        #file is not backed up. Get new filename if image
        #print(_get_name_from_exif(file))
        if _is_image(file):
            Copy_image(file, True)
        else:
            print(file, " was not an image")

        #break
        #print(f"{file} hashed to {files[file]}")
    print(f"Hashed {len(LIBRARY_FILES)} files")

if __name__ == "__main__":
    Backup("F")
