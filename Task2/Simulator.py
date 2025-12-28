import matplotlib.pyplot as plt


def plot(total_trials, final_probability , exact_probability):
    plt.figure(figsize=(10, 6))
    
   
    Theoretical_Probability = exact_probability
 
    plt.axhline(y=Theoretical_Probability, color='red', linestyle='--', 
                label=f'Theoretical ({Theoretical_Probability})', alpha=0.7)

 
    plt.hlines(y=final_probability, xmin=1, xmax=total_trials, 
               color='tab:blue', linewidth=4, label=f'Estimated Probability({final_probability})')


    plt.xlim(1, total_trials + 1) 
    plt.ylim(0, 0.12)
    plt.xscale('log')
    plt.title(f"Dice Probability Comparison (at {total_trials} Trials)", fontsize=14)
    plt.xlabel("Number of Trials (Log Scale)", fontsize=12)
    plt.ylabel("Probability Value", fontsize=12)
    
    plt.grid(True, which="both", linestyle=':', alpha=0.4)
    plt.legend(loc='upper right', frameon=True, shadow=True)
    
    plt.tight_layout()
    plt.show()

