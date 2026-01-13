import matplotlib.pyplot as plt

def plot(total_trials, final_probability , exact_probability):
    try:
        
        if not isinstance(total_trials,int):
            raise TypeError("total_trials must be an integer.")
        
        if not all(isinstance(x,(int,float)) for x in [final_probability,exact_probability]):
            raise TypeError("Probabilities must be numbers.")
        
        if total_trials <= 0:
            raise ValueError("total_trials must be greater than 0")
        
        if not(0 <= final_probability <= 1):
            raise  ValueError("final_probability must be between 0 and 1")
        
        if not (0 <= exact_probability <= 1):
            raise ValueError("exact_probability must be between 0 and 1")
        
        
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
        
    except TypeError as te:
        print("Type Error",te)
    
    except ValueError as ve:
        print("Value Error",ve)
        
    except Exception as e:
        print("Unexpected Error :",e)

