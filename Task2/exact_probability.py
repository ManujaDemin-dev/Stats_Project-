
def cal_exact_probability(dice_sum,dice_no,faces=6):
    try:
        
        if not all(isinstance(x,int) for x in [dice_sum,dice_no,faces]):
            raise TypeError("dice_sum,dice_no and faces must be integers")
        
        if dice_no <= 0:
            raise ValueError("dice_no must be greater than o")
        
        if faces <= 1:
            raise ValueError("faces must be greater than 1")
        
        if dice_sum < 0:
            raise ValueError("dice_sum cannot be negative")

        if dice_sum < dice_no or dice_sum > dice_no * faces:
            return 0
        

        max_sum = dice_no * faces

        count = [0] * (max_sum + 1)
        count[0] = 1

        for x in range(dice_no):

            new_count = [0] * (max_sum + 1)

            for y, outs in enumerate(count):

                if outs == 0:

                    continue

                for face in range(1, faces + 1):

                    if y + face <= max_sum:

                        new_count[y + face] += outs
            count = new_count

        return count[dice_sum]
    
    except TypeError as te:
        print("Type Error:",te)
    
    except ValueError as ve:
        print("Value Error",ve)
    
    except MemoryError:
        print("Memory Error: Input values are too large ")
        
    except Exception as e:
        print("Unexpected Error",e)



