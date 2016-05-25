#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

updrs_predicho = [44.5765, 42.69375, 0, 45.106, 46.6026, 41.7765, 43.696, 41.914, 46.254, 43.93, 46.81, 37.348, 60.828, 43.9188, 50.557, 46.625, 46.14, 39.685, 45.7432, 40.278, 46.477, 41.5266, 41.2944, 41.711, 28.774, 45.453]
hy = [2, 2, 0, 2.5, 2.5, 2, 2, 2, 2, 2.5, 2, 3, 4, 2, 2, 2, 5, 2, 1, 3, 4, 2, 2, 2, 2, 2]
edad = [70, 64, 0, 64, 67, 78, 67, 63, 50, 77, 57, 68, 59, 62, 68, 65, 80, 66, 70, 75, 79, 69, 54, 73, 57, 45]
dif_edad = [13, 19, 0, 7, 6, 3, 7, 8, 21, 8, 24, 10, 14, 6, 3, 17, 11, 10, 1, 10, 24, 17, 12, 8, 5, 6]
sexo = ['H', 'H', '', 'H', 'M', 'H', 'H', 'H', 'M', 'M', 'M', 'H', 'H', 'H', 'H', 'M', 'H', 'H', 'M', 'H', 'M', 'H', 'H', 'H', 'H', 'M']
updrs = [25, 69, 0, 49, 66, 42, 27, 18, 38, 52, 56, 57, 74, 71, 50, 55, 87, 24, 23, 54, 59, 21, 22, 19, 6, 48]
index_sort = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

for p in range(len(index_sort)):
    arff_train = open("features/Ensemble_Learning_" + str(index_sort[p]) + ".train.arff", 'a')
    arff_train.write("@relation openSMILE_features \n \n@attribute updrs numeric \n@attribute hy {1, 1.5, 2, 2.5, 3, 4, 5} \n@attribute edad numeric \n@attribute tiempo_enfermedad numeric \n@attribute sexo {'M', 'H'} \n@attribute class numeric \n \n@data \n \n")
    for p_train in range(len(index_sort)):
        # todos menos paciente index_sort[p]
        if index_sort[p_train] != index_sort[p]:
            arff_train.write(str(updrs_predicho[index_sort[p_train]]) + "," + str(hy[index_sort[p_train]]) + "," + str(edad[index_sort[p_train]]) + "," + str(dif_edad[index_sort[p_train]]) + ",'" + sexo[index_sort[p_train]] + "'," + str(updrs[index_sort[p_train]]) + "\n")
    arff_train.close()
    arff_devel = open("features/Ensemble_Learning_" + str(index_sort[p]) + ".devel.arff", 'a')
    arff_devel.write("@relation openSMILE_features \n \n@attribute updrs numeric \n@attribute hy {1, 1.5, 2, 2.5, 3, 4, 5} \n@attribute edad numeric \n@attribute tiempo_enfermedad numeric \n@attribute sexo {'M', 'H'} \n@attribute class numeric \n \n@data \n \n")
    # paciente index_sort[p]
    arff_devel.write(str(updrs_predicho[index_sort[p]]) + "," + str(hy[index_sort[p]]) + "," + str(edad[index_sort[p]]) + "," + str(dif_edad[index_sort[p]]) + ",'" + sexo[index_sort[p]] + "'," + str(updrs[index_sort[p]]) + "\n")
    arff_devel.close()

for p in range(len(index_sort)):
    os.system("cp features/Ensemble_Learning_" + str(index_sort[p]) + ".train.arff ../data/")
    os.system("cp features/Ensemble_Learning_" + str(index_sort[p]) + ".devel.arff ../data/")
