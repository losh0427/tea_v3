import numpy as np
from smt.applications.mixed_integer import(
    FLOAT,
    ORD,
    ENUM,
    MixedIntegerSamplingMethod,
    MixedIntegerSurrogateModel,
    GOWER,
    MixedIntegerContext,
)
from smt.sampling_methods import LHS, Random, FullFactorial
from smt.surrogate_models import LS, QP, KPLS, KRG, KPLSK, GEKPLS, MGP
import matplotlib.pyplot as plt
import random
import csv
import pickle
from Surrogate_Model import Surrogate_model
import os
import pandas as pd


if __name__ == "__main__":
    model_flag = True
    input_bound=[[0, 360], [500, 900], [0, 360], [500, 900], 
                [0, 360], [500, 900], [0, 360], [500, 900], 
                [0, 360], [500, 900], [0, 360], [500, 900], 
                [-100, 100], [-100, 100], [-100, 100], [-100, 100]]
    heat_coeff=100000
    item_coeff=0.95
    model = Surrogate_model(0, input_bound, heat_coeff, item_coeff)
    data_path = "./data_1004.txt"
    if model_flag:
        model.import_KRG("./KRG_model.pkl")
        model.import_KPLS("./KPLS_model.pkl")
    else:
        model.build(data_path)
        model.export_KRG("./KRG_model.pkl")
        model.export_KPLS("./KPLS_model.pkl")
    init_data_path = "./data_1004_init.txt"
    output_path = "./data_1004_gen.txt"
    # init part 
    # 1. read the data_gen.txt 
    input_parameter = []
    with open(init_data_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            ans = line.split(' ')[:-5]
            input_parameter.append(ans) 
    input_parameter = np.array(input_parameter)

    for i in range (0, 300):
        # 2. get the input parameter to predict the output
        # input_parameter = np.array(input_parameter).reshape(1,-1)
        # 3. predict the output using KRG and KPLS choose the larger one
        output = None
        # print(input_parameter[i])
        round_para = np.array([input_parameter[i]])
        # print(round_para)
        output_KRG = model.Mymodel.predict_values(round_para)
        output_KPLS = model.secondModel.predict_values(round_para)
        output_KRG = output_KRG[0]
        output_KPLS = output_KPLS[0]
        # print(i)
        # print(round_para)
        # print("KRG", output_KRG)
        # print("KPLS", output_KPLS)
        type_flag = 0 
        for i in range(0,3):
            type_flag = i
            if type_flag == 0:
                output = (output_KRG[0] + output_KPLS[0])/2
                output_path = "./data_1004_gen_mix.txt"
            elif type_flag == 1:
                output = output_KRG[0]
                output_path = "./data_1004_gen_KRG.txt"
            elif type_flag == 2:
                output = output_KPLS[0]
                output_path = "./data_1004_gen_KPLS.txt"
            # 4. write the output to the data_gen.txt
            ## write the output as a law : input_parameter[i] + " " + 0  " " + 0  " " + 0  " " + 0  " " + 0 + " " + output + "\n"
            with open(output_path, 'a') as f:
                f.write(" ".join(round_para[0]) + " 0 0 0 0 " + str(output) + "\n")
            




