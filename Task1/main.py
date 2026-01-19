# importing all necessary libraries

import argparse 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time 
from openpyxl.utils import get_column_letter

# Core simulation function

def estimate_pi(n):

    x_axis = np.random.uniform(-1, 1, n)
    y_axis = np.random.uniform(-1, 1, n)

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
    
    if len(ns) != len(set(ns)):
        raise ValueError("Duplicate N values are not allowed.")

#Main Function

def main():
    args = parse_arguments()
    validate_inputs(args.n,args.runs)
    
    all_results = []
    timestamp = int(time.time())
    filename = f"MonteCarloSim_Results_{timestamp}.xlsx"

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:

        for n in args.n:
            print(f"\nRunning simulations for N = {n} with {args.runs} runs...")

            df = pd.DataFrame(
                columns=[
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
        
            for run in range(1,args.runs + 1):
                try:
                    run_start_time = time.time()
                
                    hits, prob, pi_est, error = estimate_pi(n)
                    run_time_ms =(time.time() - run_start_time) * 1000
                    
                    row = [
                        n,
                        run,
                        hits,
                        n,
                        prob,
                        pi_est,
                        error,
                        round(run_time_ms, 3),
                    ]
                    
                    df.loc[len(df)] = row
                    all_results.append(row)
                    
                    print(f"Completed Run {run}/{args.runs} for N={n})")
                
                except Exception as e:
                    print(f"Run {run} for N={n} failed with error: {e}")

            #Writing N per sheet
            sheet_name = f"N_{n}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            ws = writer.sheets[sheet_name]
            ws.freeze_panes = "A2"

            for i, col in enumerate(ws.columns, start=1):
                max_length = max(len(str(cell.value)) for cell in col if cell.value is not None)
                ws.column_dimensions[get_column_letter(i)].width = max_length + 2
                
        #Summary Statistics Calculations
        df_all = pd.DataFrame(
            all_results,
            columns=[
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

        summary_df = df_all.groupby("N").agg(
            Mean_Pi=("Pi_Estimate", "mean"),
            Mode_Pi=("Pi_Estimate", lambda x: x.mode().iloc[0]),
            Mean_Absolute_Error=("Absolute_Error", "mean"),
            Avg_Execution_Time_ms=("Execution_Time(ms)", "mean")
        ).reset_index()

        #Save Results to Excel
        summary_df.to_excel(writer, sheet_name="Summary_Statistics", index=False)

        ws = writer.sheets["Summary_Statistics"]
        ws.freeze_panes = "A2"

        for i, col in enumerate(ws.columns, start=1):
            max_length = max(len(str(cell.value)) for cell in col if cell.value is not None)
            ws.column_dimensions[get_column_letter(i)].width = max_length + 2
    
    print(f"\nExcel Results saved to {filename}")

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
            color="red",
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
            xycoords="data",
            xytext=(-40, 30),
            textcoords="offset points",
            arrowprops=dict(arrowstyle="->"),
            ha="right"
        )
    
        plt.tight_layout()
        plot_filename = f"Pi_Convergence_{timestamp}.png"
        plt.savefig(plot_filename)
        print(f"[SUCCESS] Plot saved as: {plot_filename}")

        plt.show()

        
if __name__ == "__main__":
    main()