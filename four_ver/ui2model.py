from time import sleep
from utils import superposition
from heatmap import drawHeatMap
import pandas as pd
import matplotlib.pyplot as plt
from model import global_optimization
from analyze_data import draw_trend
import os

# Initial search iterations at the beginning
INIT_ITERATION = 300

# Called from pyqt5.py
def run(iteration_time, material_coefficient, ETconvert_coefficient, seconds_need, data_limit, update_progress):
    # TODO 
    
    # iteration_time default is 240
    # material_coefficient default is 0.95
    # ETconvert_coefficient default is 100000
    # update_progress updates the progress bar, passing in the number of completed iterations after each search
    # For example, update_progress(i)

    # seconds_need default is 3, can be temporarily ignored
    # data_limit default is [[0, 360], [500, 900], [-100, 100]]
    # Represents upper and lower bounds for phase, power, position, can also be temporarily ignored

    # global_optimization()
    # test
    # global_optimization(round_num=1)
    # global_optimization(round_num=1)    
    global_optimization(round_num=80)
    # sleep(5)
    update_progress(5)


    # Expected to execute model from here

    # for i in range(iteration_time):
    #     sleep(2)
    #     update_progress(i)



def getResult(drawOutput, file_path):
    _, max_id = getTrendArrayAndMaxId(file_path)

    # Scan the folders in "/Data/"
    data_dir = os.path.join(file_path, "Data").replace("\\", "/")
    print(data_dir)
    target_folder = None
    temp_initial_count = 0
    temp_final_count = 0
    for folder_name in os.listdir(data_dir):
        try:
            initial_count, final_count = map(int, folder_name.split('-'))
            temp_initial_count = initial_count
            temp_final_count = final_count
            if initial_count <= max_id <= final_count:
                target_folder = folder_name
                break
        except ValueError:
            continue
    target_folder_path = None
    if target_folder is None:
        temp_initial_count = temp_final_count
        data_dir = os.path.join(file_path, "Data1").replace("\\", "/")
        target_folder_path = data_dir
    else:
        target_folder_path = os.path.join(data_dir, target_folder)
    max_id += 1
    pic_path = "/UI_pic"
    the_id = max_id - temp_initial_count
    print("the_id : ", the_id)
    print("max_id : ", max_id)
    print("input_id : ", the_id*3)
    # Call the superposition function
    elec_mean, elec_std, heat_mean, heat_std, val = superposition(target_folder_path, the_id*3, 100000, 0.95)
    
    plt.clf()
    # fix the middle parameter
    if target_folder is None:
        drawHeatMap(file_path, "/Data1/", pic_path, the_id, max_id, elec_mean, elec_std, heat_mean, heat_std)
    else:
        drawHeatMap(file_path, "/Data/" + target_folder, pic_path, the_id, max_id, elec_mean, elec_std, heat_mean, heat_std)
    
    plt.clf()
    draw_trend(file_path, file_path + "/UI_pic")

    drawOutput(
        heat_path= file_path + pic_path + f"/Heat field{max_id}.jpg",
        electric_path= file_path + pic_path + f"/Electric field{max_id}.jpg",
        e_avg=round(elec_mean, 2),
        h_avg=round(heat_mean, 2),
        e_std=round(elec_std, 3),
        h_std=round(heat_std, 3),
        max_id=max_id,
    )



# Can be modified or deleted as needed
def getTrendArrayAndMaxId(file_path):

    # TODO
    # This function is mainly for obtaining data needed for trend plotting, and also provides max_id
    # Note: data_1004 has an extra record starting from line 541, so it's temporarily broken
    actual_data = []        
    with open(file_path + "/data_1004.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            actual_data.append(line.split())
    max_data = []
    max_value = 0
    max_index = -1
    for idx, data in enumerate(actual_data):
        temp = float(data[-1])
        if temp > max_value:
            max_data = data
            max_value = temp
            max_index = idx
    print(max_index, max_value)
    print((max_data))



    # data = pd.read_csv(file_path + "/data_1004.txt", sep=" ", header=None)
    # last_column_array = data.iloc[:, -1].values
    # trend_value = last_column_array[INIT_ITERATION:]
    # current_max_value = trend_value[0]
    # max_index = -1
    # real_data = trend_value
    # for i in range(1, len(real_data)):
    #     if real_data[i] > current_max_value:
    #         current_max_value = real_data[i]
    #         max_index = i
    #     else:
    #         real_data[i] = current_max_value

    # For testing, needs to be removed
    # real_data = [1,2,3,4,5,6,7,8,8,9,9,9,10,10,10,10]
    # max_index = 13
    return max_data, max_index


# Called from pyqt5.py
def getTrendFigurePath(file_path):
    print("??")
    print(file_path)
    # real_data, _ = getTrendArrayAndMaxId(file_path)
    draw_trend(file_path, file_path + "/UI_pic")

    #use "max_heat_mean_field_value" be template

    # plt.clf()
    # plt.plot(real_data, "r-", label="objective value")
    # plt.xlabel("number of data")
    # plt.ylabel("current_max_value")

    # plt.legend()
    # plt.savefig(file_path + "/UI_pic/max_value_for_ui.png")
    # plt.clf()
    return file_path + "/UI_pic/current_max_obj.png"


if __name__ == "__main__":
    # getResult(
    #     lambda heat_path, electric_path, e_avg, h_avg, e_std, h_std, max_id,: None
    # )
    pass
