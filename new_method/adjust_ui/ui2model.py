from time import sleep
from utils import superposition
from heatmap import drawHeatMap
import pandas as pd
import matplotlib.pyplot as plt
from model import global_optimization
from analyze_data import draw_trend
import os

# 最開始初始化時搜索的次數
INIT_ITERATION = 300

# 會在pyqt5.py呼叫
def run(iteration_time, material_coefficient, ETconvert_coefficient, seconds_need, data_limit, update_progress):

    global_optimization(round_num=80)
    # sleep(5)
    update_progress(5)




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



def getTrendArrayAndMaxId(file_path):
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
    return max_data, max_index


# 會在pyqt5.py呼叫
def getTrendFigurePath(file_path):
    print("??")
    print(file_path)
    draw_trend(file_path, file_path + "/UI_pic")

    return file_path + "/UI_pic/current_max_obj.png"


if __name__ == "__main__":
    pass
