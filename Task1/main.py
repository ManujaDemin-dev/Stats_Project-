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
            "Run",
            "Hits",
            "Total_Throws",
            "Hit_Probability",
            "Pi_Estimate",
            "Absolute_Error",
            "Execution_Time(ms)",
        ]
    )
    experiment_id = 1
    row_index = 0
    
    for n in args.n:
        print(f"\nRunning simulations for N={n} with {args.runs} runs...")
        
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
                
                print(f"Completed Run {run}/{args.runs} for N={n})")
                
            except Exception as e:
                print(f"Run {run} for N={n} failed with error: {e}")
                
    #Summary Statistics Calculations
    
    summary_df = df.groupby("N").agg(
        Mean_Pi=("Pi_Estimate", "mean"),
        Mode_Pi=("Pi_Estimate", lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan),
        Mean_Absolute_Error=("Absolute_Error", "mean"),
        Avg_Execution_Time_ms=("Execution_Time(ms)", "mean")
    ).reset_index()
    
    #Save Results to Excel
    
    timestamp = int(time.time())
    filename = f"MonteCarloSim_Results_{timestamp}.xlsx"

    try:
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Detailed_Logs", index=False)
            
            summary_df.to_excel(writer, sheet_name="Summary_Statistics", index=False)

            for sheet in writer.sheets.values():
                for col in sheet.columns:
                    max_length = 0
                    column = col[0].column_letter
                    for cell in col:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    sheet.column_dimensions[column].width = max_length + 2

        print(f"\n[SUCCESS] Excel workbook saved: {filename}")

    except Exception as e:
        print(f"\n[ERROR] Failed to save Excel file: {e}")
    
    # Convergence Plot    
    
    if not args.no_plot:
        plt.figure(figsize=(10, 6))

        plt.plot(
            summary_df["N"],
            summary_df["Mean_Pi"],
            marker="o",
            linewidth=2,
            label="Estimated π (Mean)"
        )
        
        plt.axhline(
            np.pi,
            linestyle="--",
            linewidth=2,
            label=f"Actual π ({round(np.pi, 5)})"
        )

        plt.xscale("log")
        plt.xlabel("Number of Dart Throws (N)")
        plt.ylabel("Estimated Value of π")
        plt.title("Monte Carlo Simulation: Convergence of π Estimate")
        plt.legend()
        plt.grid(True, which="both", alpha=0.5)
        
        final_n = summary_df["N"].iloc[-1]
        final_val = summary_df["Mean_Pi"].iloc[-1]
        plt.annotate(
            f"Final Estimate: {round(final_val, 4)}",
            xy=(final_n, final_val),
            xytext=(final_n * 0.6, final_val + 0.01),
            arrowprops=dict(arrowstyle="->")
        )
    
        plt.tight_layout()
        plot_filename = f"Pi_Convergence_{timestamp}.png"
        plt.savefig(plot_filename)
        print(f"[SUCCESS] Plot saved as: {plot_filename}")

        plt.show()

        
if __name__ == "__main__":
    main()