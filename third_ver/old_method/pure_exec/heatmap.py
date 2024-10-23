import statistics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils import superposition, elec_to_heat
import copy

def heat_map(file, max_index, OUTPUT_PATH, type = 'elec', mean = 0, std = 0):
    df = pd.DataFrame(file, columns=['X', 'Y', 'Z', 'Mag_E']).drop(columns=['Z'])
    df[['X', 'Y']]*=1000
    field_df = df.pivot(index = 'Y', columns = 'X', values = 'Mag_E')
    
    ticklabels = range(40, 270, 10)
    ticks = range(0, 230, 10)

    x_ticklabel = range(0, 242, 10)  # x -> 2.82 - 0.4(margin)
    y_ticklabel = range(0, 263, 10)  # y -> 3.03
# Code to be inserted where "# code here" comment is placed
    if type == 'elec':
        title = 'Electric field'
        # vmax = mean + 4*std  
        # vmin = mean - 4*std
        # vmax = 1000000
        # vmin = 0
        vmax = field_df.max().max()* 1.05
        vmin = field_df.min().min()* 0.95
    elif type == 'heat':
        title = 'Heat field'
        # Use actual data range for colorbar limits
        # vmax = mean + 4*std
        # vmin = mean - 4*std
        # vmax = 10
        # vmin = 0
        vmax = field_df.max().max() * 1.05
        vmin = field_df.min().min() * 0.95
    # Now generate the heatmap
    ax = sns.heatmap(field_df, cmap='rainbow', vmin=vmin, vmax=vmax, cbar_kws={'format': '%.2f'} if type == 'heat' else {'format': '%.0f'})
    ax.invert_yaxis()
    ax.set_xticks(x_ticklabel)
    ax.set_yticks(y_ticklabel)
    ax.set_xticklabels(x_ticklabel)
    ax.set_yticklabels(y_ticklabel)


    ax.set_title(title)
    figure = ax.get_figure()
    figure.savefig(OUTPUT_PATH + '/'  + title + str(max_index) +'.jpg', dpi = 400, bbox_inches='tight')
    #reset the plot
    plt.clf()
    # plt.show()

def drawHeatMap(HOME_PATH, OUTPUT_PATH, DRAW_PATH,output_index, max_index, elec_mean_field_value, elec_std_field_value, heat_mean_field_value, heat_std_field_value):
    with open(f'{HOME_PATH+OUTPUT_PATH}/output{output_index}.fld', 'r') as f1:
        file1 = f1.readlines()[2:]
    with open(f'{HOME_PATH+OUTPUT_PATH}/output{output_index+1}.fld', 'r') as f2:
        file2 = f2.readlines()[2:]
    with open(f'{HOME_PATH+OUTPUT_PATH}/output{output_index+2}.fld', 'r') as f3:
        file3 = f3.readlines()[2:]
    
    for i in range(len(file1)):
        file1[i] =  [float(x) for x in file1[i].split()]
        file2[i] =  [float(x) for x in file2[i].split()]
        file3[i] =  [float(x) for x in file3[i].split()] 
    file = file1.copy() 
    heat_file1 = copy.deepcopy(file1)
    heat_file2 = copy.deepcopy(file2)
    heat_file3 = copy.deepcopy(file3)
    heat_file = elec_to_heat(heat_file1, heat_file2, heat_file3)

    for i in range(len(file)):
        file[i][3] = (file1[i][3]+file2[i][3]+file3[i][3])
        
    # with open('./Maxdata.txt', 'w') as f:
    #     for i in range(len(file)):
    #         f.writelines(str(file[i]) + '\n')

    # with open(f'{OUTPUT_PATH}/Maxdata.txt', 'w') as f:
    #     for i in range(len(heat_file)):
    #         f.writelines(str(heat_file[i]) + '\n')
    
    heat_map(file, max_index, HOME_PATH+DRAW_PATH, 'elec', elec_mean_field_value, elec_std_field_value)
    heat_map(heat_file, max_index, HOME_PATH+DRAW_PATH, 'heat', heat_mean_field_value, heat_std_field_value)





if __name__ =='__main__':
    # output_number = 0
    # while output_number <= 0:
    #     print(superposition("C:/Users/USER/Desktop/Tea_second/Code_v1/Full_Flow/Data1",0))
    #     output_number+=3
    # drawHeatMap("C:/Users/USER/Desktop/tea/3/Tea_second/Code_v3/Full_Flow/Data1/", 63,63)
    # print(superposition("C:/Users/USER/Desktop/tea/3/Tea_second/Code_v3/Full_Flow/Data1/", 63))
    #C:/Users/USER/Desktop/Tea_second/Code_v1/Full_Flow/Data
    elec_mean_field_value , elec_std_field_value, heat_mean_field_value, heat_std_field_value, obj = superposition("./mix/best_data", 153)
    print(elec_mean_field_value, elec_std_field_value, heat_mean_field_value, heat_std_field_value)
    drawHeatMap("./mix/best_data", 153, 512, elec_mean_field_value, elec_std_field_value, heat_mean_field_value, heat_std_field_value)
