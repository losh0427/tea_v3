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


if __name__ ==  "__main__":
    parser = argparse.ArgumentParser(description='hello!')
    parser.add_argument('-p','--path',help='The path to the file',default='C:/Users/USER/Desktop/Tea_second/Code_v3/Full_Flow')
    parser.add_argument('-d','--data',help='data name',default='data_1016_change')


    args = parser.parse_args()
    PATH = args.path
    data_name = args.data
    DATA_PATH = f'{PATH}/{data_name}.txt'

    move_file_source = 'C:/Users/USER/Desktop/tea/3/Tea_second/Code_v3/Full_Flow/Data1/'
    move_file_destination = 'C:/Users/USER/Desktop/tea/3/Tea_second/Code_v3/Full_Flow/Data/'
    file_record = 'C:/Users/USER/Desktop/tea/3/Tea_second/Code_v3/Full_Flow/move_file.txt'

    #move file to Data
    with open(file_record, mode='r+', encoding='utf-8') as f:
        count = f.readlines()
        initial_count = int((count[1]))
        final_count =int((count[0]))
        f.close()
    move_file(move_file_source, move_file_destination, initial_count, final_count)
    initial_count = final_count+1

    #delete data
    #file_patterns = ["input*.txt", "output*.fld"]
    #delete_files = []
    #for pattern in file_patterns:
    #   delete_files += glob.glob(os.path.join(f'{PATH}/Data1', pattern))
    #for f in delete_files:
    #   os.remove(f)
    #try:
    #   os.remove(f'{PATH}/surrogate_result.csv')
    #except:
    #   None

    # record length
    datamax_initial_len = 0
    with open(DATA_PATH, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        datamax_initial_len = len(list(reader))
    input_number = 0
    output_number = 0
    pre_max_index = -1
    for i in range(300):
        model = Surrogate_model()
        model.build(DATA_PATH)
        parameters = model.find_max(i)
        # ##parameters have 19 variable, the last one is predicted value 
        # ##export input
        # print((parameters[0]))
        with open(f'{PATH}/Data1/input{input_number}.txt', 'w') as f:
            for index in [0,1,2,3,4,5,18,19,20,21]:
                f.write((str(parameters[0][index])) + " ")
        input_number += 1
        with open(f'{PATH}/Data1/input{input_number}.txt', 'w') as f:
            for index in [6,7,8,9,10,11,18,19,20,21]:
                f.write((str(parameters[0][index]))+ " ")
        input_number += 1
        with open(f'{PATH}/Data1/input{input_number}.txt', 'w') as f:
            for index in [12,13,14,15,16,17,18,19,20,21]:
                f.write((str(parameters[0][index]))+ " ")
        input_number += 1
        if len(parameters) == 2:
            with open(f'{PATH}/Data1/input{input_number}.txt', 'w') as f:
                for index in [0,1,2,3,4,5,18,19,20,21]:
                    f.write((str(parameters[1][index]))+ " ")
            input_number += 1
            with open(f'{PATH}/Data1/input{input_number}.txt', 'w') as f:
                for index in [6,7,8,9,10,11,18,19,20,21]:
                    f.write((str(parameters[1][index]))+ " ")
            input_number += 1
            with open(f'{PATH}/Data1/input{input_number}.txt', 'w') as f:
                for index in [12,13,14,15,16,17,18,19,20,21]:
                    f.write((str(parameters[1][index]))+ " ")
            input_number += 1
            
        ############# Ansys executing ###############

        ##Waiting for output
        for num in range(len(parameters)):
            for j in range(3):
                path = f"{PATH}/Data1/output{output_number}.fld"
                print(f"Waiting for output{output_number}")
                while not os.path.exists(path):
                    time.sleep(3)
                output_number += 1
                time.sleep(5)

            # analyze data
            output_path = "C:/Users/USER/Desktop/Tea_second/Code_v3/Full_Flow/Data1/"
            Output_Handler_superposition(output_number-3,output_path,DATA_PATH,parameters[num])


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
                temp = float(actual_data[i][-3])
                if temp > max_value:
                    max_value = temp
                    max_index = i
            if pre_max_index == -1:
                pre_max_index = max_index
            
            #if pre_max_index != max_index :
            #     drawHeatMap(output_path, output_number - 3, max_index)
            print(f"actual value {max_value}, predict value {parameters[num][-1]}, \
                actual average {actual_data[max_index][-2]}, actual std : {actual_data[max_index][-1]}, \
                max index {max_index+1}")
            print("------------------------------")
            final_count+=1
        
        seq = [str(final_count)+'\n',str(initial_count)]
        with open(file_record, mode='w', encoding='utf-8') as f:
            f.writelines(seq)
            f.close()
    

