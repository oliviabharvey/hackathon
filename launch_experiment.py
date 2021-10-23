#!/usr/bin/env python3

import argparse
import yaml

from experiments.exp1A import Experiment1A
from experiments.exp1B import Experiment1B
from experiments.exp2 import Experiment2
from experiments.exp3 import Experiment3
from experiments.exp4 import Experiment4

# def parse_args():
#     """
#     Parser for the command line arguments.

#     Returns
#     -------
#     args : Namespace
#         The arguments.
#     """

#     parser = argparse.ArgumentParser(description="Launch Experiment")
#     parser.add_argument('--cfg',
#                         type=str,
#                         required=True,
#                         help="Path to config file containing all experiment definitions.")
#     return parser.parse_args()

def main(): 
    
    my_exp = Experiment4(duration_minutes=1)
    my_exp.run_experiment()

    return


if __name__ == "__main__":
    # args = parse_args()
    # with open(args.cfg, 'r') as f:
    #     cfg = yaml.load(f, Loader=yaml.Loader)

    main()