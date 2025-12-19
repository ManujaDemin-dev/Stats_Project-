# importing all necessary libraries

import argparse 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time 
from openpyxl.utils import get_column_letter

# Core simulation function

def estimate_pi(n):

    x_axis = np.random.uniform(0, 1, n)
    y_axis = np.random.uniform(0, 1, n)

    inside_circle = (x_axis**2 + y_axis**2) <= 1
    hits = inside_circle.sum()

    hit_probability = hits / n
    pi_estimate = hit_probability * 4
    absolute_error = abs(np.pi - pi_estimate)

    return hits, hit_probability, pi_estimate, absolute_error

# Implementation of the command line arguments parser 

def parse_arguments():
    
    parser = argparse.ArgumentParser(
        description=("Monte Carlo Simulation to estimate the value of Pi using a dart-throwing method.\n"
                     "Generates Excel logs and convergence plots. \n"
                     "Example usage: python MonteCarloSim_Improved.py --n 1000 10000 100000 1000000 --runs 10 \n"
                     "Required libraries: numpy, pandas, matplotlib, openpyxl"
        )
    )

    parser.add_argument(
        "--n",
        nargs= "+",
        type=int,
        required=True,
        help="List of Dart throws (e.g. 1000 10000 100000 1000000)"
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=10,
        help="Number of repetitions for each N (Default 10)"
    )

    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Disable plotting of results"
    )

    return parser.parse_args()