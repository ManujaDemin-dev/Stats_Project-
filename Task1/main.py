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

#Input Validation Implementation to Prevent Invalid inputs and Exceptions 

def validate_inputs(ns, runs):
    if runs <= 0:
        raise ValueError("Number of runs must be a positive integer.")
    
    for n in ns:
        if n <= 0:
            raise ValueError("All N values must be positive integers.")
        
    min_N = 100
    max_N = 10000000
    for n in ns:

        if n<=0:
            raise ValueError("All N values must be positive integers.")
        if n < min_N:
            raise ValueError(f"N value {n} is too small. Minimum is {min_N}.")
        if n > max_N:
            raise ValueError(f"N value {n} is too large. Maximum is {max_N}.")
        
    try:
        test_filename = "permission_test.xlsx"
        test_df = pd.DataFrame({"Test": [1, 2, 3]})
        
        with pd.ExcelWriter(test_filename, engine="openpyxl") as writer:
            test_df.to_excel(writer, index=False)
    except PermissionError:
        raise PermissionError("No permission to write Excel files in the current directory.")
    
    if len(ns) != len(set(ns)):
        raise ValueError("Duplicate N values are not allowed.")

#Main Function

def main():
    args = parse_arguments()
    validate_inputs(args.n,args.runs)
    
    df = pd.DataFrame(
        columns=[
            "Experiment_ID",
            "N",
            "Hits",
            "Total_Throws",
            "Hit_Probability",
            "Pi_Estimate",
            "Absolute_Error",
            "Execution_Time(s)",
        ]
    )
    experiment_id = 1
    row_index = 0
    
    for n in args.n:
        print(f"\nRunning simulations for N={n} with {args.runs} runs...")
        start_n_time = time.time()
        
        for run in range(1,args.runs +1 ):
            try:
                run_start_time = time.time()
                hits,prob,pi_est,eror = estimate_pi(n)
                run_time_ms =(time.time() - run_start_time) * 1000
                
                df.loc[row_index] = [
                    experiment_id,
                    n,
                    run,
                    hits,
                    n,
                    prob,
                    pi_est,
                    eror,
                    round(run_time_ms,3),
                    
                ]
                
                row_index += 1
                experiment_id += 1
                
            except Exception as e:
                print(f"\nMonte Carlo Simulation Completed successfully for N={n} with {args.runs} runs.")
                print(f"Total Experiments Executed: {len(df)}")
                print(df.head())
                
                