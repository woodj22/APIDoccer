import os
from tkinter import *
from APIDoccer.PHPParser import *
root = Tk()
# Code to add widgets will go here...
# app = Application(master=root)
# app.mainloop()


dir_name = "/Users/JoeWood/dev/api-laravel-mobileapi/app/Models/"
fileList = os.listdir(dir_name)
# print fileList
traversed_files = {}
for dirName, subdirList, fileList in os.walk(dir_name):
    traversed_files[dirName] = fileList

phpParser = PHPParser(traversed_files)
sys.exit(list(phpParser.findProtectedFields()));
root.destroy()
