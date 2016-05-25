#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import math

index_sort = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

# Parameters:
# C: c -- The complexity parameter C.(default 1.0).
# L: epsilonParameter -- The epsilon parameter of the epsilon insensitive loss function.(default 0.001).

if os.path.exists('baseline_linearregression_arff.sh'):
    for pacient in range(len(index_sort)):
        os.system("rm print_new_data_ensemble_learning_"+str(index_sort[pacient])+".dep")
        FEATURE = "Ensemble_Learning_"+str(index_sort[pacient])
        bash = "./baseline_linearregression_arff.sh " + FEATURE
        f = open("print_new_data_ensemble_learning_"+str(index_sort[pacient])+".dep", "a")
        f.write("Training " + bash + "\n")
        f.close()
        os.system(bash)
        if os.path.exists('eval/train_devel/'+FEATURE+'.LinearRegression.pred'):
            file = open('eval/train_devel/'+FEATURE+'.LinearRegression.pred', 'r')
            data = file.readlines();
            valor = 0
            pred = 0
            err = 0
            err_rel = 0
            for x in data:
                line = x.split(" ");
                line_rel = []
                for l in range(len(line)):
                    if line[l] != '':
                        line_rel.append(line[l])
                if len(line_rel) == 5:
                    valor = float(line_rel[1])
                    pred = float(line_rel[2])
                    err = float(line_rel[3])
            err_rel = err/valor
            file.close()
            f = open("print_new_data_ensemble_learning_"+str(index_sort[pacient])+".dep", "a")
            f.write("UPDRS: " + str(valor) + "\n")
            f.write("PREDICTION: " + str(pred) + "\n")
            f.write("ABSOLUTE ERROR: " + str(abs(err)) + "\n")
            f.write("RELATIVE ERROR final: " + str(abs(err_rel)) + "\n")
            f.close()
        else:
            f = open("print_new_data_ensemble_learning_"+str(index_sort[pacient])+".dep", "a")
            f.write("The pred file has not been created" + "\n")
            f.close()
else:
    f = open("print_new_data_ensemble_learning_"+str(index_sort[pacient])+".dep", "a")
    f.write("The bash script baseline_linearregression_arff.sh has not been created")
    f.close()
