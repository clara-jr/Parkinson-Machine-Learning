#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

updrs = [1, 2, 0, 1, 2, 2, 1, 0, 0, 2, 1, 2, 3, 1, 2, 2, 2, 0, 0, 3, 2, 0, 1, 0, 0, 0]
index_sort = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
audio_train_list = [1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 21, 22, 25, 26, 29, 30, 33, 34, 37, 38, 41, 42, 45, 46]
audio_devel_list = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47]
audio_test_list = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48]
n_audios = 48
version = "leave_half_all"
parkinson_class = "updrs"

if os.path.exists('extract.sh'):

    for p in range(len(updrs)):
        for a in range(n_audios+1):
            if not os.path.exists("features/palabras_" + str(a+1) + "_" + str(p) + "_"+parkinson_class+".arff"):
                os.system("./extract.sh palabras_" + str(a+1) + "_" + str(p) + ".ch1.wav palabras_" + str(a+1) + "_" + str(p) + "_"+parkinson_class+".arff "+ str(updrs[p]))

    # LEAVE-1/2-all

    train = open("features/Experiment_New_Data_"+version+".train.arff", "a") # audios 1,2,5,6,9,10,...45,46
    devel = open("features/Experiment_New_Data_"+version+".devel.arff", "a") # audios 3,7,11,15,19,...43,47
    test = open("features/Experiment_New_Data_"+version+".test.arff", "a") # audios 4,8,12,16,20,...44,48
    os.system("cp features/palabras_1_0_"+parkinson_class+".arff features/Experiment_New_Data_"+version+".train.arff")
    os.system("cp features/palabras_3_0_"+parkinson_class+".arff features/Experiment_New_Data_"+version+".devel.arff")
    os.system("cp features/palabras_4_0_"+parkinson_class+".arff features/Experiment_New_Data_"+version+".test.arff")

    for pacient in range(len(index_sort)):

        for audio_train in range(len(audio_train_list)):
            if pacient == 0:
                if audio_train != 0:
                    file_train = open("features/palabras_" + str(audio_train_list[audio_train]) + "_" + str(index_sort[pacient]) + "_"+parkinson_class+".arff", 'r')
					train.write(file_train.readlines()[-1])
					file_train.close()
            else:
                file_train = open("features/palabras_" + str(audio_train_list[audio_train]) + "_" + str(index_sort[pacient]) + "_"+parkinson_class+".arff", 'r')
                train.write(file_train.readlines()[-1])
                file_train.close()
        for audio_devel in range(len(audio_devel_list)):
            if pacient == 0:
                if audio_devel != 0:
                    file_devel = open("features/palabras_" + str(audio_devel_list[audio_devel]) + "_" + str(index_sort[pacient]) + "_"+parkinson_class+".arff", 'r')
					devel.write(file_devel.readlines()[-1])
					file_devel.close()
            else:
                file_devel = open("features/palabras_" + str(audio_devel_list[audio_devel]) + "_" + str(index_sort[pacient]) + "_"+parkinson_class+".arff", 'r')
                devel.write(file_devel.readlines()[-1])
                file_devel.close()
        for audio_test in range(len(audio_test_list)):
            if pacient == 0:
                if audio_test != 0:
                    file_test = open("features/palabras_" + str(audio_test_list[audio_test]) + "_" + str(index_sort[pacient]) + "_"+parkinson_class+".arff", 'r')
					test.write(file_test.readlines()[-1])
					file_test.close()
            else:
                file_test = open("features/palabras_" + str(audio_test_list[audio_test]) + "_" + str(index_sort[pacient]) + "_"+parkinson_class+".arff", 'r')
                test.write(file_test.readlines()[-1])
                file_test.close()

    train.close()
    devel.close()
    test.close()
    os.system("cp features/Experiment_New_Data_"+version+".train.arff ../data/")
    os.system("cp features/Experiment_New_Data_"+version+".devel.arff ../data/")
    os.system("cp features/Experiment_New_Data_"+version+".test.arff ../data/")

else:
    f = open("print.dep", "a")
    f.write("The bash script extract.sh has not been created")
    f.close()
