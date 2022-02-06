import csv
import datetime
import logging
import subprocess
import sys
import time
import threading
import os
import yaml
from tkinter import *
from tkinter.ttk import Combobox, Notebook
from typing import List
from PIL import Image, ImageTk

class MasterGUI:

    def __init__(self):
        """
        Runs the graphical user interface on the master puppet (RPi)
        """

        # Debug parameters
        self.debug = False # Debug mode will put default values in GUI fields + launches experiments in debug mode
        self.stdout_nlines = 6 # Number of lines shown in the live output shown while running experiments
        self.debug_default_puppet_idx = 1 # Position of default puppet idx
        self.debug_default_exp_idx = 1 # Position of default experiment idx

        # Initialize logger
        self.set_logger('master-gui',debug=self.debug)
        self.logger.info("MasterGUI: Running GUI...")

        # Setting display environment variable
        if os.environ.get('DISPLAY','') != ':0.0':
            os.environ.__setitem__('DISPLAY', ':0.0')

        # Thread parameters
        self.thread_max_time = 120 # default max. run time in minutes. If exceeded, we assume that there was a problem.
        self.thread_sleep_seconds = 1 # frequency (s) at which the status checker pings the puppet during run
        self.poke_screen_seconds = 60 #  seconds. Poke the puppet screen to make sure it doesn't go to sleep (screensaver activation time: 120s)
        self.screen_activation_wait_time = 5 # Seconds. Wait before waking up the screen at the beginning of the experiment

        # Set paths/filename variables
        self.puppet_path = {}
        self.master_path = {}
        self.puppet_path['repo'] = "/home/pi/hackathon_souris/" #"/home/pi/Projects/hackathon/"
        self.master_path['repo'] = "/home/pi/hackathon/hackathon/"
        self.puppets_info_filename = "puppets_info.csv"
        self.experiments_filename = "experiments.yaml"
        self.img_background = "gui_background.png"
        self.img_octopus = "octopus.png"
        self.img_run_button = "run_button.png"
        self.img_cancel_button = "cancel_button.png"
        self.img_finish_button = "finish_button.png"

        # Create sub folders if they don't exist
        self.add_rel_path("configs")
        self.add_rel_path("results")
        self.add_rel_path("bash_files")
        self.add_rel_path("images")
        self.add_rel_path("experiments")
        
        # Gui button parameters
        self.btn_width = 70
        self.btn_height = 35

        # Initialize variables
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
        self.exp_duration = {}

        # Create window (+ main tab)
        win = Tk()
        self.tabControl = Notebook(win)
        self.tab['main']=Frame(self.tabControl)
        self.tabControl.add(self.tab['main'], text = "Run")
        self.tabControl.pack(expand = 1, fill ="both")

        # Set + Add background
        self.background = ImageTk.PhotoImage(Image.open(self.master_path['images']+self.img_background))
        self.gui_set_background('main')        

        # Add canvas
        self.canvas = Canvas(self.tab['main'],width=400,height=280,highlightthickness=2, highlightbackground="#3b607d")
        self.canvas.place(x=200,y=50)

        # Add octopus image
        self.img = Image.open(self.master_path['images']+self.img_octopus)
        self.img = self.img.resize((60,60),Image.ANTIALIAS)
        self.test = ImageTk.PhotoImage(self.img)
        self.lbl_img = Label(self.tab['main'],image=self.test)
        self.lbl_img.image = self.test
        self.lbl_img.place(x=400-60/2,y=265)

        # Add entry (empty field) : Name of the mouse
        self.lbl_mouse = Label(self.tab['main'], text="Name of the mouse:",font=("Arial",11))
        self.lbl_mouse.place(x=240,y=70)
        self.entry_mouse = Entry(self.tab['main'],font=("Arial",12),borderwidth=0.5)
        if self.debug: # Debug mode : insert default value
            self.entry_mouse.insert(END,"Mouse")
        self.entry_mouse.place(x=410,y=70,height=25,width=147)

        # Add entry (dropdown) : Choose which puppet RPi puppet to use
        self.read_puppets() # Raads list of available puppet from file
        self.lbl_puppet = Label(self.tab['main'], text="Puppet ID:",font=("Arial",11))
        self.lbl_puppet.place(x=240,y=120)
        self.entry_puppet=Combobox(self.tab['main'], font=('Arial', 12), width=14, values=list(self.destination.keys()))
        if self.debug: # Debug mode : insert default value
            self.entry_puppet.current(self.debug_default_puppet_idx)
        popdown = self.entry_puppet.tk.eval('ttk::combobox::PopdownWindow %s' % self.entry_puppet)
        self.entry_puppet.tk.call('%s.f.l' % popdown, 'configure', '-font', self.entry_puppet['font'])
        self.entry_puppet.place(x=410, y=120)

        # Add entry (dropdown) : Choose which experiment to run
        self.lbl_exp = Label(self.tab['main'], text="Experiment to run:",font=("Arial",11))
        self.lbl_exp.place(x=240,y=170)
        self.entry_exp=Combobox(self.tab['main'], font=('Arial', 12), width=14, values=self.read_experiments_yaml())
        if self.debug:
            self.entry_exp.current(self.debug_default_exp_idx)
        popdown = self.entry_exp.tk.eval('ttk::combobox::PopdownWindow %s' % self.entry_exp)
        self.entry_exp.tk.call('%s.f.l' % popdown, 'configure', '-font', self.entry_exp['font'])
        self.entry_exp.place(x=410, y=170)

        # Add run button
        self.gui_button('main',self.master_path['images']+self.img_run_button,"run")

        # Launch GUI
        win.title("Run experiment")
        win.geometry("800x410+0+0")
        win.mainloop()

    def gui_button(self,tab: str,img_file: str,action: str):
        """
        Create a button on a specific tab (RUN, CANCEL, or FINISH).
        The position of the button is hardcoded in this method and specific to each type of button.
        Inputs:
            - tab: Name of the tab
            - img_file: Image file we want to use as the button
            - action: Action we want the button to do (run exp., cancel exp., finish)
        """
        self.btn_img[tab] = Image.open(img_file)
        self.btn_img[tab] = self.btn_img[tab].resize((self.btn_width,self.btn_height),Image.ANTIALIAS)
        self.btn_img[tab] = ImageTk.PhotoImage(self.btn_img[tab])
        if action == "run": # Launch/run the experiment
            self.btn[tab] = Button(self.tab[tab], image=self.btn_img[tab], command=(lambda: [self.launch_exp()]),borderwidth=0,highlightthickness=0)
            self.btn[tab].place(x=400-self.btn_width/2+5,y=220)
        elif action == "finish": # Close current tab and remove puppet from current variables
            self.btn[tab] = Button(self.tab[tab], image=self.btn_img[tab], command=(lambda: [self.btn[tab].place_forget(), self.remove_puppet_from_current(tab)]),borderwidth=0,highlightthickness=0)
            self.btn[tab].place(x=400-self.btn_width/2+5,y=280)
        elif action == "cancel": # Cancel run (for a specific puppet)
            self.btn[tab] = Button(self.tab[tab], image=self.btn_img[tab], command=(lambda: [self.btn[tab].place_forget(), self.ssh_cancel_command(tab)]),borderwidth=0,highlightthickness=0)
            self.btn[tab].place(x=600-self.btn_width/2+100,y=280)    

    def gui_set_background(self,tab: str):
        """
        Set the background for a specific tab (set background is the same for all tabs).
        Inputs:
            - tab: Name of the tab
        """
        self.background_lbl[tab] = Label(self.tab[tab],image=self.background)
        self.background_lbl[tab].place(x=0,y=0)

    def gui_button_remove(self,tab: str):
        """
        Remove button from tab
        Inputs:
            - tab: Name of the tab
        """
        self.btn[tab].place_forget()

    def launch_exp(self):
        """
        Launches experiment based on current info in GUI fields
        """
        if self.entry_puppet.get() not in self.tab and all([self.entry_puppet.get(), self.entry_mouse.get(), self.entry_exp.get()]): # if exp. is not already running on puppet
            try:
                puppet = self.get_gui_input() # get current puppet + add attributes to self for this puppet (exp. type, name of mouse)
                self.status[puppet] = 'running' # update puppet status
                self.create_new_tab(puppet) # create new tab for this puppet
                self.gui_button(puppet,self.master_path['images']+self.img_cancel_button,"cancel") # add cancel button
                self.t_start[puppet] = datetime.datetime.now() # start time of the experiment
                self.create_filenames(puppet)

                self.logger.info("MasterGUI: Launching experiment on "+puppet+".")

                # Thread 1: Run experiment
                t1 = threading.Thread(target=self.ssh_run, args=(puppet,), daemon=True)
                t1.start()
                # Thread 2: Check status of experiment
                t2 = threading.Thread(target=self.ssh_fetch_status, args=(puppet,), daemon = True)
                t2.start()
                # Thread 3: Keep screen from going to sleep on puppet
                t3 = threading.Thread(target=self.ssh_keep_screen_active, args=(puppet,), daemon = True)
                t3.start()

            except Exception as e:
                self.gui_button_remove(puppet)
                self.lbl_append(puppet,f"Experiment raised an error: {e}")
                self.ssh_cancel_command(puppet)

        elif not all([self.entry_puppet.get(), self.entry_mouse.get(), self.entry_exp.get()]): # if exp. is not already runing but input is missing
            self.warning("Please enter a valid mouse name, setup ID and experiment name.")

        else: # A tab is already opened for this puppet (exp. running or not finished yet)
            self.warning(f"WARNING! An experiment is already running on {self.entry_puppet.get()} \n\nPlease select a different puppet.")

    def ssh_run(self,puppet: str):
        """
        Sends a command through SSH to the specified puppet to start running an experiment
        Inputs:
            - puppet: Name of the puppet
        """
        try:
            self.print_config_to_yaml(puppet) # Print config file (parameters of this experiment)
            self.ssh_send_config(puppet) # Send config file to the puppet
            self.ssh_run_command(puppet) # Launch experiment on puppet with config as input
        except Exception as e:
            self.gui_button_remove(puppet) # removes cancel button
            self.lbl_append(puppet,f"Experiment raised an error: {e}") # prints error
            self.ssh_cancel_command(puppet) # Kills all python process on puppet, set status to "canceled" & add finish button
        sys.exit() # exit thread
         
    def print_config_to_yaml(self,puppet: str):
        """
        Prints config file in yaml format. This file includes the necessary parameters to run this experiment.
        Inputs:
            - puppet: Name of the puppet
        """
        if self.status[puppet] == "running":
            dict_to_yaml = {'mouse_name': self.mouse[puppet], 
                            'experiment': self.experiment[puppet],
                            'puppet': puppet,
                            'results': self.puppet_path['results']+self.filename_results[puppet]}
            with open(self.master_path['configs']+self.filename_config[puppet], 'w') as file:
                yaml.dump(dict_to_yaml, file)

    def ssh_send_config(self,puppet: str):
        """
        Sends yaml config file through SSH to puppet
        Inputs:
            - puppet: Name of the puppet
        Raises:
            - ValueError: Raises error if the ssh transfer failed
        """
        if self.status[puppet] == "running":
            self.lbl_append(puppet,"Sending config file...")
            config_puppet = self.puppet_path['configs'] + self.filename_config[puppet]
            config_master = self.master_path['configs'] + self.filename_config[puppet]
            ssh = subprocess.run(["scp", config_master, f"{self.destination[puppet]}:{config_puppet}"],check=False)
            if ssh.returncode != 0:
                raise ValueError(f"Copying config file to {puppet} failed.")
            else:
                self.lbl_append(puppet,"Done.",newline=False)

    def ssh_run_command(self,puppet: str):
        """
        Writes a series of command in a bash file, sends it to the specified puppet through ssh.
        Launches experimenent by runnign the bash file.
        Inputs:
            - puppet: Name of the puppet
        """
        config_puppet = self.puppet_path['configs'] + self.filename_config[puppet]
        bash_puppet = self.puppet_path['bash_files'] + self.bash_file[puppet]
        bash_master = self.master_path['bash_files'] + self.bash_file[puppet]
        
        # Build python command as str
        if self.debug: # debug mode: launch experiment in debug mode
            command = "python -u "+ self.puppet_path['repo'] + 'launch_experiment.py --cfg ' + config_puppet + ' --debug'
        else:
            command = "python -u "+ self.puppet_path['repo'] + 'launch_experiment.py --cfg ' + config_puppet
        # Create bash file
        self.write_sh(puppet,command)
        # Make sure the screensaver activation time is 120 seconds
        if self.status[puppet] == 'running':
            subprocess.run(["ssh", self.destination[puppet], "xset s 120 -display :0.0"],check=True)
        # Send bash file to puppet through ssh 
        if self.status[puppet] == 'running':
            self.lbl_append(puppet,f"Sending bash file to {puppet}...")
            subprocess.run(["scp", bash_master, f"{self.destination[puppet]}:{bash_puppet}"],check=True)
            self.lbl_append(puppet,"Done.",newline=False)
        # Change permission on bash file
        if self.status[puppet] == 'running':
            self.lbl_append(puppet,"Changing permission on bash file...")
            subprocess.run(["ssh", self.destination[puppet], "chmod u+x "+bash_puppet],check=True)
            self.lbl_append(puppet,"Done.",newline=False)
        # Run bash file (to launch experiment)
        if self.status[puppet] == 'running':
            self.lbl_append(puppet,f"Launching experiment on {puppet}...\n")
        if self.status[puppet] == 'running':
            cmd = ["ssh", self.destination[puppet], bash_puppet]
            self.lbl_append(puppet,'EXPERIMENT : '+self.experiment[puppet])
            self.lbl_append(puppet,'--- Last '+str(self.stdout_nlines)+' lines of output --- \n\n')
            popen = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
            # Display experiment output on puppet's tab (on master RPi). Only the last few lines will be shown.
            self.print_stdout(puppet,popen)

    def print_stdout(self,puppet: str,popen):
        """
        While loop that prints process (experiment) output on puppet's tab (on master RPi).
        Only the last few lines will be shown (number of lines specified in init).
        Inputs:
            - puppet: Name of the puppet
            - popen (subprocess.Popen): Ouput/attributes of the command run on the puppet
        """
        l = []
        while popen.poll() is None and self.status[puppet] == 'running':
            txt = popen.stdout.readline().decode()
            if txt != '' and txt != '\n' and 'EXPERIMENT' not in txt:
                l.append(txt)
                l = self.lbl_replace(puppet,l) # Replace n last lines of label with most recent ouput
        popen.stdout.close()

    def ssh_fetch_status(self,puppet: str):
        """
        Fetches the status of the experiment from the puppet every X minutes (defined in init).
        The output "results" file is generated on the puppet only when the experiment is completed, if it encountered an error.
        This method checks every X minutes if the file is generated, and if so, updates the status of the experiment on the master RPi.
        Inputs:
            - puppet: Name of the puppet
        """
        try:
            filename_puppet = self.puppet_path['results'] + self.filename_results[puppet]
            filename_master = self.master_path['results'] + self.filename_results[puppet]
            self.check_exp_duration(puppet) # Check the expected duration of the experiment
            duration = (datetime.datetime.now()-self.t_start[puppet]).seconds/60 # minutes since exp. was launched
            while (puppet in self.t_start) and (duration <= self.exp_duration[puppet]+5) and self.status[puppet] != 'completed' and self.status[puppet] != 'canceled':
                # Fetch "result" (ouput) file
                ssh = subprocess.run(["scp", f"{self.destination[puppet]}:{filename_puppet}", f"{filename_master}"],stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT,check=False)
                if ssh.returncode != 0: # If result file does not exist, wait and try again
                    time.sleep(self.thread_sleep_seconds)
                else: # If result file is found
                    status = self.read_status(puppet) # read status of experiment in the file
                    self.logger.info('status on '+puppet+': '+status)
                    if status == "completed":
                        # time.sleep(2) remove?
                        self.status[puppet] = 'completed'
                        self.gui_button_remove(puppet) # removes cancel button
                        self.lbl_append(puppet,f"Experiment complete! Results are here:\n{self.master_path['results']}{self.filename_results[puppet]}")
                        self.gui_button(puppet,self.master_path['images']+self.img_finish_button,"finish")
                    elif status == "error":
                        # time.sleep(2) remove?
                        self.status[puppet] = 'completed'
                        self.gui_button_remove(puppet) # removes cancel button
                        self.lbl_append(puppet,f"Error raised on puppet.")
                        self.gui_button(puppet,self.master_path['images']+self.img_finish_button,"finish")
            if (puppet in self.t_start) and self.status[puppet] != 'completed' and self.status[puppet] != 'canceled': # if we exceeded max time allowed for this exp.
                self.gui_button_remove(puppet) # removes cancel button
                self.lbl_append(puppet,f"Experiment lasted more than max. duration ({self.exp_duration[puppet]} minutes) without any output file generated.")
                self.ssh_cancel_command(puppet)  # Kills all python process on puppet, set status to "canceled" & add finish button
        except Exception as e:
            self.gui_button_remove(puppet) # removes cancel button
            self.lbl_append(puppet,f"Experiment raised an error: {e}") # prints error
            self.ssh_cancel_command(puppet) # Kills all python process on puppet, set status to "canceled" & add finish button
        sys.exit() # exit thread

# UTILS

    def ssh_cancel_command(self,puppet: str):
        """
        Cancels experiment on specified puppet (kills all python process on puppet, adds finish button to tab)
        Inputs:
            - puppet : Name of the puppet
        """
        self.status[puppet] = 'canceled'
        command = "pkill -9 python "
        self.lbl_append(puppet,f"Killing all python processes on {puppet}...")
        # Activate screensaver (close screen on puppet)
        subprocess.run(["ssh", self.destination[puppet], "xset s activate -display :0.0"],check=False)
        # Send "kill all python process" command
        ssh = subprocess.run(["ssh", self.destination[puppet], command],check=False)
        if ssh.returncode not in [0,1]:
            self.lbl_append(puppet,"Failed. Please restart puppet.",newline=False)
        else:
            self.lbl_append(puppet,'Done.',newline=False)
        self.gui_button_remove(puppet) # removes cancel button
        self.gui_button(puppet,self.master_path['images']+self.img_finish_button,"finish") # Add finish button

    def read_experiments_yaml(self) -> List:
        """
        Reads yaml file with list of available experiments.
        Returns:
            - exps['experiments']: list of experiments (list of strings)
        """
        with open(self.master_path['repo'] + self.experiments_filename, 'r') as file:
            exps = yaml.safe_load(file)
        return exps['experiments']

    def read_puppets(self):
        """
        Reads list of available puppets (RPi name + hostname) and save as attribute
        """
        file = open(self.master_path['repo'] + self.puppets_info_filename)
        csvreader = csv.reader(file)
        for row in csvreader:
            self.destination[row[0]] = row[1] + "@" +row[2]

    def remove_puppet_from_current(self,puppet: str):
        """
        Closes tab associated with specified puppet + removes all key/values associated with this puppet in attributes
        Args:
            puppet: Name of the puppet
        """
        # Close tab
        self.tabControl.forget(self.tab[puppet])
        # Activate screensaver (close screen on puppet)
        subprocess.run(["ssh", self.destination[puppet], "xset s activate -display :0.0"],check=False)
        # Loop all attributes in self and remove entries with the name of the puppet
        for attr in self.__dict__:
            val = getattr(self,attr)
            if type(val) is dict and puppet in val and attr != "destination":
                self.__dict__[attr].pop(puppet,None)
        # Debug : list threads
        for thread in threading.enumerate(): 
            self.logger.debug(thread.name)  

    def warning(self,message: str):
        """
        Shows a warning in "pop-up" window
        Inputs:
            - message: String to be shown in pop-up warning
        """
        popup = Tk()
        lbl1_popup = Label(popup, text=f"{message}",wraplength=500, justify="center",font=("Arial",12))
        lbl1_popup.place(x=50,y=50)
        popup.title("WARNING")
        popup.geometry("600x350+100+30")
        popup.mainloop()

    def write_sh(self,puppet: str,command: str):
        """
        Writes executable bash file with the following lines:
        - cd to the correct folder
        - activate the "souris" environment
        - python command (to launch exp. on puppet)
        Inputs:
            - puppet: Name of the puppet
            - command: python command that will launch the experiment on puppet (to write in bash file)
        """
        file = open(self.master_path['bash_files'] + self.bash_file[puppet], "w")
        file.write("# "+self.bash_file[puppet])
        file.write("\ncd " + self.puppet_path['repo'])
        file.write("\nsource /home/pi/miniconda3/bin/activate souris")
        file.write("\n"+command)
        file.close()

    def lbl_append(self,puppet: str, string: str, newline: bool=True):
        """
        Append string to text on puppet's tab.
        Inputs:
            - puppet: Name of the puppet
            - string: string to append to label
            - newline: If true, str will be added as a new line. Defaults to True.
        """
        self.logger.info(puppet+': '+string)
        if newline:
            string = '\n'+string
        else:
            string = ' '+string
        text = self.lbl_tabs[puppet].cget("text") + string
        self.lbl_tabs[puppet].configure(text=text)

    def lbl_replace(self, puppet: str, string: str) -> str:
        """
        Updates the last lines of text in the puppet's tab with new lines.
        Used to show the last X lines of output (X can be defined in init)
        Inputs:
            - puppet: Name of the puppet
            - string: str to use to replace old string
        Returns:
            - str: updated string (complete text on puppet's tab)
        """
        self.logger.info(puppet+': '+string[-1])
        text = self.lbl_tabs[puppet].cget("text")
        pos = text.find(string[0])
        text = text[:pos]
        if len(string) > self.stdout_nlines:
            string = string[-self.stdout_nlines:]
        for str in string:
            text = text + str
        self.lbl_tabs[puppet].configure(text=text)
        return string

    def get_gui_input(self) -> str:
        """
        Get the input information in the GUI and saves it as attributes
        Raises:
            - ValueError: error raised if input information is missing (mouse name, exp. name, puppet name..)
        Returns:
            - str: name of the puppet
        """
        puppet = self.entry_puppet.get()
        self.mouse[puppet] = self.entry_mouse.get()
        self.experiment[puppet] = self.entry_exp.get()
        if self.mouse[puppet] == '' or self.experiment[puppet] == '' or puppet == '':
            raise ValueError("Please enter a valid mouse name, setup ID and experiment name.")
        return puppet

    def create_new_tab(self, puppet: str):
        """
        Creates new tab for the specified puppet
        Inputs:
            - puppet: Name of the puppet 
        """
        self.tab[puppet] = Frame(self.tabControl)
        self.gui_set_background(puppet)
        self.canvas = Canvas(self.tab[puppet],width=700,height=280,highlightthickness=2, highlightbackground="#3b607d")
        self.canvas.place(x=50,y=50)
        self.tabControl.add(self.tab[puppet], text = puppet)
        self.lbl_tabs[puppet] = Label(self.tab[puppet], text=f"{puppet} - Starting experiment: {self.experiment[puppet]}\n",justify="left",font=("Arial",10),wraplength=700)
        self.lbl_tabs[puppet].place(x=52,y=52)
        self.tabControl.select(self.tab[puppet])
        self.tabControl.pack(expand = 1, fill ="both")

    def create_filenames(self, puppet: str):
        """
        Builds str for different filenames that will be useful
        Inputs:
            - puppet: Name of the puppet
        """
        t = self.t_start[puppet].strftime("%Y-%m-%dT%H%M%S")
        self.filename_config[puppet] = t + "_" + puppet.replace(" ","-") + "_" + self.experiment[puppet].replace(" ","-") + "_" + self.mouse[puppet].replace(" ","-") + "_config.yaml"
        self.filename_results[puppet] = self.filename_config[puppet].replace('_config','_results')
        self.bash_file[puppet] = puppet.replace(" ","_")+".sh"

    def add_rel_path(self, string: str):
        """
        Creates complete paths that will be useful and creates folders if they don't exist
        Inputs:
            - string: name of the folder
        """
        self.puppet_path[string] = self.puppet_path['repo'] + string + "/"
        self.master_path[string] = self.master_path['repo'] + string + "/"
        if not os.path.exists(self.master_path[string]):
            os.mkdir(self.master_path[string])

    def read_status(self, puppet: str) -> str:
        """
        Checks the status of the experiment in the yaml file.
        Inputs:
            - puppet: Name of the puppet
        Returns:
            - str: status
        """
        with open(self.master_path['results'] + self.filename_results[puppet], 'r') as file:
            out = yaml.safe_load(file)
        return out['status']

    def check_exp_duration(self, puppet: str):
        """
        Finds the the duration in the exp. file for the specified experiment.
        This will define the max. acceptable time to run the experiment (will cancel the run if it exceeds this value)
        Inputs:
            - puppet: Name of the puppet
        """
        exp_file = self.experiment[puppet].lower()
        str = 'duration_minutes='
        files = os.listdir(self.master_path['experiments'])
        found = False
        for f in files:
            if f.replace('.py','').lower() == exp_file:
                found = True
                with open(self.master_path['experiments']+f) as file:
                    file_str = file.read()
                    if str in file_str:
                        pos = file_str.find(str)
                        split = file_str[pos:].split(',')
                        minutes = float(split[0].replace(str,'').replace(' ',''))
                        self.exp_duration[puppet] = minutes

        if not found:
            self.exp_duration[puppet] = self.thread_max_time

    def set_logger(self,name: str, debug: bool=False):
        """
        Initialize Logger
        Inputs:
            - name: logger name
            - debug: run in debug mode. Defaults to False.
        """
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',"%Y-%m-%d %H:%M:%S")
		# set logger
        self.logger = logging.getLogger(name+'-log')
        self.logger.setLevel(logging.DEBUG)
		# console output
        self.ch = logging.StreamHandler()
        if debug:
            self.ch.setLevel(logging.DEBUG)
        else:
            self.ch.setLevel(logging.INFO)
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.ch)
    
    def ssh_keep_screen_active(self, puppet: str):
        """
        Pokes the puppet every X seconds to prevent the screen from going to screensaver during the experiment.
        Inputs:
            - puppet: Name of the puppet
        """
        try:
            time.sleep(self.screen_activation_wait_time) # wait a few seconds before waking up the sreen when launching exp.
            i = 1
            while puppet in self.status and self.status[puppet] == 'running':
                if i % self.poke_screen_seconds == 0:
                    time.sleep(1)
                    subprocess.run(["ssh", self.destination[puppet], "xset s reset -display :0.0"])
                i += 1
        except Exception as e:
            self.lbl_append(puppet,f"Experiment raised an non fatal error: {e}")
        sys.exit()


if __name__ == "__main__":
    myWin = MasterGUI()