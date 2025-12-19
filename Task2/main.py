import pandas as pd
import random

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

Count_32 = (Dice_data["Sum"] == 32).sum()



probability_trials = Count_32 / Trials

print(probability_trials)

print(Dice_data.head())
