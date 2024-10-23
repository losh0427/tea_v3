import random
import os
import shutil
import time
import pandas as pd
import glob
import numpy as np
#from smt_test import Surrogate_model
from Surrogate_Model import Surrogate_model
from sklearn.metrics import accuracy_score,r2_score
from smt.sampling_methods import LHS, Random
from smt.applications.mixed_integer import(
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
from utils import Output_Handler_superposition , move_file

# PATH = "C:/Users/USER/Desktop/Code/Full_Flow"
# DATA_PATH = f'{PATH}/data_for_vedio.txt'
BOX_MINIMUM = 300
BOX_MAXIMUM  = 500
# ANGLES = [0, 90]
# POSITIONS = ["up", "front", "back", "left", "right"]
#POSITIONS = ["0", "1", "2", "3", "4"]

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
    return final_count, initial_count + 1


if __name__ ==  "__main__":
    args = parse_arguments()
    PATH = args.path
    data_name = args.data
    DATA_PATH = f'{PATH}{data_name}.txt'
    move_file_source = f'{PATH}Data1/'
    move_file_destination = f'{PATH}Data/'
    file_record = f'{PATH}move_file.txt'
    time_path = './round_time.txt'
    model_time_path = './model_time.txt'
    # [debug]
    print(f"PATH : {PATH}")
    print(f"DATA_PATH : {DATA_PATH}")
    print(f"move_file_source : {move_file_source}")
    print(f"move_file_destination : {move_file_destination}")

    #move file to Data
    final_count, initial_count = move_files(file_record, move_file_source, move_file_destination)

    # record length
    datamax_initial_len = 0
    with open(DATA_PATH, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        datamax_initial_len = len(list(reader))
    input_number = 0
    output_number = 0
    pre_max_index = -1
    for i in range(300):
        # if i == 0 => search_time = 60 then search_time = 10* 60 
        if i == 0:
            seraching_time = 0
        else:
            seraching_time = 10 * 60
        print("start")
        start_time = time.time()
        model = Surrogate_model(seraching_time)
        model.build(DATA_PATH)
        mid_time = time.time()
        parameters = model.find_max(i)
        end_time = time.time()
        print("end")
        record_str = f"iteration {i}, total_time {end_time - start_time}, build_time {mid_time - start_time}, search_time {end_time - mid_time}, dataset_num {i+300}, sample_num {model.total_sampling_num }\n "
        print(record_str)
        with open(model_time_path, 'a') as f:
            f.write(record_str)
        # ##parameters have 19 variable, the last one is predicted value 
        # ##export input
        # print((parameters[0]))
        with open(f'{PATH}/Data1/input{input_number}.txt', 'w') as f:
            for index in [0,1,2,3,12,13,14,15]:
                f.write((str(parameters[0][index])) + " ")
        input_number += 1
        with open(f'{PATH}/Data1/input{input_number}.txt', 'w') as f:
            for index in [4,5,6,7,12,13,14,15]:
                f.write((str(parameters[0][index]))+ " ")
        input_number += 1
        with open(f'{PATH}/Data1/input{input_number}.txt', 'w') as f:
            for index in [8,9,10,11,12,13,14,15]:
                f.write((str(parameters[0][index]))+ " ")
        input_number += 1
        if len(parameters) == 2:
            with open(f'{PATH}/Data1/input{input_number}.txt', 'w') as f:
                for index in [0,1,2,3,12,13,14,15]:
                    f.write((str(parameters[1][index]))+ " ")
            input_number += 1
            with open(f'{PATH}/Data1/input{input_number}.txt', 'w') as f:
                for index in [4,5,6,7,12,13,14,15]:
                    f.write((str(parameters[1][index]))+ " ")
            input_number += 1
            with open(f'{PATH}/Data1/input{input_number}.txt', 'w') as f:
                for index in [8,9,10,11,12,13,14,15]:
                    f.write((str(parameters[1][index]))+ " ")
            input_number += 1
            
        ############# Ansys executing ###############

        ##Waiting for output
        # for num in range(len(parameters)):
        for j in range(3):
            path = f"{PATH}/Data1/output{output_number}.fld"
            print(f"Waiting for output{output_number}")
            start_time = time.time()
            while not os.path.exists(path):
                time.sleep(3)
            end_time = time.time()
            # add record time into file
            with open(time_path, 'a') as f:
                f.write(f"{end_time - start_time}\n")
            output_number += 1
            time.sleep(5)
        # get now input data to output
        now_input = []
        with open(f'{PATH}/Data1/input{output_number-3}.txt', 'r') as f:
            line = f.readlines()
            # only append [0,1,2,3]
            for i in range(4):
                now_input.append(float(line[0].split(' ')[i]))
        with open(f'{PATH}/Data1/input{output_number-2}.txt', 'r') as f:
            line = f.readlines()
            # only append [4,5,6,7]
            for i in range(4):
                now_input.append(float(line[0].split(' ')[i]))
        with open(f'{PATH}/Data1/input{output_number-1}.txt', 'r') as f:
            line = f.readlines()
            for i in range(8):
                now_input.append(float(line[0].split(' ')[i]))
        print(f"now input number {output_number-3}, {output_number-2}, {output_number-1}")
        print(f"now_input : {now_input}")

        # analyze data
        output_path = "C:/Users/USER/Desktop/tea/3/Tea_second/Code_v3/Full_Flow/Data1/"
        Output_Handler_superposition(output_number-3,output_path,DATA_PATH,now_input)


        #TODO : deal the output foramt
        # show training result
        actual_data = []
        with open(DATA_PATH,'r') as f:
            lines = f.readlines()
            for line in lines:
                ans = line.split(' ')
                actual_data.append(ans)
        max_value = 0
        max_index = -1
        for i in range(len(actual_data)):
            temp = float(actual_data[i][-1])
            if temp > max_value:
                max_value = temp
                max_index = i
        # first time
        if pre_max_index == -1:
            pre_max_index = max_index
        
        #if pre_max_index != max_index :
        #     drawHeatMap(output_path, output_number - 3, max_index)
        print(f"round {i},\n \
                this round predict value {now_input[-1]},\n \
            actual max value {max_value}, \n \
            actual max electric average {actual_data[max_index][-5]}, actual max electric std : {actual_data[max_index][-4]},\n \
            actual max heat average {actual_data[max_index][-3]}, actual max heat std : {actual_data[max_index][-2]}, \n\
            max index {max_index+1}")
        print("------------------------------")
        final_count+=1
        
        seq = [str(final_count)+'\n',str(initial_count)]
        with open(file_record, mode='w', encoding='utf-8') as f:
            f.writelines(seq)
            f.close()
    

