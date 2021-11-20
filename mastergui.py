from tkinter import *
from tkinter.ttk import Combobox, Notebook
from PIL import Image, ImageTk
import datetime
import os
import csv
import yaml
import subprocess
import time
import threading
import sys

#add background to tabs and canvas. put str in canvas.

class MasterGUI:

    def __init__(self):

        print("MasterGUI: Running GUI...")

        if os.environ.get('DISPLAY','') != ':0.0':
            os.environ.__setitem__('DISPLAY', ':0.0')
        self.FNULL = open(os.devnull, 'w')

        # Threads parameters
        self.thread_max_time = 75 # minutes. If the experiment is not completed after this time, stop looking for a "completed" status
        self.thread_sleep_seconds = 1 # frequency (s) at which the status checker pings the puppet during run

        # Set paths
        self.puppet_path = {}
        self.master_path = {}
        self.puppet_path['repo'] = "/home/pi/hackathon_souris/" #"/home/pi/Projects/hackathon/"
        self.master_path['repo'] = "C:/dev/olivia/hackathon/"#"/home/pi/hackathon/hackathon/"
        self.puppets_info_filename = "puppets_info.csv"
        self.experiments_filename = "experiments.yaml"
        self.add_rel_path("configs")
        self.add_rel_path("results")
        self.add_rel_path("bash_files")
        self.add_rel_path("images")

        # Initialize vars
        self.tab = {}
        self.mouse = {}
        self.puppets = {}
        self.experiment = {}
        self.destination = {}
        self.t_start = {}
        self.bash_file = {}
        self.lbl_tabs = {}
        self.btn_tabs = {}
        self.filename_config = {}
        self.filename_results = {}
        self.back_img = {}
        self.background = {}
        self.background_lbl = {}
        self.btn_img = {}
        self.btn = {}
        self.status = {}
        
        # Create window (main tab)
        win = Tk()
        self.tabControl = Notebook(win)
        self.tab['main']=Frame(self.tabControl)
        self.tabControl.add(self.tab['main'], text = "Run")
        self.tabControl.pack(expand = 1, fill ="both")

        # Background
        self.background = ImageTk.PhotoImage(Image.open(self.master_path['images']+"gui_background.png"))
        self.gui_set_background('main')        

        # canvas
        self.canvas = Canvas(self.tab['main'],width=400,height=280,highlightthickness=2, highlightbackground="#3b607d")
        self.canvas.place(x=200,y=50)

        # Octopus
        self.img = Image.open(self.master_path['images']+"octopus.png")
        self.img = self.img.resize((60,60),Image.ANTIALIAS)
        self.test = ImageTk.PhotoImage(self.img)
        self.lbl_img = Label(self.tab['main'],image=self.test)
        self.lbl_img.image = self.test
        self.lbl_img.place(x=400-60/2,y=265)

        # Name of the mouse
        self.lbl_mouse = Label(self.tab['main'], text="Name of the mouse:",font=("Arial",11))
        self.lbl_mouse.place(x=240,y=70)
        self.entry_mouse = Entry(self.tab['main'],font=("Arial",12),borderwidth=0.5)#,highlightthickness=1)
        self.entry_mouse.insert(END,"Mouse")
        self.entry_mouse.place(x=410,y=70,height=25,width=147)
        
        # Choose which puppet RPi puppet to use
        self.read_puppets()
        self.lbl_puppet = Label(self.tab['main'], text="Puppet ID:",font=("Arial",11))
        self.lbl_puppet.place(x=240,y=120)
        self.entry_puppet=Combobox(self.tab['main'], font=('Arial', 12), width=14, values=list(self.destination.keys()))
        popdown = self.entry_puppet.tk.eval('ttk::combobox::PopdownWindow %s' % self.entry_puppet)
        self.entry_puppet.tk.call('%s.f.l' % popdown, 'configure', '-font', self.entry_puppet['font'])
        self.entry_puppet.place(x=410, y=120)

        # Choose which experiment to run
        self.lbl_exp = Label(self.tab['main'], text="Experiment to run:",font=("Arial",11))
        self.lbl_exp.place(x=240,y=170)
        self.entry_exp=Combobox(self.tab['main'], font=('Arial', 12), width=14, values=self.read_experiments_yaml())
        popdown = self.entry_exp.tk.eval('ttk::combobox::PopdownWindow %s' % self.entry_exp)
        self.entry_exp.tk.call('%s.f.l' % popdown, 'configure', '-font', self.entry_exp['font'])
        self.entry_exp.place(x=410, y=170)

        # Run button
        self.gui_button('main',self.master_path['images']+"run_button.png","run")

        # Build GUI
        win.title("Run experiment")
        win.geometry("800x410+0+0")
        win.mainloop()

    def gui_button(self,tab,img_file,action):
        self.btn_width = 70
        self.btn_img[tab] = Image.open(img_file)
        self.btn_img[tab] = self.btn_img[tab].resize((self.btn_width,35),Image.ANTIALIAS)
        self.btn_img[tab] = ImageTk.PhotoImage(self.btn_img[tab])
        if action == "run":
            self.btn[tab] = Button(self.tab[tab], image=self.btn_img[tab], command=(lambda: [self.launch_exp()]),borderwidth=0,highlightthickness=0)
            self.btn[tab].place(x=400-self.btn_width/2+5,y=220)
        elif action == "finish":
            self.btn[tab] = Button(self.tab[tab], image=self.btn_img[tab], command=(lambda: [self.remove_puppet_from_current(tab)]),borderwidth=0,highlightthickness=0)
            self.btn[tab].place(x=400-self.btn_width/2+5,y=270)
        elif action == "cancel":
            self.btn[tab] = Button(self.tab[tab], image=self.btn_img[tab], command=(lambda: [self.ssh_cancel_command(tab)]),borderwidth=0,highlightthickness=0)
            self.btn[tab].place(x=600-self.btn_width/2+100,y=270)        

    def gui_set_background(self,tab):
        self.background_lbl[tab] = Label(self.tab[tab],image=self.background)
        self.background_lbl[tab].place(x=0,y=0)

    def launch_exp(self):
        if self.entry_puppet.get() not in self.tab and self.entry_puppet.get() != "":
            try:
                puppet = self.get_gui_input()
                self.status[puppet] = 'running'
                self.create_new_tab(puppet)
                self.gui_button(puppet,self.master_path['images']+"cancel_button.png","cancel")
                self.create_filenames(puppet)
                # Run experiment in thread
                t1 = threading.Thread(target=self.ssh_run, args=(self.entry_puppet.get(),), daemon = True)
                t1.start()
                # Check status of experiment
                t2 = threading.Thread(target=self.ssh_fetch_status, args=(self.entry_puppet.get(),), daemon = True)
                t2.start()
                for thread in threading.enumerate(): 
                    print(thread.name)
            except Exception as e:
                self.warning(f"Experiment raised an error:\n{e}")
                self.gui_button(self.entry_puppet.get(),self.master_path['images']+"finish_button.png","finish")
        elif self.entry_puppet.get() == "":
            self.warning("Please enter a valid mouse name, setup ID and experiment name.")
        else:
            self.warning(f"WARNING! An experiment is already running on {self.entry_puppet.get()} \n\nPlease select a different puppet.")

    def ssh_run(self,puppet):
        self.print_config_to_yaml(puppet)
        self.ssh_send_config(puppet)
        self.ssh_run_command(puppet)
        sys.exit()
         
    def print_config_to_yaml(self,puppet):
        dict_to_yaml = {'mouse_name': self.mouse[puppet], 
                        'experiment': self.experiment[puppet],
                        'puppet': puppet,
                        'results': self.puppet_path['results']+self.filename_results[puppet]}
        with open(self.master_path['configs']+self.filename_config[puppet], 'w') as file:
            yaml.dump(dict_to_yaml, file)

    def ssh_send_config(self,puppet):
        config_puppet = self.puppet_path['configs'] + self.filename_config[puppet]
        config_master = self.master_path['configs'] + self.filename_config[puppet]
        ssh = subprocess.run(["scp", config_master, f"{self.destination[puppet]}:{config_puppet}"])
        if ssh.returncode != 0:
            self.lbl_append(puppet,f"Copying config file to {puppet} failed.")
            self.gui_button(self.entry_puppet.get(),self.master_path['images']+"finish_button.png","finish")
            raise ValueError(f"Copying config file to {puppet} failed.")
        else:
            self.lbl_append(puppet,"\nSent confg file successfully...")

    def ssh_run_command(self,puppet):
        config_puppet = self.puppet_path['configs'] + self.filename_config[puppet]
        bash_puppet = self.puppet_path['bash_files'] + self.bash_file[puppet]
        bash_master = self.master_path['bash_files'] + self.bash_file[puppet]
        command = "python "+ self.puppet_path['repo'] + "launch_experiment.py --cfg " + config_puppet
        self.write_sh(puppet,command)
        self.lbl_append(puppet,"Launching python script on puppet:")
        try:
            self.lbl_append(puppet,"Sending bash file...")
            subprocess.run(["scp", bash_master, f"{self.destination[puppet]}:{bash_puppet}"])
            self.lbl_append(puppet,"Changing permission on bash file...")
            subprocess.run(["ssh", self.destination[puppet], "chmod u+x "+bash_puppet])
            self.lbl_append(puppet,"Running python script...")
            subprocess.Popen(["ssh", self.destination[puppet], bash_puppet])
        except:
            self.lbl_append(puppet,f"Command to {puppet} failed.")
            self.gui_button(self.entry_puppet.get(),self.master_path['images']+"finish_button.png","finish")
            raise ValueError(f"Command to {puppet} failed.")

    def ssh_fetch_status(self,puppet):
        filename_puppet = self.puppet_path['results'] + self.filename_results[puppet]
        filename_master = self.master_path['results'] + self.filename_results[puppet]
        completed = False
        while puppet in self.t_start and (datetime.datetime.now()-self.t_start[puppet]).seconds/60<=self.thread_max_time and not completed:
            ssh = subprocess.run(["scp", f"{self.destination[puppet]}:{filename_puppet}", f"{filename_master}"],stdout=self.FNULL, stderr=subprocess.STDOUT)
            if ssh.returncode != 0:
                time.sleep(self.thread_sleep_seconds)
            else:
                status = self.read_status(self,puppet)
                print(status)
                if status == "completed":
                    self.lbl_append(puppet,f"Experiment complete! \n\nResults are here:\n{self.master_path['results']}{self.filename_results[puppet]}")
                    self.gui_button(self.entry_puppet.get(),self.master_path['images']+"finish_button.png","finish")
                    completed = True
                elif status == "error":
                    self.lbl_append(puppet,f"Error raised on puppet.")
                    self.gui_button(self.entry_puppet.get(),self.master_path['images']+"finish_button.png","finish")
                    completed = True
        if puppet in self.t_start and not completed:
            self.lbl_append(puppet,f"Experiment lasted more than {self.thread_max_time} minutes without any output file generated.")
            self.ssh_cancel_command(puppet)

        sys.exit()

    def ssh_cancel_command(self,puppet):
        command = "pkill -9 python "
        self.lbl_append(puppet,f"Killing all python processes on {puppet}:")
        ssh = subprocess.run(["ssh", self.destination[puppet], command])
        if ssh!= 0:
            self.lbl_append(puppet,f"Failed. Trying again...")
            ssh = subprocess.run(["ssh", self.destination[puppet], command])
            if ssh != 0: 
                self.lbl_append(puppet,f"Failed. Please restart puppet.")
                self.gui_button(self.entry_puppet.get(),self.master_path['images']+"finish_button.png","finish")
            else:
                self.gui_button(self.entry_puppet.get(),self.master_path['images']+"finish_button.png","finish")
        else:
            self.gui_button(self.entry_puppet.get(),self.master_path['images']+"finish_button.png","finish")

    def read_experiments_yaml(self,):
        with open(self.master_path['repo'] + self.experiments_filename, 'r') as file:
            exps = yaml.safe_load(file)
        return exps['experiments']

    def read_puppets(self):
        file = open(self.master_path['repo'] + self.puppets_info_filename)
        csvreader = csv.reader(file)
        for row in csvreader:
            self.destination[row[0]] = row[1] + "@" +row[2]

    def remove_puppet_from_current(self,puppet):
        self.tabControl.forget(self.tab[puppet])
        for attr in self.__dict__:
            val = getattr(self,attr)
            if type(val) is dict and puppet in val and attr != "destination":
                self.__dict__[attr].pop(puppet,None)
        for thread in threading.enumerate(): 
            print(thread.name)                

    def warning(self,message):
        popup = Tk()
        lbl1_popup = Label(popup, text=f"{message}",wraplength=500, justify="center",font=("Arial",12))
        lbl1_popup.place(x=50,y=50)
        popup.title("WARNING")
        popup.geometry("600x350+100+30")
        popup.mainloop()

    def write_sh(self,puppet,command):
        file = open(self.master_path['bash_files'] + self.bash_file[puppet], "w")
        file.write("# "+
        self.bash_file[puppet])
        file.write("\ncd " + self.puppet_path['repo'])
        file.write("\nsource /home/pi/miniconda3/bin/activate souris")
        file.write("\n"+command)
        file.close()

    def lbl_append(self,puppet,string):
        text = self.lbl_tabs[puppet].cget("text") + "\n" + string
        self.lbl_tabs[puppet].configure(text=text)

    def get_gui_input(self):
        puppet = self.entry_puppet.get()
        self.mouse[puppet] = self.entry_mouse.get()
        self.experiment[puppet] = self.entry_exp.get()
        if self.mouse[puppet] == '' or self.experiment[puppet] == '' or puppet == '':
            raise ValueError("Please enter a valid mouse name, setup ID and experiment name.")
        return puppet

    def create_new_tab(self,puppet):
        self.tab[puppet] = Frame(self.tabControl)
        self.gui_set_background(puppet)
        self.canvas = Canvas(self.tab[puppet],width=700,height=280,highlightthickness=2, highlightbackground="#3b607d")
        self.canvas.place(x=50,y=50)
        self.tabControl.add(self.tab[puppet], text = puppet)
        self.lbl_tabs[puppet] = Label(self.tab[puppet], text=f"{puppet} - Starting experiment: {self.experiment[puppet]}\n",justify="left",font=("Arial",10))
        self.lbl_tabs[puppet].place(x=52,y=52)
        self.tabControl.select(self.tab[puppet])
        self.tabControl.pack(expand = 1, fill ="both")

    def create_filenames(self,puppet):
        self.t_start[puppet] = datetime.datetime.now()
        t = self.t_start[puppet].strftime("%Y-%m-%dT%H%M%S")
        self.filename_config[puppet] = t + "_" + puppet.replace(" ","-") + "_" + self.experiment[puppet].replace(" ","-") + "_" + self.mouse[puppet].replace(" ","-") + "_config.yaml"
        self.filename_results[puppet] = self.filename_config[puppet].replace('_config','_results')
        self.bash_file[puppet] = puppet.replace(" ","_")+".sh"

    def add_rel_path(self,string):
        self.puppet_path[string] = self.puppet_path['repo'] + string + "/"
        self.master_path[string] = self.master_path['repo'] + string + "/"
        if not os.path.exists(self.master_path[string]):
            os.mkdir(self.master_path[string])

    def read_status(self,puppet):
        with open(self.master_path['results'] + self.filename_results[puppet], 'r') as file:
            out = yaml.safe_load(file)
        return out['status']


if __name__ == "__main__":
    myWin = MasterGUI()