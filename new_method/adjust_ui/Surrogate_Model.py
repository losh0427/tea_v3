import smt
import numpy as np
from smt.applications.mixed_integer import(
    FLOAT,
    ORD,
    ENUM,
    MixedIntegerSamplingMethod,
    MixedIntegerSurrogateModel,
    GOWER,
    MixedIntegerContext,
)
from smt.sampling_methods import LHS, Random, FullFactorial
from smt.surrogate_models import LS, QP, KPLS, KRG, KPLSK, GEKPLS, MGP
import matplotlib.pyplot as plt
import random
import csv
import pickle
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessRegressor
#from RBF_discrete import SequenceKernel
import time
from sklearn.svm import SVR


class Surrogate_model():
    def __init__(self, search_time , input_bound, heat_coeff, item_coeff):
        self.phase = [0, 360]
        self.Power = [500, 900]
        self.position = [-100, 100]
        self.number_of_parameter = 18
        self.SAMPLING_SIZE = 800
        self.Power_MINIMUM = 500
        self.Power_MAXIMUM  = 900
        self.sampling_num = 30
        self.xtypes = [FLOAT for _ in range(16)]
        self.xlimits = input_bound
        self.mixint = MixedIntegerContext(self.xtypes, self.xlimits)
        self.train_x = []
        self.train_y = []
        self.sorted_index_list = []
        self.search_time = search_time
        self.total_sampling_num = 0
        self.heat_coeff = heat_coeff
        self.item_coeff = item_coeff

    def sort_list_index(self):
        origin_list = [(value, i) for i, value in enumerate(self.train_y)]
        sorted_list = sorted(origin_list, key=lambda x: x[0], reverse=True)
        self.sorted_index_list = [index for _, index in sorted_list]

    def build(self, data_path):
        start_time = time.time()
        with open(data_path, 'r') as f:
            for line in f.readlines():
                s = line.split(' ')
                s[0] = float(s[0])
                s[1] = float(s[1])
                s[2] = float(s[2])
                s[3] = float(s[3])
                s[4] = float(s[4])
                s[5] = float(s[5])
                s[6] = float(s[6])
                s[7] = float(s[7])
                s[8] = float(s[8])
                s[9] = float(s[9])
                s[10] = float(s[10])
                s[11] = float(s[11])
                s[12] = float(s[12])
                s[13] = float(s[13])
                s[14] = float(s[14])
                s[15] = float(s[15])

                self.train_x.append(s[0:16])
                self.train_y.append(int(float(s[-1])))
        self.train_x = np.array(self.train_x)
        self.train_y = np.array(self.train_y)
        self.sort_list_index()
        # traing model
        self.Mymodel = self.mixint.build_surrogate_model(KRG(print_global=False))
        self.Mymodel.set_training_values(self.train_x, self.train_y)
        self.Mymodel.train()
        with open('surrogate_model_sec.pkl','wb') as f:
            pickle.dump(self.Mymodel, f)
        #self.secondModel = self.mixint.build_surrogate_model(MGP(print_global=False))
        self.secondModel = self.mixint.build_surrogate_model(KPLS(print_global=False))
        self.secondModel.set_training_values(self.train_x, self.train_y)
        self.secondModel.train()
        end_time = time.time()
        self.search_time -= (end_time - start_time)




    def global_sampling(self):
        sampling_method = self.mixint.build_sampling_method(Random)
        sampling_value = sampling_method(self.sampling_num)
        # print(f"sampling_value: {sampling_value}")
        return sampling_value

    def medium_sampling(self):
        medium_xtypes = [FLOAT, FLOAT, FLOAT, FLOAT, FLOAT, FLOAT, FLOAT, FLOAT, FLOAT, FLOAT, FLOAT, FLOAT, FLOAT, FLOAT, FLOAT, FLOAT]
        bound = [[] for j in range(16)]

        top_indices = self.sorted_index_list[:10]
        for top_index in top_indices:
            for i in range(16):
                bound[i].append(self.train_x[top_index][i])

        medium_xlimits = [[min(bound[0]),max(bound[0])],  [min(bound[1]),max(bound[1])], [min(bound[2]),max(bound[2])], [min(bound[3]),max(bound[3])], [min(bound[4]),max(bound[4])], [min(bound[5]),max(bound[5])], [min(bound[6]),max(bound[6])], [min(bound[7]),max(bound[7])], [min(bound[8]),max(bound[8])], [min(bound[9]),max(bound[9])], [min(bound[10]),max(bound[10])], [min(bound[11]),max(bound[11])], [min(bound[12]),max(bound[12])], [min(bound[13]),max(bound[13])], [min(bound[14]),max(bound[14])], [min(bound[15]),max(bound[15])]]
        medium_mixint = MixedIntegerContext(medium_xtypes, medium_xlimits)
        sampling_method = medium_mixint.build_sampling_method(Random)
        sampling_value = sampling_method(self.sampling_num)
        # print(f"sampling_value: {str(sampling_value)}")
        return sampling_value

    def local_sampling(self):
        top_indices = self.sorted_index_list[:5]
        candidate_sampling = []
        # print(f"train_x top 1: {str(self.train_x[top_indices])}")
        for top_index in top_indices:
            
            k = int(self.sampling_num/5) 
            for j in range(k):
                sampling = [0] * 16
                for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
                    sampling[i] = float(self.train_x[top_index][i]) + random.uniform(-10, 10)
                for i in [12, 13, 14, 15]:
                    sampling[i] = float(self.train_x[top_index][i]) + random.uniform(-0.5, 0.5)
                candidate_sampling.append(sampling)
        return candidate_sampling

    # TODO: infill criteria
    def sampling(self, iteration):
        # if iteration < 80:
        #     self.sampling_num = 30
        # elif iteration >= 80 and iteration < 160:
        #     self.sampling_num = 20
        # else:
        #     self.sampling_num = 10
        self.sampling_num = 30
        if iteration % 5 == 1:
            # print("global sample")
            candidate_sampling = self.global_sampling()
        elif iteration % 5 ==  3:
            # print("medium sample")
            candidate_sampling = self.medium_sampling()
        elif iteration % 5 == 0 or iteration % 5 == 2 or iteration % 5 == 4:
            # print("local sample")
            candidate_sampling = self.local_sampling()
        # candidate_sampling = self.local_sampling()
        return candidate_sampling

    #TODO : choose point into Ansys
    def find_max(self, iteration):
        if iteration % 5 == 1:
            print("global sample")
        elif iteration % 5 ==  3:
            print("medium sample")
        elif iteration % 5 == 0 or iteration % 5 == 2 or iteration % 5 == 4:
            print("local sample")
        max_val = 0
        second_model_max_val = 0
        tmp_test_x_first = None
        tmp_test_x_second = None

        search_start_time = time.time()
        test_x = np.array(self.sampling(iteration))
        test_y = self.Mymodel.predict_values(test_x)
        second_test_y = self.secondModel.predict_values(test_x)
        self.total_sampling_num += len(test_x)
        for i in range(len(test_y)):
            if test_y[i] > max_val:
                # check the parameters are all in the range
                # out_flag = False
                # for j in range(16):
                #     if test_x[i][j] < self.xlimits[j][0] or test_x[i][j] > self.xlimits[j][1]:
                #         out_flag = True
                #         break
                # if out_flag == True:
                #     continue
                max_val = test_y[i]
                tmp_test_x_first = test_x[i]
        for i in range(len(second_test_y)):
            if second_test_y[i] > second_model_max_val:
                # check the parameters are all in the range
                # out_flag = False
                # for j in range(16):
                #     if test_x[i][j] < self.xlimits[j][0] or test_x[i][j] > self.xlimits[j][1]:
                #         out_flag = True
                #         break
                # if out_flag == True:
                #     continue
                second_model_max_val = second_test_y[i]
                tmp_test_x_second = test_x[i]
        search_end_time = time.time()
        self.search_time -= (search_end_time - search_start_time)

        while self.search_time > 0:
            search_start_time = time.time()
            test_x = np.array(self.sampling(iteration))
            test_y = self.Mymodel.predict_values(test_x)
            second_test_y = self.secondModel.predict_values(test_x)
            for i in range(len(test_y)):
                if test_y[i] > max_val:
                    # check the parameters are all in the range
                    # out_flag = False
                    # for j in range(16):
                    #     if test_x[i][j] < self.xlimits[j][0] or test_x[i][j] > self.xlimits[j][1]:
                    #         out_flag = True
                    #         break
                    # if out_flag == True:
                    #     continue
                    max_val = test_y[i]
                    tmp_test_x_first = test_x[i]
            for i in range(len(second_test_y)):
                if second_test_y[i] > second_model_max_val:
                    # check the parameters are all in the range
                    # out_flag = False
                    # for j in range(16):
                    #     if test_x[i][j] < self.xlimits[j][0] or test_x[i][j] > self.xlimits[j][1]:
                    #         out_flag = True
                    #         break
                    # if out_flag == True:
                    #     continue
                    second_model_max_val = second_test_y[i]
                    tmp_test_x_second = test_x[i]
            search_end_time = time.time()
            self.search_time -= (search_end_time - search_start_time)
            self.total_sampling_num += len(test_x)
        # if max_index == second_model_max_index :
        #         tmp = test_x[max_index].tolist()
        #         tmp.append(float(max_val))
        #         return [tmp]
        # else :
        #     newPoint1 = test_x[max_index].tolist()
        #     newPoint1.append(float(max_val))

        #     newPoint2 = test_x[second_model_max_index].tolist()
        #     newPoint2.append(float(second_model_max_val))
        #     return [newPoint1,newPoint2]
        # if the tmp_test_x_first and tmp_test_x_second are the same, return one point
        if np.array_equal(tmp_test_x_first, tmp_test_x_second):
            tmp = tmp_test_x_first.tolist()
            tmp.append(float(max_val))
            return [tmp]
        else:
            newPoint1 = tmp_test_x_first.tolist()
            newPoint1.append(float(max_val))
            newPoint2 = tmp_test_x_second.tolist()
            newPoint2.append(float(second_model_max_val))
            return [newPoint1, newPoint2]
        
        
    def export_result(self, logger):
        with open('C:/Users/USER/Desktop/Tea_second/Code_v3/Full_Flow/surrogate_result.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile,delimiter=',')
            writer.writerow(logger)


if __name__ == '__main__':
    data_path = "./Full_Flow/data_1004.txt"
    model = Surrogate_model()
    model.build(data_path)
    parameters = model.find_max(1)
