# High level overview of the code

### **1) Interaction between the GUI and the experiment launching**

When the user selects an experiment with the GUI, launch_experiment.py is called. This script takes as input
a config file (example.config.yaml) that holds the details of the experiment. For example, it contains the nature of the experiment (example: exp4). 
An object of type Experiment is then instantiated and launched from the GUI.

All experiments are a subclass of the class BaseExperiment located in base_exp.py. In order to understand better how this program works, let's dive a little into the workflow.

The BaseExperiment class is a template for all the possible experiments. This template contains a great number of methods that are useful for all different experiments. Depending on the actual task, an experiment will select any of the following:
  - Run experiment
  - Initialize
  - Deliver sequence
  - Tray light on
  - play tone
  - deliver food
  - is completed
  - on infrared break
  - tray light off
  - ...

Any experiment is based on the BaseExperiment class and so will inherit all of these methods as well as specific method per experiment. When the function launch_experiment.py is used, run_experiment() is called. This function initializes the whole experiment. It starts the timer, it adjusts the status of the experiment to running and it turns the light on to indicate that the experiment is indeed running. It will wait for the status to be completed and once the experiment is done, the results will be saved inside a yaml file. The GUI will indicate where the results are saved so that you can look at them.

### **2) Experiments setup**

Any experience starts with Box Habituation <br />

#### Box Habituation <br />
 1: Exp1A --> black screen <br />
 2: Exp1B --> familiarize with food tray <br /> 
 3: Exp2 --> familiarize with touchscreen <br /> 
 4: Exp3 --> press the good square to obtain food, otherwise nothing happens <br />
 5 Exp4 --> press the good square to obtain food, otherwise punishment happens <br />

#### Perseverence 
- 1: Exp5: deterministic reversal learning: There is always two squares, the left one is always the good square.
- 2: Prl1: 80% of the time, the good square will be on side X, the other 20% will be on side Y.

#### Create a new experiment
If one wishes to create a new experiment, the code should be added in the [experiments](https://github.com/oliviabharvey/hackathon/tree/master/experiments) section of the code. One should use the BaseExperiment class (base_exp.py) as template for any new addition.
