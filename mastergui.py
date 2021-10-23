from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import datetime
import os

class MasterGUI:

    def __init__(self,setups,experiments):

        if os.environ.get('DISPLAY','') == '':
            print('no display found. Using :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')

        print("MasterGUI: Running GUI...")
        win = Tk()

        # Octopus
        self.img = Image.open("octopus.jpg")
        self.img = self.img.resize((50,50),Image.ANTIALIAS)
        self.test = ImageTk.PhotoImage(self.img)
        self.lbl_img = Label(win,image=self.test)
        self.lbl_img.image = self.test
        self.lbl_img.place(x=177,y=300)

        # Name of the mouse
        self.lbl_mouse = Label(win, text="Name of the mouse:")
        self.lbl_mouse.place(x=50,y=50)
        self.entry_mouse = Entry()
        self.entry_mouse.insert(END,"NAME")
        self.entry_mouse.place(x=200,y=50)
        
        # Choose which puppet RPi setup to use
        self.lbl_setup = Label(win, text="Setup ID:")
        self.lbl_setup.place(x=50,y=100)
        self.entry_setup=Combobox(win, values=setups)
        self.entry_setup.insert(END,setups[0])
        self.entry_setup.place(x=200, y=100)

        # Choose which experiment to run
        self.lbl_exp = Label(win, text="Experiment to run:")
        self.lbl_exp.place(x=50,y=150)
        self.entry_exp=Combobox(win, values=experiments)
        self.entry_exp.insert(END,experiments[0])
        self.entry_exp.place(x=200, y=150)

        # Run button
        self.btn = Button(win, text="Run", command=(lambda: [self.print_to_txt_file(), win.destroy()]))
        self.btn.place(x=190,y=250)

        # Build GUI
        win.title("Run experiment")
        win.geometry("400x400+20+20")
        win.mainloop()
        print("MasterGUI: Done.")

    def print_to_txt_file(self):
        mouse = self.entry_mouse.get()
        setup = self.entry_setup.get()
        exp = self.entry_exp.get()
        t = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
        self.filename = t + "_" + setup.replace(" ","-") + "_" + exp.replace(" ","-") + "_" + mouse.replace(" ","-") + ".txt"
        print("MasterGUI: Printing experiment parameters to "+self.filename+"...")
        file = open(self.filename,"w")
        file.writelines([mouse, "\n"+setup, "\n"+exp])
        file.close()

setups = ["Setup 1","Setup 2","Setup 3","Setup 4"]
experiments = ["Experiment 1","Experiment 2","Experiment 3","Experiment 4","Experiment 5","Experiment 6","Experiment 7","Experiment 8"]
myWin = MasterGUI(setups,experiments)