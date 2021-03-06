# AUTOMATED COGNITIVE EXPERIMENTS

The [user guide](https://github.com/oliviabharvey/hackathon/blob/master/readme_userguide.md) explains how to run the experiments.

The [code development readme](https://github.com/oliviabharvey/hackathon/blob/master/readme_development_environment.md) explains how the code is structured.

The [hardware readme](https://github.com/oliviabharvey/hackathon/tree/master/hardware/readme_hardware.md) explains the circuits and how hardware is connected.

## Project Overview
This repository contains code that can create automated cognitive experiments used for mice, it was financed by the Rossignol Laboratory.

The goal of this project is to be able to automatically run cognitive experiments on mice. The project is coded in Python and uses Raspberrypis to launch and run the experiments. All of the necessary code is available in this repository. Further experiments can be added to the list of experiments, as it stands at the moment, we have one complete experiment: probabilistic reversal learning (also known as Prl1). All of the experiment preparations step are listed as (exp1A, exp1B, etc.). Those experiments are the preparations for any of the "real" experimentation. The present architecture of the code allows users to add new experiments if they wish to. More details on that end are provided in the [code development readme](https://github.com/oliviabharvey/hackathon/blob/master/readme_development_environment.md) and within the code itself where we have commented our steps.

An experiment can be launched from the master RaspberryPi onto any puppet RaspberryPi. More details are provided in the [user guide](https://github.com/oliviabharvey/hackathon/blob/master/readme_userguide.md) section. It details how to properly setup an experiment. Also, if you want to add a new RaspberryPi as a puppet, follow the section detailed [here](https://github.com/oliviabharvey/hackathon/blob/master/readme_userguide.md#how-to-reinstall-or-setup-a-new-masterpuppet-rpi).
