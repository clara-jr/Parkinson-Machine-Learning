#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

updrs = [1, 2, 0, 1, 2, 2, 1, 0, 0, 2, 1, 2, 3, 1, 2, 2, 2, 0, 0, 3, 2, 0, 1, 0, 0, 0]
index_sort = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
n_audios = 48
version = "leave_half_two"
parkinson_class = "updrs"
leave = 2

if os.path.exists('extract.sh'):

    for p in range(len(updrs)):
        for a in range(n_audios+1):
            if not os.path.exists("features/palabras_" + str(a+1) + "_" + str(p) + "_"+parkinson_class+".arff"):
                os.system("./extract.sh palabras_" + str(a+1) + "_" + str(p) + ".ch1.wav palabras_" + str(a+1) + "_" + str(p) + "_"+parkinson_class+".arff "+ str(updrs[p]))

    # LEAVE-1/2-two

    for pacient_devel in range(len(index_sort)):
        pacient_train_inic = 0
        if pacient_devel != len(index_sort)-1:
            train = open("features/Experiment_New_Data_"+str(index_sort[pacient_devel])+"_"+str(index_sort[pacient_devel+1])+"_"+version+".train.arff", "a")
            devel = open("features/Experiment_New_Data_"++str(index_sort[pacient_devel])+"_"+str(index_sort[pacient_devel+1])+"_"+version+".devel.arff", "a") # audios impares 1-47
            test = open("features/Experiment_New_Data_"++str(index_sort[pacient_devel])+"_"+str(index_sort[pacient_devel+1])+"_"+version+".test.arff", "a") # audios pares 2-48
            os.system("cp features/palabras_1_" + str(index_sort[pacient_devel]) + "_"+parkinson_class+".arff features/Experiment_New_Data_"+str(index_sort[pacient_devel])+"_"+version+".devel.arff")
            os.system("cp features/palabras_2_" + str(index_sort[pacient_devel]) + "_"+parkinson_class+".arff features/Experiment_New_Data_"+str(index_sort[pacient_devel])+"_"+version+".test.arff")
            for pacient in range(leave):
                for audio in range(n_audios):
                    if pacient == 0:
                        if audio != 0 and audio != 1:
            				if audio%2==0:
                                file_devel = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient_devel]) + "_"+parkinson_class+".arff", 'r')
            					devel.write(file_devel.readlines()[-1])
            					file_devel.close()
            				else:
            					file_test = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient_devel]) + "_"+parkinson_class+".arff", 'r')
            					test.write(file_test.readlines()[-1])
            					file_test.close()
                    else:
                        if audio%2==0:
                            file_devel = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient_devel+1]) + "_"+parkinson_class+".arff", 'r')
                            devel.write(file_devel.readlines()[-1])
                            file_devel.close()
                        else:
                            file_test = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient_devel+1]) + "_"+parkinson_class+".arff", 'r')
                            test.write(file_test.readlines()[-1])
                            file_test.close()
                devel.close()
                test.close()
            if pacient_devel != 0:
                os.system("cp features/palabras_1_0_"+parkinson_class+".arff features/Experiment_New_Data_"+str(index_sort[pacient_devel])+"_"+str(index_sort[pacient_devel+1])+"_"+version+".train.arff")
            else:
                pacient_train_inic = 2
                os.system("cp features/palabras_1_3_"+parkinson_class+".arff features/Experiment_New_Data_"+str(index_sort[pacient_devel])+"_"+str(index_sort[pacient_devel+1])+"_"+version+".train.arff")
            for pacient_train in range(len(index_sort)):
                if pacient_train != pacient_devel and pacient_train != pacient_devel+1:
                    if pacient_train != pacient_train_inic:
                        for audio in range(n_audios):
                            file_train = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient_train]) + "_"+parkinson_class+".arff", 'r')
                            train.write(file_train.readlines()[-1])
                            file_train.close()
                    else:
                        for audio in range(n_audios):
                            if audio != 0:
                                file_train = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient_train]) + "_"+parkinson_class+".arff", 'r')
                                train.write(file_train.readlines()[-1])
                                file_train.close()
            train.close()

    for pacient in range(len(index_sort)):
        if pacient != len(index_sort)-1:
            os.system("cp features/Experiment_New_Data_"+str(index_sort[pacient])+"_"+str(index_sort[pacient+1])+"_"+version+".train.arff ../data/")
            os.system("cp features/Experiment_New_Data_"+str(index_sort[pacient])+"_"+str(index_sort[pacient+1])+"_"+version+".devel.arff ../data/")
            os.system("cp features/Experiment_New_Data_"+str(index_sort[pacient])+"_"+str(index_sort[pacient+1])+"_"+version+".test.arff ../data/")

else:
    f = open("print.dep", "a")
    f.write("The bash script extract.sh has not been created")
    f.close()
