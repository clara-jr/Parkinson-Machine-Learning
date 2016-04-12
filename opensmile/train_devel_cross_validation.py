#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

updrs = [25, 69, 0, 49, 66, 42, 27, 18, 38, 52, 56, 57, 74, 71, 50, 55, 87, 24, 23, 54, 59, 21, 22, 19, 6, 48]
hoenhyahr = [2, 2, 0, 2.5, 2.5, 2, 2, 2, 2, 2.5, 2, 3, 4, 2, 2, 2, 5, 2, 1, 3, 4, 2, 2, 2, 2, 2]
index_sort = [25, 12, 5, 11, 23, 24, 13, 15, 14, 19, 22, 7, 4, 21, 9, 10, 1, 17, 0, 20, 8, 3, 6, 18, 16]
parkinson_class = ["updrs", "hoenhyahr"]

if os.path.exists('extract.sh'):

    # WAV2ARFF

    os.system("rm print.dep")
    for p in range(len(updrs)):
        for a in range(49):
            f = open("print.dep", "a")
            f.write("Converting audio " + str(a+1) + " of pacient " + str(p) + "\n")
            f.close()
            for i in range(len(parkinson_class)):
                # ./extract.sh wav_file feat_file class
                if i == 0:
                    os.system("./extract.sh palabras_" + str(a+1) + "_" + str(p) + ".ch1.wav palabras_" + str(a+1) + "_" + str(p) + "_updrs.arff "+ str(updrs[p]))
                else:
                    os.system("./extract.sh palabras_" + str(a+1) + "_" + str(p) + ".ch1.wav palabras_" + str(a+1) + "_" + str(p) + "_hoenhyahr.arff "+ str(hoenhyahr[p]))

                if p==0 and a==0:
                    os.system("cp features/palabras_1_0_"+parkinson_class[i]+".arff features/Experiment_New_Data_all_"+parkinson_class[i]+".train.arff")
                else:
                    if p != 2:
                        data = open("features/Experiment_New_Data_all_"+parkinson_class[i]+".train.arff", "a")
                        file = open("features/palabras_" + str(a+1) + "_" + str(p) + "_" + parkinson_class[i] + ".arff", 'r')
                        data.write(file.readlines()[-1])
                        file.close()
                #os.system("rm features/palabras_" + str(a+1) + "_" + str(p) + ".arff")

    data.close()
    os.system("cp features/Experiment_New_Data_all_updrs.train.arff features/Experiment_New_Data_all_updrs.devel.arff")
    os.system("cp features/Experiment_New_Data_all_hoenhyahr.train.arff features/Experiment_New_Data_all_hoenhyahr.devel.arff")

    # CROSS-VALIDATION

    for exp in range(len(parkinson_class)):
        for experiment in range(5):
            train = open("features/Experiment_New_Data_"+str(experiment+1)+"_"+parkinson_class[exp]+".train.arff", "a")
            devel = open("features/Experiment_New_Data_"+str(experiment+1)+"_"+parkinson_class[exp]+".devel.arff", "a")
            group_train = 0
            if experiment == 4:
                group_train = 1
            for group in range(5):
                for pacient in range(5):
                    for audio in range(48):
                        if group != 4-experiment:
                            if group == group_train and pacient==0 and audio==0:
                                os.system("cp features/palabras_1_" + str(index_sort[pacient+group*5]) + "_" + parkinson_class[exp] + ".arff features/Experiment_New_Data_"+str(experiment+1)+"_"+parkinson_class[exp]+".train.arff")
                            else:
                                file = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient+group*5]) + "_" + parkinson_class[exp] + ".arff", 'r')
                                train.write(file.readlines()[-1])
                                file.close()
                        else:
                            if pacient==0 and audio==0:
                                os.system("cp features/palabras_1_" + str(index_sort[pacient+group*5]) + "_" + parkinson_class[exp] + ".arff features/Experiment_New_Data_"+str(experiment+1)+"_"+parkinson_class[exp]+".devel.arff")
                            else:
                                file = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient+group*5]) + "_" + parkinson_class[exp] + ".arff", 'r')
                                devel.write(file.readlines()[-1])
                                file.close()
            train.close()
            devel.close()

    for i in range(len(parkinson_class)):
        os.system("cp features/Experiment_New_Data_all_"+parkinson_class[i]+".train.arff ../data/")
        os.system("cp features/Experiment_New_Data_all_"+parkinson_class[i]+".devel.arff ../data/")
        for n in range(5):
            os.system("cp features/Experiment_New_Data_"+str(n+1)+"_"+parkinson_class[i]+".train.arff ../data/")
            os.system("cp features/Experiment_New_Data_"+str(n+1)+"_"+parkinson_class[i]+".devel.arff ../data/")

else:
    f = open("print.dep", "a")
    f.write("The bash script extract.sh has not been created")
    f.close()
