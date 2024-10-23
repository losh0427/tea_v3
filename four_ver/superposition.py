import statistics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def heat_map(file, max_index):
    df = pd.DataFrame(file, columns=['X', 'Y', 'Z', 'Mag_E']).drop(columns=['Z'])
    df[['X', 'Y']]*=1000
    field_df = df.pivot(index = 'Y', columns = 'X', values = 'Mag_E')
    
    ticklabels = range(40, 270, 10)
    ticks = range(0, 230, 10)

    x_ticklabel = range(0, 242, 10)  # x -> 2.82 - 0.4(margin)
    y_ticklabel = range(0, 263, 10)  # y -> 3.03

    ax = sns.heatmap(field_df,cmap = 'rainbow')
    ax.invert_yaxis()
    ax.set_xticks(x_ticklabel)
    ax.set_yticks(y_ticklabel)
    ax.set_xticklabels(x_ticklabel)
    ax.set_yticklabels(y_ticklabel)
    
    figure = ax.get_figure()
    figure.savefig('./heat_map/'+ str(max_index) +'.jpg', dpi = 400, bbox_inches='tight')
    # plt.show()

def drawHeatMap(OUTPUT_PATH,output_index, max_index):
    with open(f'{OUTPUT_PATH}/output{output_index}.fld', 'r') as f1:
        file1 = f1.readlines()[2:]
    with open(f'{OUTPUT_PATH}/output{output_index+1}.fld', 'r') as f2:
        file2 = f2.readlines()[2:]
    with open(f'{OUTPUT_PATH}/output{output_index+2}.fld', 'r') as f3:
        file3 = f3.readlines()[2:]
    
    for i in range(len(file1)):
        file1[i] =  [float(x) for x in file1[i].split()]
        file2[i] =  [float(x) for x in file2[i].split()]
        file3[i] =  [float(x) for x in file3[i].split()] 
    file = file1.copy() 

    for i in range(len(file1)):
        file[i][3] = (file1[i][3]+file2[i][3]+file3[i][3])/3
    with open('./Maxdata.txt', 'w') as f:
        for i in range(len(file)):
            f.writelines(str(file[i]) + '\n')
    heat_map(file, max_index)



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







if __name__ =='__main__':
    # output_number = 0
    # while output_number <= 0:
    #     print(superposition("C:/Users/USER/Desktop/Tea_second/Code_v1/Full_Flow/Data1",0))
    #     output_number+=3
    drawHeatMap("C:/Users/USER/Desktop/Tea_second/Code_v3/Full_Flow/Data1", 63,63)
    print(superposition("C:/Users/USER/Desktop/Tea_second/Code_v3/Full_Flow/Data1", 63))
    #C:/Users/USER/Desktop/Tea_second/Code_v1/Full_Flow/Data
