import os
from Tkinter import *

root = Tk()
# Code to add widgets will go here...
# app = Application(master=root)
# app.mainloop()


dir_name = "/Users/JoeWood/dev/api-laravel-mobileapi/app/Models/"
fileList = os.listdir(dir_name)
# print fileList
traversed_files = {}
for dirName, subdirList, fileList in os.walk(dir_name):
    fileArray = []
    for fname in fileList:
        fileArray.append(fname)
    traversed_files[dirName] = fileArray

print(help("modules"))
#phpParser = PHPParser(traversed_files)

root.destroy()
