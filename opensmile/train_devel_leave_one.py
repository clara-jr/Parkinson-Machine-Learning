#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

updrs = [25, 69, 0, 49, 66, 42, 27, 18, 38, 52, 56, 57, 74, 71, 50, 55, 87, 24, 23, 54, 59, 21, 22, 19, 6, 48]
index_sort = [25, 12, 5, 11, 23, 24, 13, 15, 14, 19, 22, 7, 4, 21, 9, 10, 1, 17, 0, 20, 8, 3, 6, 18, 16]

if os.path.exists('extract.sh'):

    # WAV2ARFF

    #os.system("rm print.dep")
    #for p in range(len(updrs)):
        #for a in range(49):
            #f = open("print.dep", "a")
            #f.write("Converting audio " + str(a+1) + " of pacient " + str(p) + "\n")
            #f.close()
            #os.system("./extract.sh palabras_" + str(a+1) + "_" + str(p) + ".ch1.wav palabras_" + str(a+1) + "_" + str(p) + ".arff "+ str(updrs[p]))

    # LEAVE-ONE

    for pacient_devel in range(len(index_sort)):
        pacient_train_inic = 0
        train = open("features/Experiment_New_Data_"+str(index_sort[pacient_devel])+"_leave_one.train.arff", "a")
        devel = open("features/Experiment_New_Data_"+str(index_sort[pacient_devel])+"_leave_one.devel.arff", "a")
        os.system("cp features/palabras_1_" + str(index_sort[pacient_devel]) + "_updrs.arff features/Experiment_New_Data_"+str(index_sort[pacient_devel])+"_leave_one.devel.arff")
        for audio in range(48):
            if audio != 0:
                file_devel = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient_devel]) + "_updrs.arff", 'r')
                devel.write(file_devel.readlines()[-1])
                file_devel.close()
        devel.close()
        if pacient_devel != 0:
            os.system("cp features/palabras_1_0_updrs.arff features/Experiment_New_Data_"+str(index_sort[pacient_devel])+"_leave_one.train.arff")
        else:
            pacient_train_inic = 1
            os.system("cp features/palabras_1_1_updrs.arff features/Experiment_New_Data_"+str(index_sort[pacient_devel])+"_leave_one.train.arff")
        for pacient_train in range(len(index_sort)):
            if pacient_train != pacient_devel:
                if pacient_train != pacient_train_inic:
                    for audio in range(48):
                        file_train = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient_train]) + "_updrs.arff", 'r')
                        train.write(file_train.readlines()[-1])
                        file_train.close()
                else:
                    for audio in range(48):
                        if audio != 0:
                            file_train = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient_train]) + "_updrs.arff", 'r')
                            train.write(file_train.readlines()[-1])
                            file_train.close()
        train.close()

    for pacient in range(len(index_sort)):
        os.system("cp features/Experiment_New_Data_"+str(index_sort[pacient])+"_leave_one.train.arff ../data/")
        os.system("cp features/Experiment_New_Data_"+str(index_sort[pacient])+"_leave_one.devel.arff ../data/")

else:
    f = open("print.dep", "a")
    f.write("The bash script extract.sh has not been created")
    f.close()
