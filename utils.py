import pandas as pd
from superposition import superposition
import statistics
import numpy as np
import os
import shutil


def move_file(source, destination, initial_count, final_count):
    allfiles = os.listdir(source)

    new_folder_path = destination+str(initial_count)+'-'+str(final_count)

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print("Create folder '{new_folder_path}'.")
    else:
        print("Folder '{new_folder_path}' already exists,")

    #iterate all files to move them to destination folder
    for i in allfiles:
        src_path = os.path.join(source, i)
        dst_path = os.path.join(new_folder_path, i)
        shutil.move(src_path, dst_path)
        #print("Moved {src_path} -> {dst_path}")

def elec_to_heat( file1, file2, file3, coeff = 100000, item = 0.95):

    pass


def superposition(OUTPUT_PATH,output_number):
    #open file 
    with open(f'{OUTPUT_PATH}/output{output_number}.fld', 'r') as f1:
        file1 = f1.readlines()[2:]
    with open(f'{OUTPUT_PATH}/output{output_number+1}.fld', 'r') as f2:
        file2 = f2.readlines()[2:]
    with open(f'{OUTPUT_PATH}/output{output_number+2}.fld', 'r') as f3:
        file3 = f3.readlines()[2:]
    #change str to float
    for i in range(len(file1)):
        file1[i] =  [float(x) for x in file1[i].split()]
        file2[i] =  [float(x) for x in file2[i].split()]
        file3[i] =  [float(x) for x in file3[i].split()]
    
    heat_file1 = file1.copy()
    heat_file2 = file2.copy()
    heat_file3 = file3.copy()
    elec_to_heat()
    
    #average electric fields       
    file = file1.copy() 
    average_mean_list = []
    for i in range(len(file1)):
        file[i][3] = (file1[i][3]+file2[i][3]+file3[i][3])/3
        average_mean_list.append(file[i][3])
    mean_field =  statistics.mean(average_mean_list)   
    


    #split 10*10 square
    list_square = []
    count = 0
    for a in range(len(file)//100):
        small_sqaure = np.empty((10, 10),dtype = object ) #10*10 square
        for i in range(10):
            for j in range(10):
                if count<len(file):
                    small_sqaure[i][j] = file[count]
                    count+=1
        list_square.append(small_sqaure)
    #average each 10*10 square
    average_of_sm_square = []  #record the mean electric field of each 10*10 square
    for i in range(len(list_square)):
        temp = []
        for j in range(10):
            for k in range(10):
                temp.append(list_square[i][j][k][3])        
        average_of_sm_square.append(statistics.mean(temp))
    std_field = statistics.pstdev(average_of_sm_square)
    return mean_field, std_field


def Output_Handler_superposition(iteration, path, dataset_path, parameter):
    average, std = superposition(path,iteration)
    parameter.pop(-1) # paramete[-1] is surrogate model predict value 
    parameter.append(str(average - std * 3))
    parameter.append(str(average))
    parameter.append(str(std))
    with open(dataset_path,'a') as f:
        for para in parameter[:-1]:
            f.write(str(para) + " ")
        f.write(str(parameter[-1]) + "\n")



if __name__ =='__main__':
    pass