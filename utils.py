import pandas as pd
import statistics
import numpy as np
import os
import shutil
import copy

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
    # change electric field to heat
    #deal coefficient : div coefficient
    for i in range(len(file1)):
        file1[i][3] = file1[i][3]/coeff
        file2[i][3] = file2[i][3]/coeff
        file3[i][3] = file3[i][3]/coeff
    # deal spread
    mean1 = statistics.mean([file1[i][3] for i in range(len(file1))])
    for i in range(len(file1)):
        file1[i][3] = file1[i][3] + (mean1 - file1[i][3])*item
    for i in range(len(file1)):
        file1[i][3] = file1[i][3] + file2[i][3] 
    mean2 = statistics.mean([file1[i][3] for i in range(len(file1))])
    for i in range(len(file1)):
        file1[i][3] = file1[i][3] + (mean2 - file1[i][3])*item
    for i in range(len(file1)):
        file1[i][3] = file1[i][3] + file3[i][3]
    mean3 = statistics.mean([file1[i][3] for i in range(len(file1))])
    for i in range(len(file1)):
        file1[i][3] = file1[i][3] + (mean3 - file1[i][3])*item
    return file1


# need a function to decide the surrogate model objective value 
def objective_value(elec_mean , elec_std, heat_mean, heat_std):
    # weight function (need to be modified)
    # weight = [0.5, 0.5]
    # final_val = weight[0]*elec_mean + weight[1]*heat_mean
    final_val = 100000*(heat_mean - heat_std)/2 + (elec_mean - elec_std)/2
    return final_val

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
    
    heat_file1 = copy.deepcopy(file1)
    heat_file2 = copy.deepcopy(file2)
    heat_file3 = copy.deepcopy(file3)
    heat_file = elec_to_heat(heat_file1, heat_file2, heat_file3)
    
    #average electric fields       
    file = file1.copy() 
    elec_mean_field = statistics.mean([file[i][3] for i in range(len(file))])
    heat_mean_field = statistics.mean([heat_file[i][3] for i in range(len(heat_file))])


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
    elec_std_field = statistics.pstdev(average_of_sm_square)
    
    #do the same thing for heat field
    list_square = []
    count = 0
    for a in range(len(heat_file)//100):
        small_sqaure = np.empty((10, 10),dtype = object ) #10*10 square
        for i in range(10):
            for j in range(10):
                if count<len(heat_file):
                    small_sqaure[i][j] = heat_file[count]
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
    heat_std_field = statistics.pstdev(average_of_sm_square)
    obj_val = objective_value(elec_mean_field , elec_std_field, heat_mean_field, heat_std_field)
    return elec_mean_field, elec_std_field , heat_mean_field, heat_std_field , obj_val


def Output_Handler_superposition(iteration, path, dataset_path, parameter):
    elec_mean , elec_std, heat_mean, heat_std , val = superposition(path,iteration)
    parameter.pop(-1) # paramete[-1] is surrogate model predict value 
    parameter.append(str(elec_mean))
    parameter.append(str(elec_std))
    parameter.append(str(heat_mean))
    parameter.append(str(heat_std))
    parameter.append(str(val))
    with open(dataset_path,'a') as f:
        for para in parameter[:-1]:
            f.write(str(para) + " ")
        f.write(str(parameter[-1]) + "\n")



if __name__ =='__main__':
    pass