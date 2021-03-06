#!/usr/bin/env python3

import argparse
import yaml

from experiments.exp1A import Exp1A
from experiments.exp1B import Exp1B
from experiments.exp2 import Exp2
from experiments.exp3 import Exp3
from experiments.exp4 import Exp4
from experiments.exp5 import Exp5
from experiments.prl1 import Prl1
from experiments.check_components import CheckComponents

def parse_args():
    """
    Parser for the command line arguments.

    Returns
    -------
    args : Namespace
        The arguments.
    """

    parser = argparse.ArgumentParser(description="Launch Experiment")
    parser.add_argument('--cfg',
                        type=str,
                        required=False,
                        default='example.config.yaml',
                        help="Path to config file containing the experiment definition.")

    parser.add_argument('--debug', # add the --debug arg to launch the experiment in debug mode
                        action="store_true",
                        help="Whether to launch script in debug mode - auto click.")
    return parser.parse_args()

def main(cfg, debug): 
    """
    Main function to start the experiment.

    """
    print(f"\n --- EXPERIMENT {cfg['experiment'].upper()} ON MOUSE {cfg['mouse_name'].upper()} ---\n")
    Experiment = eval(f"{cfg['experiment']}")
    my_exp = Experiment(cfg=cfg, duration_minutes=2, debug=debug, enableAutoClick=debug)
    my_exp.run_experiment()
    return


"""
When calling lauch_experiment.py directly, the code reads the command line arguments,
reads the yaml config file, and from there, run the main script.
"""
if __name__ == "__main__":
    args = parse_args()
    with open(args.cfg, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.Loader)

    main(cfg=cfg, debug=args.debug)