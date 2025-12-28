import pandas as pd
import random
import argparse as ap
from Simulator import plot
import openpyxl as xl

Value =0.06287

if __name__ == "__main__":
    print("Hellow !")

    parser = ap.ArgumentParser()
    parser.add_argument("--NUM_OF_DICE" , help="Enter the number of dice")
    parser.add_argument("--NUM_OF_Trials", help="Enter the number of Trials")
    args = parser.parse_args()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Dice_Simulation_Results_{timestamp}.xlsx"

    a = args.NUM_OF_DICE
    b = args.NUM_OF_Trials

    if a == None and b == None:
        No_of_dice = 10
        Trials = 500

        combinations = 6** No_of_dice
        print(f"Number of all the outcomes : {combinations}")


        TRIALS = []

        for i in range(Trials):
            roll_the_dice = [random.randint(1,6) for j in range(No_of_dice)]
            TRIALS.append(roll_the_dice)

        #just check a one iteration 

        roll_the_dice


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


        # Save results to Excel file
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            Dice_data.to_excel(writer, sheet_name='Simulation_Data', index=False)
            stact_df.to_excel(writer, sheet_name='Summary', index=False)
            

        probability_trials = Count_32 / Trials

        print(probability_trials)

        print(Dice_data.head())

    else:
        No_of_dice = int(a)
        Trials = int(b)

        combinations = 6** No_of_dice
        print(f"Number of all the outcomes : {combinations}")


        TRIALS = []

        for i in range(Trials):
            roll_the_dice = [random.randint(1,6) for j in range(No_of_dice)]
            TRIALS.append(roll_the_dice)

        #just check a one iteration 

        roll_the_dice


        Dice_data = pd.DataFrame(
            TRIALS,
            columns=[f"Dice {i}" for i in range(1,No_of_dice + 1)]
        )

        Dice_data["Sum"] = Dice_data.sum(axis=1)

        Count_32 = (Dice_data["Sum"] == 32).sum()



        probability_trials = Count_32 / Trials

        print(probability_trials)

        print(Dice_data.head())

plot(Trials,probability_trials)