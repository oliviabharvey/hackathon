#!/usr/bin/env python3

import argparse
import yaml

from exp1B import Experiment1B

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
    
    my_exp = Experiment1B()
    my_exp.run_experiment()

    return


if __name__ == "__main__":
    # args = parse_args()
    # with open(args.cfg, 'r') as f:
    #     cfg = yaml.load(f, Loader=yaml.Loader)

    main()