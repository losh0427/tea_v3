import random
import os
import time
import pandas as pd
import glob
from smt_test import Surrogate_model
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
import numpy as np
BOX_MINIMUM = 300
BOX_MAXIMUM  = 500
from utils import superposition




# TODO: surrogate or RL
def initial_LHS_model():
    # randomly generate parameter
    xtypes = [FLOAT, ORD, FLOAT, FLOAT, ORD, FLOAT, FLOAT, ORD, FLOAT, FLOAT, ORD, FLOAT, FLOAT, ORD, FLOAT, FLOAT, ORD, FLOAT, FLOAT, FLOAT, FLOAT, FLOAT]
    xlimits = [[0, 360], ["2","2.45","3"], [500,900], [0, 360], ["2","2.45","3"], [500,900], [0, 360], ["2","2.45","3"], [500,900], [0, 360], ["2","2.45","3"], [500,900], [0, 360], ["2","2.45","3"], [500,900], [0, 360], ["2","2.45","3"], [500,900], [-100, 100], [-100, 100], [-100, 100], [-100, 100]]
    mixint = MixedIntegerContext(xtypes, xlimits)
    sampling_method = mixint.build_sampling_method(Random)
    sampling_value = sampling_method(1)[0]
    # print((sampling_value))
    input1 = sampling_value[:6]
    input2 = sampling_value[6:12]
    input3 = sampling_value[12:18]
    position = sampling_value[18:]
    input1 = np.append(input1,position)
    input2 = np.append(input2,position)
    input3 = np.append(input3,position)
    sampling_split = [input1,input2,input3]
    return sampling_split


def Create_Initial_dataset_Superposition ():
    path = "C:/Users/USER/Desktop/Tea_second/Code_v3/Full_Flow/Data1/"
    dataset_path = "C:/Users/USER/Desktop/Tea_second/Code_v3/Full_Flow/data_1004.txt"
    for i in range(0,900,3):
        average, std = superposition(path,i)
        input_parameter = []
        for j in range(3):
            if j == 1 or j == 0:
                with open(path + "input"+ str(i+j)+".txt", 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        ans = line.split(' ')[:-1]
                    input_parameter.extend(ans[:-4])
            else:
                with open(path + "input"+ str(i+j)+".txt", 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        ans = line.split(' ')[:-1]
                    input_parameter.extend(ans)
        input_parameter.append(str(average - std * 2))
        input_parameter.append(str(average))
        input_parameter.append(str(std))
        print(input_parameter)

        with open(dataset_path,'a') as f:
            for para in input_parameter[:-1]:
                f.write(str(para) + " ")
            f.write(str(input_parameter[-1]) + "\n")

        print("finish")

if __name__ ==  "__main__":
    Create_Initial_dataset_Superposition()
    # parser = argparse.ArgumentParser(description='hello!')
    # parser.add_argument('-p','--path',help='The path to the file',default='C:/Users/USER/Desktop/Tea_second/Code_v2_addPosition/Full_Flow')
    # parser.add_argument('-d','--data',help='data name',default='data_1004')


    # args = parser.parse_args()
    # PATH = args.path
    # data_name = args.data
    # DATA_PATH = f'{PATH}/{data_name}.txt'

    # # delete data
    # file_patterns = ["input*.txt", "output*.fld"]
    # delete_files = []
    # for pattern in file_patterns:
    #     delete_files += glob.glob(os.path.join(f'{PATH}/Data', pattern))
    # for f in delete_files:
    #     os.remove(f)
    # try:
    #     os.remove(f'{PATH}/surrogate_result.csv')
    # except:
    #     None

    # input_number = 0
    # output_number = 0
    #
    # for i in range(300):
    #     # predict
    #     parameters = initial_LHS_model()
    #     for j in range(3):
    #         with open(f'{PATH}/Data1/input{input_number}.txt', 'w') as f:
    #             for parameter in parameters[j]:
    #                 f.write(str(parameter) + " ")
    #         input_number += 1
    
