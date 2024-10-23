from time import sleep
# from utils import superposition
# from heatmap import drawHeatMap
import pandas as pd
import matplotlib.pyplot as plt
# from model import global_optimization
# from analyze_data import draw_trend
import os
import random


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
    # global_optimization(round_num=0)    
    # global_optimization(round_num=80)
    # sleep(5)
    update_progress(5)


    # 預計從這裡執行model

    # for i in range(iteration_time):
    #     sleep(2)
    #     update_progress(i)



def getResult(drawOutput, file_path):
# 從data_1004.txt抓取最後五行數據
    data = pd.read_csv(os.path.join(file_path, 'data_1004.txt'), sep=" ", header=None)
    last_five_rows = data.tail(5)

    elec_mean = last_five_rows.iloc[-1, 0]
    elec_std = last_five_rows.iloc[-1, 1]
    heat_mean = last_five_rows.iloc[-1, 2]
    heat_std = last_five_rows.iloc[-1, 3]
    val = last_five_rows.iloc[-1, 4]

    # 隨機選擇一組圖片
    random_index = random.randint(0, 19)
    heat_img_path = os.path.join(file_path, f"Heatmaps/Heat field_{random_index}.jpg")
    electric_img_path = os.path.join(file_path, f"Heatmaps/Electric field_{random_index}.jpg")

    # 更新 drawOutput 的顯示
    drawOutput(
        heat_path=heat_img_path,
        electric_path=electric_img_path,
        e_avg=round(elec_mean, 2),
        h_avg=round(heat_mean, 2),
        e_std=round(elec_std, 3),
        h_std=round(heat_std, 3),
        max_id=random_index,
    )





# 會在pyqt5.py呼叫
def getTrendFigurePath(file_path):
# 繪製趨勢圖
    # draw_trend(file_path, os.path.join(file_path, "output_trend_plots"))

    # 隨機選擇一個 trend plot 作為輸出
    random_index = random.randint(0, 19)
    trend_plot_path = os.path.join(file_path, f"output_trend_plots/trend_plot_{random_index}.png")

    return trend_plot_path

if __name__ == "__main__":
    # getResult(
    #     lambda heat_path, electric_path, e_avg, h_avg, e_std, h_std, max_id,: None
    # )
    pass
