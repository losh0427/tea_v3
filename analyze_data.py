import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data_1016_change.txt', sep=' ', header=None)
#Model1_Waveport1_Phase, Model1_Waveport1_frequency, Model1_Waveport1_power, Model1_Waveport2_Phase, Model1_Waveport2_frequency, Model1_Waveport2_power
data.columns = ["M1_W1_Phase", "M1_W1_freq", "M1_W1_Power", "M1_W2_Phase", "M1_W2_freq", "M1_W2_Power", "M2_W1_Phase", "M2_W1_freq", "M2_W1_Power", "M2_W2_Phase", "M2_W2_freq", "M2_W2_Power", "M3_W1_Phase", "M3_W1_freq", "M3_W1_Power", "M3_W2_Phase", "M3_W2_freq", "M3_W2_Power", 'waveport1_x', 'waveport1_y', 'waveport2_x', 'waveport2_y', "Objective_value", "average", "std"]

average_value = data["average"].values
std_value = data["std"].values
objective_value = data["Objective_value"].values


current_max_value = objective_value[0]
current_average = average_value[0]
current_std = std_value[0]
max_index = -1
real_data = objective_value
real_avg = average_value
real_std = std_value
for i in range(1,len(real_data)):
    if real_data[i] > current_max_value:
        current_max_value = real_data[i]
        current_average = real_avg[i]
        current_std = real_std[i]
        max_index = i
    else:
        real_data[i] = current_max_value
        real_avg[i] = current_average
        real_std[i] = current_std

print(f"Max index {max_index}, max_value {real_data[max_index]},  average {real_avg[max_index]}, std {real_std[max_index]}")



plt.plot(real_data,'r-',label = 'objective value')
plt.xlabel("number of data")
plt.ylabel("current_max_value")

plt.legend()
plt.savefig("./max_value.png")
plt.show()


plt.plot(real_avg,'b-',label = 'average')
plt.xlabel("number of data")
plt.ylabel("current_max_average")
plt.legend()
plt.show()

plt.plot(real_std,'g-',label = 'std')
plt.xlabel("number of data")
plt.ylabel("current_max_std")
plt.legend()
plt.show()
