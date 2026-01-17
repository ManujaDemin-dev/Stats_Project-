import sys
from fileinput import filename
import pandas as pd
import random
import argparse as ap
from Simulator import plot
import openpyxl as xl
from datetime import datetime
from exact_probability import cal_exact_probability



def main():
    try:
        parser = ap.ArgumentParser(description="Dice Monte Carlo Simulation")
        parser.add_argument("--NUM_OF_DICE" ,type=int,default=10, help="Enter the number of dice (default: 10)")
        parser.add_argument("--NUM_OF_Trials", type=int, default=500, help="Enter the number of Trials (default:500)")

        args = parser.parse_args()

        if args.NUM_OF_DICE <= 0 or args.NUM_OF_Trials <= 0:
            raise ValueError("Number of dice and number of trials must be positive integers.")

        No_of_dice = args.NUM_OF_DICE
        Trials = args.NUM_OF_Trials
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Dice_Simulation_Results_{timestamp}.xlsx"

        favorable_count = cal_exact_probability(32, No_of_dice)
        total_outcomes = 6 ** No_of_dice
        exact_probability_value = favorable_count / total_outcomes


        #implementing a dynamic way to calculate exact probability
        print("Exact Probability Calculation: \n")
        print(f"Exact favourable (sum = 32 combinations) : {favorable_count}")
        print(f"Total Outcomes (6^^num_of_dice({No_of_dice})) : {total_outcomes}")
        print(f"Exact Probability : {exact_probability_value:.8f} \n")



        TRIALS = []

        for i in range(Trials):
            roll_the_dice = [random.randint(1,6) for j in range(No_of_dice)]
            TRIALS.append(roll_the_dice)

        
        Dice_data = pd.DataFrame(
            TRIALS,
            columns=[f"Dice {i}" for i in range(1,No_of_dice + 1)]
        )

        Dice_data["Sum"] = Dice_data.sum(axis=1)

        stact_df = pd.DataFrame({
            "Statistic" : ["Mean", "Median", "Mode", "Max", "Min"],
            "value" : [
                Dice_data["Sum"].mean(),
                Dice_data["Sum"].median(),
                Dice_data["Sum"].mode()[0],
                Dice_data["Sum"].max(),
                Dice_data["Sum"].min()
            ]
        })

        Count_32 = (Dice_data["Sum"] == 32).sum()

        Dice_data['Is_Sum_32'] = Dice_data['Sum'] == 32

        probability_extimated = Count_32 / Trials

        #show the results

        print("Simulation Results : \n")
        print(f"Trials : {Trials}")
        print(f"Favourable outcomes (Sum = 32) : {Count_32}")
        print(f"Estimated Probability : {probability_extimated:.7f} ")
        print(f"Estimated probability in prcentage : {Count_32*100/Trials} %")

        print("\n")
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                Dice_data.to_excel(writer, sheet_name='Simulation_Data', index=False)
                stact_df.to_excel(writer, sheet_name='Summary', index=False)
        except PermissionError:
            print(f"Permission denied: Unable to write to file '{filename}'. Please close the file if it is open and try again.")
            sys.exit(1)

        print(probability_extimated)

        print("This is the head of the Dice DataFrame: Check the excel file for complete data")

        print(Dice_data.head())


        plot(Trials, probability_extimated , exact_probability_value)

    except ImportError as e:
            print(f"Import Error: {e}")

    except ValueError as e:
            print(f"Input  Error: {e}")
        
    except ZeroDivisionError as e:
            print(f"Math Error:Division by zero occured.")
        
    except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
    finally:
            print("Simulation Successfully executed.")

if __name__ == "__main__":
        main()