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

    **Sequences** are predefined lists of experiments (that can be in a specific suggested order) to help the user in the selection of the experiments. This only affects the experiments shown in the dropdown menu on the GUI. The specific sequence names `All Experiments` should always include all available experiments.

    It is possible to modify this list to create new sequences or add new experiments to the dropdown menu by modifying the [sequences.yaml](https://github.com/oliviabharvey/hackathon/blob/master/sequences.yaml) file (see instructions in [section below](https://github.com/oliviabharvey/hackathon/blob/master/readme_userguide.md#how-to-update-the-experiment-sequences)).



![](https://github.com/oliviabharvey/hackathon/blob/master/images_for_readme/exp_all.png)



## How to update the experiment sequences

## How to reinstall or add a puppet

inital setup: connecter le master aux RPIs
copie ISO (master & puppet) (noter comment refaire une copie iso au besoin)
git pull pour les mettre à jour