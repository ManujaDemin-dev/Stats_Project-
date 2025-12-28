
def cal_exact_probability(dice_sum,dice_no,faces=6):

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



