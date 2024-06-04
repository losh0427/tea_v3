import random
import os
import shutil
import time
import pandas as pd
import glob
import numpy as np
#from smt_test import Surrogate_model
from Surrogate_Model import Surrogate_model
from sklearn.metrics import accuracy_score, r2_score
from smt.sampling_methods import LHS, Random
from smt.applications.mixed_integer import (
    FLOAT,
    ORD,
    ENUM,
    MixedIntegerSamplingMethod,
    MixedIntegerSurrogateModel,
    GOWER,
    MixedIntegerContext,
)
import csv
import argparse
from utils import Output_Handler_superposition, move_file

BOX_MINIMUM = 300
BOX_MAXIMUM = 500

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process model parameters.')
    parser.add_argument('-p', '--path', help='The path to the file', default='C:/Users/USER/Desktop/tea/3/Tea_second/Code_v3/Full_Flow/')
    parser.add_argument('-d', '--data', help='data name', default='data_1004')
    return parser.parse_args()

def move_files(file_record, source, destination):
    with open(file_record, mode='r+', encoding='utf-8') as f:
        count = f.readlines()
        initial_count = int(count[1])
        final_count = int(count[0])
    move_file(source, destination, initial_count, final_count)
    return final_count, final_count + 1

def global_optimization(exec_path="C:/Users/USER/Desktop/tea/3/Tea_second/Code_v3/Full_Flow/",
                        dataset_name="data_1004",
                        round_num=300,
                        heat_coeff=100000,
                        item_coeff=0.95,
                        input_bound=[[0, 360], ["2.0", "2.45", "3.0"], [500, 900], [0, 360], ["2.0", "2.45", "3.0"], [500, 900], 
                                     [0, 360], ["2.0", "2.45", "3.0"], [500, 900], [0, 360], ["2.0", "2.45", "3.0"], [500, 900], 
                                     [0, 360], ["2.0", "2.45", "3.0"], [500, 900], [0, 360], ["2.0", "2.45", "3.0"], [500, 900], 
                                     [-100, 100], [-100, 100], [-100, 100], [-100, 100]],
                        output_path='Data1', data_path='Data1', file_record='move_file.txt'):
    
    if round_num == 0:
        # testing
        return


    PATH = exec_path
    DATA_PATH = f'{PATH}{dataset_name}.txt'
    move_file_source = f'{PATH}{output_path}/'
    move_file_destination = f'{PATH}{data_path}/'
    file_record = f'{PATH}{file_record}'
    time_path = './round_time.txt'
    model_time_path = './model_time.txt'
    # comment in the future
    input_bound = [[0, 360], [500, 900], [0, 360], [500, 900], [0, 360], [500, 900], [0, 360], [500, 900], [-100, 100], [-100, 100], [-100, 100], [-100, 100]]



    final_count, initial_count = move_files(file_record, move_file_source, move_file_destination)

    datamax_initial_len = 0
    with open(DATA_PATH, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        datamax_initial_len = len(list(reader))
    input_number = 0
    output_number = 0
    pre_max_index = -1
    for i in range(1000):
        seraching_time = 0 if i == 0 else 10 * 60
        start_time = time.time()
        model = Surrogate_model(seraching_time, input_bound, heat_coeff, item_coeff)
        model.build(DATA_PATH)
        mid_time = time.time()
        parameters = model.find_max(i)
        end_time = time.time()
        
        record_str = f"iteration {i}, total_time {end_time - start_time}, build_time {mid_time - start_time}, search_time {end_time - mid_time}, dataset_num {i+300}, sample_num {model.total_sampling_num}\n"
        with open(model_time_path, 'a') as f:
            f.write(record_str)

        for param_set in parameters:
            for subset in [[0, 1, 2, 3, 12, 13, 14, 15], [4, 5, 6, 7, 12, 13, 14, 15], [8, 9, 10, 11, 12, 13, 14, 15]]:
                with open(f'{PATH}/{data_path}/input{input_number}.txt', 'w') as f:
                    f.write(" ".join(str(param_set[index]) for index in subset))
                input_number += 1
        
        ## Waiting Ansys output
        for j in range(3):
            path = f"{PATH}/{data_path}/output{output_number}.fld"
            print(f"Waiting for output{output_number}")
            while not os.path.exists(path):
                time.sleep(3)
            output_number += 1
            time.sleep(5)
        
        now_input = []
        for idx in range(3):
            with open(f'{PATH}/{data_path}/input{output_number-3+idx}.txt', 'r') as f:
                now_input.extend(float(value) for value in f.readline().split())

        output_path = f"{PATH}/{data_path}/"
        Output_Handler_superposition(output_number-3, output_path, DATA_PATH, now_input, heat_coeff, item_coeff)

        actual_data = []
        with open(DATA_PATH, 'r') as f:
            lines = f.readlines()
            for line in lines:
                actual_data.append(line.split())

        max_value = 0
        max_index = -1
        for idx, data in enumerate(actual_data):
            temp = float(data[-1])
            if temp > max_value:
                max_value = temp
                max_index = idx

        if pre_max_index == -1:
            pre_max_index = max_index
        
        print(f"round {i},\n this round predict value {now_input[-1]},\n actual max value {max_value}, \n actual max electric average {actual_data[max_index][-5]}, actual max electric std: {actual_data[max_index][-4]},\n actual max heat average {actual_data[max_index][-3]}, actual max heat std: {actual_data[max_index][-2]}, \n max index {max_index+1}")
        final_count += 1
        
        with open(file_record, mode='w', encoding='utf-8') as f:
            f.writelines([str(final_count)+'\n', str(initial_count)])
        if i >= round_num:
            break

if __name__ == "__main__":
    args = parse_arguments()
    global_optimization(exec_path=args.path, dataset_name=args.data)
