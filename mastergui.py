from tkinter import *
from tkinter.ttk import Combobox, Notebook
from PIL import Image, ImageTk
import datetime
import os
import csv

class MasterGUI:

    def __init__(self,puppets,experiments):

        if os.environ.get('DISPLAY','') != ':0.0':
            print('no display found. Using :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')

        self.puppets_filename = puppets

        print("MasterGUI: Running GUI...")
        win = Tk()
        self.tab = {}
        self.mouse = {}
        self.puppets = {}
        self.experiment = {}
        self.lbl_tabs = {}

       # create first tab
        self.tabControl = Notebook(win)
        self.tab['main']=Frame(self.tabControl)
        self.tabControl.add(self.tab['main'], text = "Run")
        self.tabControl.pack(expand = 1, fill ="both")

        # Octopus
        self.img = Image.open("octopus.jpg")
        self.img = self.img.resize((50,50),Image.ANTIALIAS)
        self.test = ImageTk.PhotoImage(self.img)
        self.lbl_img = Label(self.tab['main'],image=self.test)
        self.lbl_img.image = self.test
        self.lbl_img.place(x=177,y=300)

        # Name of the mouse
        self.lbl_mouse = Label(self.tab['main'], text="Name of the mouse:")
        self.lbl_mouse.place(x=50,y=50)
        self.entry_mouse = Entry(self.tab['main'])
        self.entry_mouse.insert(END,"NAME")
        self.entry_mouse.place(x=200,y=50)
        
        # Choose which puppet RPi puppet to use
        self.read_puppets()
        self.lbl_puppet = Label(self.tab['main'], text="Puppet ID:")
        self.lbl_puppet.place(x=50,y=100)
        self.entry_puppet=Combobox(self.tab['main'], values=list(self.puppets.keys()))
        self.entry_puppet.place(x=200, y=100)

        # Choose which experiment to run
        self.lbl_exp = Label(self.tab['main'], text="Experiment to run:")
        self.lbl_exp.place(x=50,y=150)
        self.entry_exp=Combobox(self.tab['main'], values=experiments)
        self.entry_exp.place(x=200, y=150)

        # Run button
        self.btn = Button(self.tab['main'], text="Run", command=(lambda: [self.launch_exp()]))
        self.btn.place(x=190,y=250)

        # Build GUI
        win.title("Run experiment")
        win.geometry("400x400+20+20")
        win.mainloop()
        print("MasterGUI: Done.")

    def launch_exp(self):
        if self.entry_puppet.get() not in self.experiment:
            current_puppet = self.entry_puppet.get()
            self.mouse[current_puppet] = self.entry_mouse.get()
            self.experiment[current_puppet] = self.entry_exp.get()
            self.tab[current_puppet] = Frame(self.tabControl)
            self.tabControl.add(self.tab[current_puppet], text = current_puppet)
            self.lbl_tabs[current_puppet] = Label(self.tab[current_puppet], text=f"{current_puppet}: Running {self.experiment[current_puppet]}...")
            self.lbl_tabs[current_puppet].place(x=50,y=50)
            self.tabControl.select(self.tab[current_puppet])
            self.print_to_log_file(current_puppet)
            self.ssh_connect(current_puppet)
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

    def print_to_log_file(self,current_puppet):
        t = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
        self.filename = t + "_" + current_puppet.replace(" ","-") + "_" + self.experiment[current_puppet].replace(" ","-") + "_" + self.mouse[current_puppet].replace(" ","-") + ".txt"
        self.filename_log = "log_" + self.filename
        print("MasterGUI: Printing experiment parameters to "+self.filename+"...",end="")
        file = open(self.filename,"w")
        file.writelines([self.mouse[current_puppet], "\n"+current_puppet, "\n"+self.experiment[current_puppet]])
        file.close()
        print("OK.")

    def read_puppets(self):
        file = open(self.puppets_filename)
        csvreader = csv.reader(file)
        for row in csvreader:
            self.puppets[row[0]] = {}
            self.puppets[row[0]]['username'] = row[1]
            self.puppets[row[0]]['domain'] = row[2]
            self.puppets[row[0]]['password'] = row[3]

    def ssh_connect(self,current_puppet):
        #add file to read data from
        command = "ls"
        print(f"MasterGUI: command to RPi system will be : sshpass -p {self.puppets[current_puppet]['password']} ssh {self.puppets[current_puppet]['username']}@{self.puppets[current_puppet]['domain']} {command}")
        os.system(f"sshpass -p {self.puppets[current_puppet]['password']} ssh {self.puppets[current_puppet]['username']}@{self.puppets[current_puppet]['domain']} {command}")

#read IP and puppets domains from file.
#connect to rpi.
#run script on rpi with filename input (check with JS)
#check state and show on screen
# if complete, add button to tab to close tab and remove setup from list of busy setups. 
# comment je vais dealer avec les exp que j'enlève? faudra l'enlever dans tous les appends... a revoir. 


puppets = "puppets_info.csv"
experiments = ["Experiment 1","Experiment 2","Experiment 3","Experiment 4","Experiment 5","Experiment 6","Experiment 7","Experiment 8"]
myWin = MasterGUI(puppets,experiments)