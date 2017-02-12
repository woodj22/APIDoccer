
from Item import Item
from PHPParser import PHPParser
from Tkinter import *
import tkFileDialog
import os
import glob
class Application(Frame):


    def __init__(self, master=None):  # this method creates the class object.
        Frame.__init__(self, master)

       # self.createButtons()
        # self.pack()
        self.chooseFile()

    def createButtons(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "choose file",
        self.hi_there["command"] = self.chooseFile
        self.hi_there.pack({"side": "left"})

    def chooseFile(self):
        #fileName = tkFileDialog.askopenfilename()
        dir_name = "/Users/JoeWood/dev/api-laravel-mobileapi/app/Models/"
        fileList = os.listdir(dir_name)
        #print fileList
        os.chdir(dir_name)
        print glob.glob(dir_name+"/*/"+"*.php")


        #for file in glob.glob("*"):
            #print(file)




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
phpParser = PHPParser(traversed_files)

root.destroy()
