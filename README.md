# Setup
## **On Ubuntu**

### **Required**
* Raspberry Pi with power cable
* Ethernet cable
* SD card

### **Install Rasberry Pi OS Lite**
This version of the OS does not have a GUI and will require that we interface with the pi with the command line. The good news is that we will use our IDE (i.e. VS Code) on our laptop and remotely connect to the pi via VS Code.

* Insert SD card in card reader and format card in FAT format.
* Write the Raspberry Pi OS Lite on the SD card using the [Imager tool](https://www.raspberrypi.com/software/). This will create two compartments (rootfs and boot)
* Go to boot folder and add an empty file called ssh, without extension:  `touch media/<user>/boot/ssh`
  - For Windows, create the same empty file named `ssh` in your removable device under the `boot` folder.
* Eject rootfs folder, insert sd card in pi but do not plug in pi nor the ethernet cable yet. 
* Go to Settings/Network/Wired. In the options, go to IPV4 and set the default to `shared to other computers`
  - For Windows go to Control Panel/Network and Sharing/Network, Select your WiFi connection/Properties/Sharing and select `Allow other network to connect through this computer's Internet connection` and select your Ethernet connection in the dropdown below.
* Plug ethernet cable in both laptop and pi, then plug in power in pi.
* Reboot computer
* Launch terminal (Powershell for Windows) and use `ping raspberrypi.local` to get static ip of pi. 
* ssh into pi using `ssh pi@<ip address of pi>` or use `ssh pi@raspberrypi.local`
* input password : `raspberry`

Congrats! Now you can ssh into your pi via ethernet!

### **Install VS Code**
Install [VS Code](https://code.visualstudio.com/Download?WT.mc_id=academic-11397-jabenn).

### **Configure Remote Development in VS Code**
* From inside VS Code, select the Extensions tab from the sidebar and install `Python Extention` and `Remote developement Extention`. 
* Launch the command palette using ctrl+shift+P, select `Remote SSH: Connect current window to host`, enter `pi@<addres of pi>`, then enter password: `raspberry`

Congrats! Now your VS Code IDE is remotely linked to your pi. You can launch a terminal from there, or you can access the project repo and start coding! You will eventually also be able to launch your scripts and troubleshoot code as well. 

### **Install Anaconda**
* `wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh`
  - For Windows, download `http://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe`
* `sudo /bin/bash Miniconda3-latest-Linux-armv7l.sh`
  - For Widowns, Install `Miniconda3-latest-Windows-x86_64.exe`
* Accept the license agreement with yes
* When asked, change the install location: `/home/pi/miniconda3`
  - For Windows, select all users and keep default folder `C:\ProgramData\Miniconda3`
* Do you wish the installer to prepend the Miniconda3 install location... answer yes
* Now add the install path to the PATH variable: `sudo nano /home/pi/.bashrc`. Go to the end of the file .bashrc and add the following line: `export PATH="/home/pi/miniconda3/bin:$PATH"`
  - For Windows, Select `Add Miniconda3 to system PATH environment variable`
* Save the file and exit with ctrl+X then yes then enter. 
* `source /home/pi/.bashrc`

## Path and update your pi
* `sudo apt-get update`
* `sudo apt-get upgrade`
