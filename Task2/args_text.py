import argparse as ap

if __name__ == "__main__" :

    print("\n")
    print("WELCOME TO _ _CAR GAME_ _")

    parser = ap.ArgumentParser()
    parser.add_argument("--CAR_BRAND" , help="enter a car brand")
    parser.add_argument("--CAR_Race" , help="enter a race type")
    args = parser.parse_args()

    a = args.CAR_BRAND
    b = args.CAR_Race

    if a == None and b == None:

        print("I would bring my BMW M5 Comp for a Drift race \n")

    else:

        print(f"i would bring my {a} for a {b} \n")
        
        



