import pandas as pd
from superposition import superposition

# def Create_Initial_dataset ():
#     path = "C:/Users/USER/Desktop/Tea_second/Code_v1/Full_Flow/Data1/"
#     dataset_path = "C:/Users/USER/Desktop/Tea_second/Code_v1/Full_Flow/data_1004.txt"
#     for i in range(0,6,3):
#         file0 = path + "output"+ str(i)+".fld"
#         file1 = path + "output"+ str(i+1)+".fld"
#         file2 = path + "output"+ str(i+2)+".fld"
#         data0 = pd.read_csv(file0, sep='\s+', header=None, skiprows=2)
#         data1 = pd.read_csv(file1, sep='\s+', header=None, skiprows=2)
#         data2 = pd.read_csv(file2, sep='\s+', header=None, skiprows=2)
#         data0.columns = ["X", "Y", "Z", "Mag_E"]
#         data1.columns = ["X", "Y", "Z", "Mag_E"]
#         data2.columns = ["X", "Y", "Z", "Mag_E"]
#         data_new = (data0['Mag_E'] + data1['Mag_E'] + data2['Mag_E'])/3
#         average = data_new.mean()
#         std = data_new.std()
#         print(average)
#         print(std)
#         input_parameter = []
#         for j in range(3):
#             with open(path + "input"+ str(i+j)+".txt", 'r') as f:
#                 lines = f.readlines()
#                 for line in lines:
#                     ans = line.split(' ')[:-1]
#                 input_parameter.extend(ans)
#         input_parameter.append(str(average - std * 2))
#         input_parameter.append(str(average))
#         input_parameter.append(str(std))
#         print(input_parameter)

#         with open(dataset_path,'a') as f:
#             for para in input_parameter[:-1]:
#                 f.write(str(para) + " ")
#             f.write(str(input_parameter[-1]) + "\n")

def Create_Initial_dataset_Superposition ():
    path = "C:/Users/USER/Desktop/Tea_second/Code_v3/Full_Flow/Data1/"
    dataset_path = "C:/Users/USER/Desktop/Tea_second/Code_v3/Full_Flow/data_1016_change.txt"
    for i in range(0,33,3):
        average, std = superposition(path,i)
        input_parameter = []
        for j in range(3):
            with open(path + "input"+ str(i+j)+".txt", 'r') as f:
                lines = f.readlines()
                for line in lines:
                    ans = line.split(' ')[:-1]
                input_parameter.extend(ans)
        input_parameter.append(str(average - std * 3))
        input_parameter.append(str(average))
        input_parameter.append(str(std))
        print(input_parameter)

        with open(dataset_path,'a') as f:
            for para in input_parameter[:-1]:
                f.write(str(para) + " ")
            f.write(str(input_parameter[-1]) + "\n")


# def Output_Handler(iteration, path, dataset_path, parameter):
#     file0 = path + "output"+ str(iteration)+".fld"
#     file1 = path + "output"+ str(iteration+1)+".fld"
#     file2 = path + "output"+ str(iteration+2)+".fld"
#     data0 = pd.read_csv(file0, sep='\s+', header=None, skiprows=2)
#     data1 = pd.read_csv(file1, sep='\s+', header=None, skiprows=2)
#     data2 = pd.read_csv(file2, sep='\s+', header=None, skiprows=2)
#     data0.columns = ["X", "Y", "Z", "Mag_E"]
#     data1.columns = ["X", "Y", "Z", "Mag_E"]
#     data2.columns = ["X", "Y", "Z", "Mag_E"]
#     data_new = (data0['Mag_E'] + data1['Mag_E'] + data2['Mag_E'])/3
#     average = data_new.mean()
#     std = data_new.std()
#     parameter.pop(-1) # paramete[-1] is surrogate model predict value 
#     parameter.append(str(average - std * 2))
#     parameter.append(str(average))
#     parameter.append(str(std))
#     with open(dataset_path,'a') as f:
#         for para in parameter[:-1]:
#             f.write(str(para) + " ")

#         # for i in range(len(parameter)-1):
#         #     if i in [2,5,8,11,14,17]:
#         #         f.write(str(int(parameter[i])) + " ")
#         #     else:
#         #         f.write(str(parameter[i]) + " ")
#         f.write(str(parameter[-1]) + "\n")



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
    Create_Initial_dataset_Superposition()