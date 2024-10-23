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
    model_flag = False
    model = Surrogate_model()
    data_path = "./Full_Flow/data_1004.txt"
    if model_flag:
        model.import_KRG("./Full_Flow/KRG_model.pkl")
        model.import_KPLS("./Full_Flow/KPLS_model.pkl")
    else:
        model.build(data_path)
        model.export_KRG("./Full_Flow/KRG_model.pkl")
        model.export_KPLS("./Full_Flow/KPLS_model.pkl")
    init_data_path = "./Full_Flow/data_1004_init.txt"
    output_path = "./Full_Flow/data_1004_gen.txt"
    # init part 
    for i in range (0, 300):
        # 1. read the data_gen.txt 
        input_parameter = []
        with open(init_data_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                ans = line.split(' ')[:-1]
            input_parameter.extend(ans)
        print(input_parameter)

        # 2. get the input parameter to predict the output
        input_parameter = np.array(input_parameter).reshape(1,-1)

        # 3. predict the output using KRG and KPLS choose the larger one
        output = None
        output_KRG = model.Mymodel.predict_values(input_parameter)
        output_KPLS = model.Mymodel2.predict_values(input_parameter)
        if output_KRG > output_KPLS:
            output = output_KRG
        else:
            output = output_KPLS
        # 4. write the output to the data_gen.txt
        ## write the output as a law : input_parameter + " " + 0  " " + 0  " " + 0  " " + 0  " " + 0 + " " + output + "\n"
        with open(output_path, 'a') as f:
            f.write(" ".join(input_parameter) + " 0 0 0 0 0 " + str(output) + "\n")
            




