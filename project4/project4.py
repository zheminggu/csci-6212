import time
import numpy as np
from pyexcel import Excel_dealer
import string
import random
import math


def randomly_generate_candidates(num_candidates):
    temp_candidates = np.random.randint(0, 100, size=(num_candidates, 2))
    # temp_candidates *= 100
    # print(f"candidates informaiton is {temp_candidates}")
    return temp_candidates


def evaluate_benchmark(candidates, stop_position: int, total_number: int):
    best_profit = candidates[0][0] - candidates[0][1]
    for i in range(stop_position):
        # evaluate which one is the best
        # candidates[i][0] means value of this candidate
        # candidates[i][1] means cost of this candidate
        current_profit = candidates[i][0] * (total_number-i) - candidates[i][1]
        if current_profit > best_profit:
            best_profit = current_profit
    return best_profit


def get_first_candidate_better_than_benchmark(candidates, stop_position: int, total_number: int, baseline):
    for i in range(stop_position, total_number):
        # evaluate if the candidate is better than the baseline
        # candidates[i]
        current_profit = candidates[i][0] * (total_number-(stop_position+i)) - candidates[i][1]
        if current_profit > baseline:
            return current_profit
    # return candidates[len(candidates)-1][0]-candidates[len(candidates)-1][1]
    return 0


def generate_stop_positions(start_position, end_position, step):
    temp_position = start_position
    positions = []
    positions.append(temp_position)
    while temp_position < end_position:
        temp_position += step
        positions.append(int(temp_position))
    print(f"generated positions are {positions}")
    return positions


def get_max_profit(candidates):
    max_profit = -9999
    for i in range(len(candidates)):
        current_profit = candidates[i][0] * (len(candidates)-i) - candidates[i][1]
        if current_profit > max_profit:
            max_profit = current_profit
    return max_profit


# def get_digits_int(number):
#     digit = 0
#     while(number > 0):
#         digit += number % 10
#         number /= 10
#     return digit


def output_information_to_excel(candidates_number, simulate_times, stop_position, accuracy):
    global current_row
    global t_candidates_number
    global t_simulate_times
    global t_stop_position
    global t_accuracy
    print("=========output information to excel =======")
    print(f"candidate number = {candidates_number}, simulate time = {simulate_times}, stop position = {stop_position}, accuracy = {accuracy}")

    excel.insert(column=t_candidates_number, row=current_row, information=f"{candidates_number}")
    excel.insert(column=t_simulate_times, row=current_row, information=f"{simulate_times}")
    excel.insert(column=t_stop_position, row=current_row, information=f"{stop_position}")
    excel.insert(column=t_accuracy, row=current_row, information=f"{accuracy}")
    current_row += 1
    # print(f"num_candidates = {num_candidates}, target = {target} index of this target = {index_candidate}")


def get_further_step_position(stop_positions, accuracy_stop_positions):
    for i in range(len(stop_positions)-1):
        if accuracy_stop_positions[i] > accuracy_stop_positions[i+1]:
            if i-1 >= 0:
                return stop_positions[i-1], stop_positions[i+1]
            else:
                return stop_positions[i], stop_positions[i+1]


# main program here
# constants
e = 2.71828

excel = Excel_dealer("Project4")
# column
t_candidates_number = "A"
t_simulate_times = "B"
t_stop_position = "C"
t_accuracy = "D"

# row
current_row = 1
excel.insert(column=t_candidates_number, row=current_row, information="candidates number")
excel.insert(column=t_simulate_times, row=current_row, information="simulate times")
excel.insert(column=t_stop_position, row=current_row, information="stop position")
excel.insert(column=t_accuracy, row=current_row, information="accuracy")
current_row += 1


print("test begin")
candidates_pool = [1000]
simulate_times = 100000
for num_candidates in candidates_pool:
    candidates = randomly_generate_candidates(num_candidates)
    print(f"current candidates are {candidates}")
    # step = math.pow(10, get_digits_int(num_candidates)-1)
    step = num_candidates
    start_position = 0
    end_position = num_candidates
    while step > 1:
        step /= 10
        stop_positions = generate_stop_positions(start_position, end_position, step)
        accuracy_stop_positions = [0 for i in range(len(stop_positions))]
        print(f"accuracy stop positions are {accuracy_stop_positions}")
        for i in range(len(stop_positions)):
            accuracy = 0.0  # accuracy in this stop position
            for each_simulate in range(simulate_times):
                np.random.shuffle(candidates)
                max_profit = get_max_profit(candidates)
                baseline = evaluate_benchmark(candidates, stop_positions[i], num_candidates)
                current_profit = get_first_candidate_better_than_benchmark(candidates, stop_positions[i], num_candidates, baseline)

                if current_profit > max_profit * 0.98:
                    accuracy += 1

                if each_simulate % 1000 == 0 and each_simulate != 0:
                    print(f"stop position {stop_positions[i]} simulate process {int(each_simulate/1000)}/100. current accuracy {accuracy/each_simulate}")
                    # print(f"baseline {baseline} max_profit {max_profit} current profit {current_profit}")
            accuracy /= simulate_times
            accuracy_stop_positions[i] = accuracy
            output_information_to_excel(num_candidates, simulate_times, stop_positions[i], accuracy)
        start_position, end_position = get_further_step_position(stop_positions, accuracy_stop_positions)
        excel.savefile()
