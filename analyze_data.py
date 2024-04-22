import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data_1004.txt', sep=' ', header=None)
#Model1_Waveport1_Phase, Model1_Waveport1_frequency, Model1_Waveport1_power, Model1_Waveport2_Phase, Model1_Waveport2_frequency, Model1_Waveport2_power
data.columns = ["M1_W1_Phase", "M1_W1_Power", "M1_W2_Phase", "M1_W2_Power", "M2_W1_Phase", "M2_W1_Power", "M2_W2_Phase", "M2_W2_Power", "M3_W1_Phase", "M3_W1_Power", "M3_W2_Phase", "M3_W2_Power", 'waveport1_x', 'waveport1_y', 'waveport2_x', 'waveport2_y', "elec_mean_field", "elec_std_field", "heat_mean_field", "heat_std_field", "obj_val"]

# average_value = data["average"].values
# std_value = data["std"].values
# objective_value = data["Objective_value"].values

elec_mean_field_value = data["elec_mean_field"].values
elec_std_field_value = data["elec_std_field"].values
heat_mean_field_value = data["heat_mean_field"].values
heat_std_field_value = data["heat_std_field"].values
# obj_val = data["obj_val"].values

# current_max_value = objective_value[0]
# current_average = average_value[0]
# current_std = std_value[0]

current_elec_mean_field_value = elec_mean_field_value[0]
current_elec_std_field_value = elec_std_field_value[0]
current_heat_mean_field_value = heat_mean_field_value[0]
current_heat_std_field_value = heat_std_field_value[0]

max_index = -1
real_data = objective_value
real_avg = average_value
real_std = std_value
for i in range(1,len(current_elec_mean_field_value)):
    # if real_data[i] > current_max_value:
    #     current_max_value = real_data[i]
    #     current_average = real_avg[i]
    #     current_std = real_std[i]
    #     max_index = i
    # else:
    #     real_data[i] = current_max_value
    #     real_avg[i] = current_average
    #     real_std[i] = current_std
    if elec_mean_field_value[i] > current_elec_mean_field_value:
        current_elec_mean_field_value = elec_mean_field_value[i]
        current_elec_std_field_value = elec_std_field_value[i]
    else:
        elec_mean_field_value[i] = current_elec_mean_field_value
        elec_std_field_value[i] = current_elec_std_field_value

    if heat_mean_field_value[i] > current_heat_mean_field_value:
        current_heat_mean_field_value = heat_mean_field_value[i]
        current_heat_std_field_value = heat_std_field_value[i]        
    else:
        heat_mean_field_value[i] = current_heat_mean_field_value
        heat_std_field_value[i] = current_heat_std_field_value

# print(f"Max index {max_index}, max_value {real_data[max_index]},  average {real_avg[max_index]}, std {real_std[max_index]}")

PATH = "./trend_plot/"


plt.plot(real_data,'g-',label = 'max_elec_mean_field_value')
plt.xlabel("number of data")
plt.ylabel("max_elec_mean_field_value")
plt.legend()
plt.savefig(PATH + "max_elec_mean_field_value.png")
plt.show()

plt.plot(real_data,'g-',label = 'max_elec_std_field_value')
plt.xlabel("number of data")
plt.ylabel("max_elec_std_field_value")
plt.legend()
plt.savefig(PATH + "max_elec_std_field_value.png")
plt.show()


plt.plot(real_data,'r-',label = 'max_heat_mean_field_value')
plt.xlabel("number of data")
plt.ylabel("max_heat_mean_field_value")
plt.legend()
plt.savefig(PATH + "max_heat_mean_field_value.png")
plt.show()

plt.plot(real_data,'r-',label = 'max_heat_std_field_value')
plt.xlabel("number of data")
plt.ylabel("max_heat_std_field_value")
plt.legend()
plt.savefig(PATH + "max_heat_std_field_value.png")
plt.show()



# plt.plot(real_avg,'b-',label = 'average')
# plt.xlabel("number of data")
# plt.ylabel("current_max_average")
# plt.legend()
# plt.show()

# plt.plot(real_std,'g-',label = 'std')
# plt.xlabel("number of data")
# plt.ylabel("current_max_std")
# plt.legend()
# plt.show()
