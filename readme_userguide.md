# User Guide

This document will guide the user to run one or more experiments, step by step.

Please note the following terms that will be used throughout this guide:

- **Master RPi**: The RPi used as main console. This RPi will be used to launch expriments on the other RPis.
- **Puppet RPi**: RPi plugged into the physical setup (screen, motor, lights, etc.). The experience will be run on this RPi. Multiple **Puppet RPis** can be connected to the **Master RPi**.

## How to run an experiment

### 1) Make sure the setup is ready to be used

* Check that all RPis (Master and puppets) are plugged in (power source)
* Check that all RPis are connected to the Ethernet Switch (via Ethernet cable)
* Check that the pysical setup of each puppet (box, screen, motor, lights, etc.) are correclty installed and plugged in to the RPi

### 2) Launch the Graphical User Interface (GUI) on the Master RPi

1. Touch the screen of the Master RPi to deactivate the screensaver (if in screensaving mode)
2. Open the **Terminal**
3. Type the followind command: `./run_GUI.sh` (you should by default already be in the `/home/pi/` folder)
4. The GUI will launch

![](https://github.com/oliviabharvey/hackathon/blob/master/images_for_readme/empty.png)

### 3) Test the equipment on a specific **Puppet RPi**

### 4) Run an experiment on a specific **Puppet RPi**

*Note: Please refrain from using special characters in any field (é, à, %, $, etc.)*

1. Fill in the `Name of the mouse` field.

![](https://github.com/oliviabharvey/hackathon/blob/master/images_for_readme/Name.png)

2. Select the puppet on which you want to run the experiment in the `Puppet ID` field.

![](https://github.com/oliviabharvey/hackathon/blob/master/images_for_readme/puppet.png)

3. Select a sequence of experiments in the `Sequence to run` field.

    **Sequences** are predefined lists of experiments (that can be in a specific suggested order) to help the user in the selection of the experiments. This only affects the experiments shown in the dropdown menu on the GUI. The specific sequence named `All Experiments` should always include all available experiments.

    It is possible to modify this list to create new sequences or add new experiments to the dropdown menu by modifying the [sequences.yaml](https://github.com/oliviabharvey/hackathon/blob/master/sequences.yaml) file (see instructions in [section below](https://github.com/oliviabharvey/hackathon/blob/master/readme_userguide.md#how-to-update-the-experiment-sequences)).



![](https://github.com/oliviabharvey/hackathon/blob/master/images_for_readme/exp_all.png)



## How to update the experiment sequences

Here is an example of what the [sequence.yaml](https://github.com/oliviabharvey/hackathon/blob/master/sequences.yaml) can look like this:

```
Check Components:
 Check: CheckComponents
Perseverence:
 1: Exp1a
 2: Exp1B
 3: Exp2
 4: Exp3
Other Sequence:
 1: Exp3
 2: Exp4
 3: Exp5
 4: Prl1
All experiments:
 a: Exp1A
 b: Exp1B
 c: Exp2
 d: Exp3
 e: Exp4
 f: Exp5
 g: Prl1
```

A sequence is simply a list of experiment to filter through all the available experiment in the GUI.

* The sequence "Check Components" should always stay in the file.
* The sequence "All experiments" should also always stay in the file and include all available experiments.
* You can add any number of sequences in the file, as long as you respect the yaml formatting, and they will appear in the GUI at the next launch. For example:

```
New Sequence:
 1: Exp5
 2: Exp4
 3: Exp3
```

## How to reinstall or add a puppet

An ISO image of both the puppet RPI and Master RaspberryPi can be found [here]().

For both RPI types (puppet and master), the process is the same. 

1. Insert you microSD car into your PC using a microSD card reader.
2. Download ([here](https://www.raspberrypi.com/software/)) and install Rasperry Pi Imager.
3. Launch Raspberry Pi Manager on your PC.
4. Under "Operating System", select "Use Custom", select your *.img.gz* file.
5. Select the microSD card you wish to burn it to (the one you just inserted in your PC).
6. Click "write".
7. Once the process is done, eject the microSD.
8. Insert the microSD into your RPI (it has to be connected to a RPI screen).
9. Turn on the RPI. Note that if any password is required throughout the process, use "raspberry".
10. Open a command window in the RPI
11. Enter the following command to activate your environment: `source activate souris`
12. Enter the following command to go the the github folder 
    * For a puppet RPI: `cd hackathon_souris/`
    * For a master RPI: `cd hackathon/`
14. Enter the following command to pull the most recent scripts from gitgub `git pull` (this is important if changes are made to the github scripts after 2022/04/20, since this is the date when the ISO image was created).
15. Your new RPI (puppet or master) is good to go!

