from tkinter import *
from tkinter.ttk import Combobox, Notebook
from PIL import Image, ImageTk
import datetime
import os

class MasterGUI:

    def __init__(self,puppets,experiments):

        if os.environ.get('DISPLAY','') != ':0.0':
            print('no display found. Using :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')

        print("MasterGUI: Running GUI...")
        win = Tk()
        self.tab = []
        self.mouse = []
        self.puppet = []
        self.experiment = []
        self.lbl_tabs = []
        self.i_exp = -1
        self.i_tab = 0
        self.puppets_running = []
        self.puppets_info = []

        for item in puppets:
            self.puppets_info.append(f"{item}: {puppets[item]}")

       # create first tab
        self.tabControl = Notebook(win)
        self.tab.append(Frame(self.tabControl))
        self.tabControl.add(self.tab[0], text = "Run")
        self.tabControl.pack(expand = 1, fill ="both")

        # Octopus
        self.img = Image.open("octopus.jpg")
        self.img = self.img.resize((50,50),Image.ANTIALIAS)
        self.test = ImageTk.PhotoImage(self.img)
        self.lbl_img = Label(self.tab[0],image=self.test)
        self.lbl_img.image = self.test
        self.lbl_img.place(x=177,y=300)

        # Name of the mouse
        self.lbl_mouse = Label(self.tab[0], text="Name of the mouse:")
        self.lbl_mouse.place(x=50,y=50)
        self.entry_mouse = Entry(self.tab[0])
        self.entry_mouse.insert(END,"NAME")
        self.entry_mouse.place(x=200,y=50)
        
        # Choose which puppet RPi puppet to use
        self.lbl_puppet = Label(self.tab[0], text="Puppet ID:")
        self.lbl_puppet.place(x=50,y=100)
        self.entry_puppet=Combobox(self.tab[0], values=self.puppets_info)
        # self.entry_puppet.insert(END,puppets[0])
        self.entry_puppet.place(x=200, y=100)

        # Choose which experiment to run
        self.lbl_exp = Label(self.tab[0], text="Experiment to run:")
        self.lbl_exp.place(x=50,y=150)
        self.entry_exp=Combobox(self.tab[0], values=experiments)
        # self.entry_exp.insert(END,experiments[0])
        self.entry_exp.place(x=200, y=150)

        # Run button
        self.btn = Button(self.tab[0], text="Run", command=(lambda: [self.launch_exp()]))
        self.btn.place(x=190,y=250)

        # Build GUI
        win.title("Run experiment")
        win.geometry("400x400+20+20")
        win.mainloop()
        print("MasterGUI: Done.")

    def launch_exp(self):
        if self.entry_puppet.get() not in self.puppets_running:
            self.i_tab += 1
            self.i_exp += 1
            self.mouse.append(self.entry_mouse.get())
            self.puppet.append(self.entry_puppet.get())
            self.experiment.append(self.entry_exp.get())
            self.puppets_running.append(self.puppet[self.i_exp])
            self.tab.append(Frame(self.tabControl))
            self.tabControl.add(self.tab[self.i_tab], text = self.puppet[self.i_exp])
            self.lbl_tabs.append(Label(self.tab[self.i_tab], text=f"{self.puppet[self.i_exp]}: Running {self.experiment[self.i_exp]}..."))
            self.lbl_tabs[self.i_exp].place(x=50,y=50)
            self.tabControl.select(self.tab[self.i_tab])
            self.print_to_log_file()
        else:
            self.warning("Please select a different puppet.")


    def warning(self,message):
        popup = Tk()
        lbl1_popup = Label(popup, text=f"WARNING! An experiment is already running on {self.entry_puppet.get()}")
        lbl1_popup.place(x=50,y=50)
        lbl2_popup = Label(popup, text=f"{message}")
        lbl2_popup.place(x=50,y=100)
        popup.title("WARNING")
        popup.geometry("500x200+0+0")
        popup.mainloop()

    def print_to_log_file(self):
        t = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
        self.filename = t + "_" + self.puppet[self.i_exp].replace(" ","-") + "_" + self.experiment[self.i_exp].replace(" ","-") + "_" + self.mouse[self.i_exp].replace(" ","-") + ".txt"
        self.filename_log = "log_" + self.filename
        print("MasterGUI: Printing experiment parameters to "+self.filename+"...",end="")
        file = open(self.filename,"w")
        file.writelines([self.mouse[self.i_exp], "\n"+self.puppet[self.i_exp], "\n"+self.experiment[self.i_exp]])
        file.close()
        print("OK.")



#connect to rpi.
#run script on rpi with filename input (check with JS)
#check state and show on screen
# if complete, add button to tab to close tab and remove setup from list of busy setups. 

puppets = {'Setup 1':'ip1','Setup 2':'ip2','Setup 3':'ip3','Setup 4':'ip4'}
experiments = ["Experiment 1","Experiment 2","Experiment 3","Experiment 4","Experiment 5","Experiment 6","Experiment 7","Experiment 8"]
myWin = MasterGUI(puppets,experiments)