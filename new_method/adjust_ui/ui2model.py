from time import sleep
from utils import superposition
from heatmap import drawHeatMap
import pandas as pd
import matplotlib.pyplot as plt
from model import global_optimization
import os

# 最開始初始化時搜索的次數
INIT_ITERATION = 300

# 會在pyqt5.py呼叫
def run(iteration_time, material_coefficient, ETconvert_coefficient, seconds_need, data_limit, update_progress):
    # TODO 
    
    # iteration_time 預設240
    # material_coefficient 預設0.95
    # ETconvert_coefficient 預設100000
    # update_progress更新進度條，每次搜索完畢後傳入完成的次數
    # 例如，update_progress(i)

    # seconds_need 預設3，可以暫時不管
    # data_limit 預設 [[0, 360], [500, 900], [-100, 100]]
    # 為phase, power, position的上下界，也可暫時不管

    # global_optimization()
    # test
    # global_optimization(round_num=1)
    global_optimization(round_num=0)


    # 預計從這裡執行model

    # for i in range(iteration_time):
    #     sleep(2)
    #     update_progress(i)



def getResult(drawOutput, file_path):
    _, max_id = getTrendArrayAndMaxId(file_path)

    # Scan the folders in "/Data/"
    data_dir = os.path.join(file_path, "Data")
    target_folder = None
    temp_initial_count = 0
    for folder_name in os.listdir(data_dir):
        try:
            initial_count, final_count = map(int, folder_name.split('-'))
            if initial_count <= max_id <= final_count:
                target_folder = folder_name
                temp_initial_count = initial_count
                break
        except ValueError:
            continue

    if target_folder is None:
        raise ValueError(f"No suitable folder found for max_id {max_id} in {data_dir}")


    target_folder_path = os.path.join(data_dir, target_folder)

    pic_path = file_path + "/UI_pic"
    the_id = max_id - temp_initial_count
    print("the_id : ", the_id)
    print("max_id : ", max_id)
    # Call the superposition function
    elec_mean, elec_std, heat_mean, heat_std, val = superposition(target_folder_path, the_id*3, 100000, 0.95)
    
    plt.clf()

    drawHeatMap(file_path, "/Data1", pic_path, 0, max_id, elec_mean, elec_std, heat_mean, heat_std)
    
    plt.clf()

    drawOutput(
        heat_path= pic_path + f"/Heat field{max_id}.jpg",
        electric_path= pic_path + f"/Electric field{max_id}.jpg",
        e_avg=round(elec_mean, 2),
        h_avg=round(heat_mean, 2),
        e_std=round(elec_std, 2),
        h_std=round(heat_std, 2),
        max_id=max_id,
    )



# 視情況可以隨便改或刪除
def getTrendArrayAndMaxId(file_path):

    # TODO
    # 這個函數主要是為了獲得畫趨勢圖所需的數據，順便給出max_id
    # 由於data_1004從第541行開始多了1筆資料所以暫時壞了

    data = pd.read_csv(file_path + "/data_1004.txt", sep=" ", header=None)
    last_column_array = data.iloc[:, -1].values
    trend_value = last_column_array[INIT_ITERATION:]
    current_max_value = trend_value[0]
    max_index = -1
    real_data = trend_value
    for i in range(1, len(real_data)):
        if real_data[i] > current_max_value:
            current_max_value = real_data[i]
            max_index = i
        else:
            real_data[i] = current_max_value

    # 測試用，需移除
    # real_data = [1,2,3,4,5,6,7,8,8,9,9,9,10,10,10,10]
    # max_index = 13
    return real_data, max_index


# 會在pyqt5.py呼叫
def getTrendFigurePath(file_path):
    # 畫趨勢圖，回傳絕對路徑
    # 做的事可能類似analyze_data.py
    # 但由於該檔案沒有寫成函數，暫時先自己畫
    
    real_data, _ = getTrendArrayAndMaxId(file_path)

    plt.clf()
    plt.plot(real_data, "r-", label="objective value")
    plt.xlabel("number of data")
    plt.ylabel("current_max_value")

    plt.legend()
    plt.savefig(file_path + "/UI pic/max_value_for_ui.png")
    plt.clf()
    return file_path + "/UI pic/max_value_for_ui.png"


if __name__ == "__main__":
    # getResult(
    #     lambda heat_path, electric_path, e_avg, h_avg, e_std, h_std, max_id,: None
    # )
    pass
