
from Item import Item
from Tkinter import *
import tkFileDialog
import os
import glob
class Application(Frame):


    def __init__(self, master=None):  # this method creates the class object.
        Frame.__init__(self, master)

        self.createWidgets()
        self.pack()

    def createWidgets(self):
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
        os.chdir(dir_name)
        for file in glob.glob("*"):
            print(file)


    def say_hi(self):
        print "hi there, everyone!"



root = Tk()
# Code to add widgets will go here...
app = Application(master=root)
app.mainloop()
root.destroy()
