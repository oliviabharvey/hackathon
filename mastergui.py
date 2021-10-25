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

class MasterGUI:

    def __init__(self):

        if os.environ.get('DISPLAY','') != ':0.0':
            print('no display found. Using :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')

        self.puppets_filename = "puppets_info.csv" #convertir en yaml
        self.experiments_filename = "experiments.yaml"
        self.puppet_path_to_repo = "/home/pi/hackathon_souris/"
        # self.puppet_path_to_repo = "/home/pi/Projects/hackathon/"
        self.puppet_path_to_configs = self.puppet_path_to_repo + "configs/"
        self.puppet_path_to_results = self.puppet_path_to_repo + "results/"
        self.puppet_path_to_bash = self.puppet_path_to_repo + "bash_files/"
        self.master_path_to_repo = "/home/pi/hackathon/hackathon/"
        self.master_path_to_results = self.master_path_to_repo + "results/"
        self.master_path_to_configs = self.master_path_to_repo + "configs/"

        print("MasterGUI: Running GUI...")
        win = Tk()
        self.tab = {}
        self.mouse = {}
        self.puppets = {}
        self.experiment = {}
        self.lbl_tabs = {}
        self.lbl_tabs_config = {}
        self.lbl_tabs_command = {}
        self.lbl_tabs_status = {}
        self.btn_tabs = {}
        self.filename_config = {}
        self.filename_results = {}
        self.t_start = {}
        self.bash_file = {}
        self.thread_max_loops = 10
        self.thread_sleep_seconds = 5

        # create useful folder
        if not os.path.exists(self.master_path_to_results):
            os.mkdir(self.master_path_to_results)
        if not os.path.exists(self.master_path_to_configs):
            os.mkdir(self.master_path_to_configs)

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
        self.lbl_img.place(x=369,y=300)

        # Name of the mouse
        self.lbl_mouse = Label(self.tab['main'], text="Name of the mouse:")
        self.lbl_mouse.place(x=250,y=50)
        self.entry_mouse = Entry(self.tab['main'])
        self.entry_mouse.insert(END,"NAME")
        self.entry_mouse.place(x=400,y=50)
        
        # Choose which puppet RPi puppet to use
        self.read_puppets()
        self.lbl_puppet = Label(self.tab['main'], text="Puppet ID:")
        self.lbl_puppet.place(x=250,y=100)
        self.entry_puppet=Combobox(self.tab['main'], values=list(self.puppets.keys()))
        self.entry_puppet.place(x=400, y=100)

        # Choose which experiment to run
        self.lbl_exp = Label(self.tab['main'], text="Experiment to run:")
        self.lbl_exp.place(x=250,y=150)
        self.entry_exp=Combobox(self.tab['main'], values=self.read_experiments_yaml())
        self.entry_exp.place(x=400, y=150)

        # Run button
        self.btn = Button(self.tab['main'], text="Run", command=(lambda: [self.launch_exp()]))
        self.btn.place(x=380,y=250)

        # Build GUI
        win.title("Run experiment")
        win.geometry("800x410+0+0")
        win.mainloop()
        print("MasterGUI: Done.")

    def launch_exp(self):
        if self.entry_puppet.get() not in self.experiment:
            current_puppet = self.entry_puppet.get()
            self.mouse[current_puppet] = self.entry_mouse.get()
            self.experiment[current_puppet] = self.entry_exp.get()
            self.tab[current_puppet] = Frame(self.tabControl)
            self.tabControl.add(self.tab[current_puppet], text = current_puppet)
            self.lbl_tabs[current_puppet] = Label(self.tab[current_puppet], text=f"{current_puppet}: {self.experiment[current_puppet]}")
            self.lbl_tabs[current_puppet].place(x=50,y=50)
            self.tabControl.select(self.tab[current_puppet])
            self.print_config_to_yaml(current_puppet)
            self.ssh_send_config(current_puppet)
            self.ssh_run_command(current_puppet)
        else:
            self.warning(f"WARNING! An experiment is already running on {self.entry_puppet.get()} \n\nPlease select a different puppet.")

    def print_config_to_yaml(self,current_puppet):
        self.t_start[current_puppet] = datetime.datetime.now()
        t = self.t_start[current_puppet].strftime("%Y-%m-%dT%H%M%S")
        self.filename_config[current_puppet] = t + "_" + current_puppet.replace(" ","-") + "_" + self.experiment[current_puppet].replace(" ","-") + "_" + self.mouse[current_puppet].replace(" ","-") + "_config.yaml"
        self.filename_results[current_puppet] = self.filename_config[current_puppet].replace('_config','_results')
        self.bash_file[current_puppet] = current_puppet.replace(" ","_")+".sh"
        print(self.bash_file[current_puppet])
        print("MasterGUI: Printing experiment parameters to "+self.filename_config[current_puppet]+"...",end="")
        dict_to_yaml = {'mouse_name': self.mouse[current_puppet], 
                        'experiment': self.experiment[current_puppet],
                        'puppet': current_puppet,
                        'results': self.puppet_path_to_results+self.filename_results[current_puppet]}
        with open(self.master_path_to_configs+self.filename_config[current_puppet], 'w') as file:
            documents = yaml.dump(dict_to_yaml, file)
        print("OK.")

    def ssh_send_config(self,current_puppet):
        print('Sending config file to puppet..')
        path = self.puppet_path_to_configs
        filename = self.filename_config[current_puppet]
        username = self.puppets[current_puppet]['username']
        domain = self.puppets[current_puppet]['domain']
        ssh = subprocess.run(["scp", self.master_path_to_configs+filename, f"{username}@{domain}:{path}{filename}"])
        if ssh.returncode != 0:
            self.remove_puppet_from_current(current_puppet)
            self.warning(f"Copying config file to {current_puppet} failed.")
        else:
            self.lbl_tabs_config[current_puppet] = Label(self.tab[current_puppet], text="Sent confg file successfully...")
            self.lbl_tabs_config[current_puppet].place(x=50,y=75)

    def ssh_run_command(self,current_puppet):
        print('Running command...')
        path = self.puppet_path_to_configs
        filename = self.filename_config[current_puppet]
        username = self.puppets[current_puppet]['username']
        domain = self.puppets[current_puppet]['domain']
        command = "python "+ self.puppet_path_to_repo + "launch_experiment.py --cfg " + path + filename
        self.write_sh(current_puppet,command)
        try:
            ssh1 = subprocess.run(["scp", self.master_path_to_repo+self.bash_file[current_puppet], f"{username}@{domain}:{self.puppet_path_to_bash}{self.bash_file[current_puppet]}"])
            ssh2 = subprocess.run(["ssh", username+"@"+domain, "chmod u+x "+self.puppet_path_to_bash+self.bash_file[current_puppet]])
            ssh3 = subprocess.Popen(["ssh", username+"@"+domain, self.puppet_path_to_bash+self.bash_file[current_puppet]])
            self.lbl_tabs_command[current_puppet] = Label(self.tab[current_puppet], text="Running...")
            self.lbl_tabs_command[current_puppet].place(x=50,y=100)
            x = threading.Thread(target=self.ssh_fetch_status, args=(current_puppet,), daemon = True)
            x.start()
        except:
            self.remove_puppet_from_current(current_puppet)
            self.warning(f"Command to {current_puppet} failed.")


    def ssh_fetch_status(self,current_puppet):
        path = self.puppet_path_to_results
        filename = self.filename_results[current_puppet]
        username = self.puppets[current_puppet]['username']
        domain = self.puppets[current_puppet]['domain']
        i = 0
        while i<self.thread_max_loops:
            ssh = subprocess.run(["scp", f"{username}@{domain}:{path}{filename}", f"{self.master_path_to_results}{filename}"])
            if ssh.returncode != 0:
                i += 1
                if (datetime.datetime.now()-self.t_start[current_puppet]).seconds/60 > 80: #if it's been running for more than 80 minutes, cancel run
                    self.lbl_tabs_status[current_puppet] = Label(self.tab[current_puppet], text=f"Abnormally long experiment (running for more than 80 minutes). Canceled run.", justify="left")
                    self.lbl_tabs_status[current_puppet].place(x=50,y=125)
                    i = self.thread_max_loops
                else:
                    time.sleep(self.thread_sleep_seconds)
            else:
                #ici lire le fichier pour savoir si c'est complete ou une erreur...
                self.lbl_tabs_status[current_puppet] = Label(self.tab[current_puppet], text=f"Experiment complete! \n\nResults are here:\n{self.master_path_to_results}{self.filename_results[current_puppet]}", justify="left")
                self.lbl_tabs_status[current_puppet].place(x=50,y=150)
                i = self.thread_max_loops
                # Run button
                time.sleep(10)
                self.remove_puppet_from_current(current_puppet)
                # self.btn_tabs[current_puppet] = Button(self.tab[current_puppet], text="Finish", command=self.remove_puppet_from_current(current_puppet))
                # self.btn_tabs[current_puppet].place(x=380,y=250)

    def read_experiments_yaml(self,):
        # print("MasterGUI: Printing experiment parameters to "+self.filename_config[current_puppet]+"...",end="")
        with open(self.experiments_filename, 'r') as file:
            exps = yaml.safe_load(file)
        # print("OK."
        return exps['experiments']

    def read_puppets(self):
        file = open(self.puppets_filename)
        csvreader = csv.reader(file)
        for row in csvreader:
            self.puppets[row[0]] = {}
            self.puppets[row[0]]['username'] = row[1]
            self.puppets[row[0]]['domain'] = row[2]

    def remove_puppet_from_current(self,current_puppet):
        self.tabControl.forget(self.tab[current_puppet])
        self.mouse.pop(current_puppet, None)
        self.experiment.pop(current_puppet, None)
        self.tab.pop(current_puppet, None)
        self.lbl_tabs.pop(current_puppet, None)
        self.lbl_tabs_config.pop(current_puppet, None)
        self.lbl_tabs_command.pop(current_puppet, None)
        self.lbl_tabs_status.pop(current_puppet, None)
        self.filename_config.pop(current_puppet, None)
        self.filename_results.pop(current_puppet, None)
        self.t_start.pop(current_puppet, None)
        self.bash_file.pop(current_puppet, None)

    def warning(self,message):
        popup = Tk()
        lbl1_popup = Label(popup, text=f"{message}",wraplength=500, justify="center")
        lbl1_popup.place(x=50,y=50)
        popup.title("WARNING")
        popup.geometry("600x350+0+0")
        popup.mainloop()

    def write_sh(self,current_puppet,command):
        print(f"LogExpOutput: printing bash...")
        file = open(self.bash_file[current_puppet], "w")
        file.write("# "+self.bash_file[current_puppet])
        file.write("\ncd " + self.puppet_path_to_repo)
        file.write("\nsource /home/pi/miniconda3/bin/activate souris")
        file.write("\nsleep 5")
        file.write("\n"+command)
        file.close()
        print("OK.")


myWin = MasterGUI()