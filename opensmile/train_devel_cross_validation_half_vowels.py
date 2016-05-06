#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

updrs = [25, 69, 0, 49, 66, 42, 27, 18, 38, 52, 56, 57, 74, 71, 50, 55, 87, 24, 23, 54, 59, 21, 22, 19, 6, 48]
index_sort = [24, 18, 5, 19, 4, 7, 17, 25, 15, 1, 23, 0, 3, 10, 13, 21, 6, 14, 11, 12, 22, 8, 9, 20, 16]
version = "homoupdrs_half_vowels_attributes"
parkinson_class = ["updrs"]
audio_arff = "_vowels"
n_audios = 15
n_locutores = 25
n_grupos = 5

if os.path.exists('extract.sh'):

    # CROSS-VALIDATION

    for exp in range(len(parkinson_class)):
        for experiment in range(n_grupos):
            train = open("features/Experiment_New_Data_"+str(experiment+1)+"_"+parkinson_class[exp]+"_"+version+".train.arff", "a")
            devel = open("features/Experiment_New_Data_"+str(experiment+1)+"_"+parkinson_class[exp]+"_"+version+".devel.arff", "a")
            test = open("features/Experiment_New_Data_"+str(experiment+1)+"_"+parkinson_class[exp]+"_"+version+".test.arff", "a")
            group_train = 0
            if experiment == n_grupos-1:
                group_train = 1
            for group in range(n_grupos):
                for pacient in range(n_grupos):
                    for audio in range(n_audios):
                        if group != (n_grupos-1)-experiment:
                            if group == group_train and pacient==0 and audio==0:
                                os.system("cp features/palabras_1_" + str(index_sort[pacient+group*n_locutores/n_grupos]) + audio_arff + ".arff features/Experiment_New_Data_"+str(experiment+1)+"_"+parkinson_class[exp]+"_"+version+".train.arff")
                            else:
                                file_train = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient+group*n_locutores/n_grupos]) + audio_arff + ".arff", 'r')
                                train.write(file_train.readlines()[-1])
                                file_train.close()
                        else:
                            if pacient==0 and audio==0:
                                os.system("cp features/palabras_1_" + str(index_sort[pacient+group*n_locutores/n_grupos]) + audio_arff + ".arff features/Experiment_New_Data_"+str(experiment+1)+"_"+parkinson_class[exp]+"_"+version+".devel.arff")
                            elif pacient==0 and audio==1:
                                os.system("cp features/palabras_2_" + str(index_sort[pacient+group*n_locutores/n_grupos]) + audio_arff + ".arff features/Experiment_New_Data_"+str(experiment+1)+"_"+parkinson_class[exp]+"_"+version+".test.arff")
                            else:
                                if audio%2==0:
                                    file_devel = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient+group*n_locutores/n_grupos]) + audio_arff + ".arff", 'r')
                                    devel.write(file_devel.readlines()[-1])
                                    file_devel.close()
                                else:
                					file_test = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient+group*n_locutores/n_grupos]) + audio_arff + ".arff", 'r')
                                    test.write(file_test.readlines()[-1])
                					file_test.close()
            train.close()
            devel.close()
            test.close()

    for i in range(len(parkinson_class)):
        for n in range(n_grupos):
            os.system("cp features/Experiment_New_Data_"+str(n+1)+"_"+parkinson_class[i]+"_"+version+".train.arff ../data/")
            os.system("cp features/Experiment_New_Data_"+str(n+1)+"_"+parkinson_class[i]+"_"+version+".devel.arff ../data/")
            os.system("cp features/Experiment_New_Data_"+str(n+1)+"_"+parkinson_class[i]+"_"+version+".test.arff ../data/")

else:
    f = open("print.dep", "a")
    f.write("The bash script extract.sh has not been created")
    f.close()
