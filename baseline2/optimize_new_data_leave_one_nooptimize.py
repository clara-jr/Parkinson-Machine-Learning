#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import math

index_sort = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

# Parameters:
# C: c -- The complexity parameter C.(default 1.0).
# L: epsilonParameter -- The epsilon parameter of the epsilon insensitive loss function.(default 0.001).

if os.path.exists('baseline_svm_arff.sh'):
    os.system("rm print_new_data_leave_one_nooptimize.dep")
    for pacient in range(len(index_sort)):
        params = [1.0E-3, 0.8] # [C, L]
        FEATURE = "Experiment_New_Data_"+str(index_sort[pacient])+"_leave_one"
        bash = "./baseline_svm_arff.sh " + str(params[0]) + " " + str(params[1]) + " " + FEATURE
        f = open("print_new_data_leave_one_nooptimize.dep", "a")
        f.write("Training " + bash + "\n")
        f.close()
        os.system(bash)
        if os.path.exists('eval/train_devel/'+FEATURE+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.pred'):
            file = open('eval/train_devel/'+FEATURE+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.pred', 'r')
            data = file.readlines();
            valor = 0
            pred = []
            err = []
            for x in data:
                line = x.split(" ");
                line_rel = []
                for l in range(len(line)):
                    if line[l] != '':
                        line_rel.append(line[l])
                if len(line_rel) == 5:
                    valor = float(line_rel[1])
                    pred.append(float(line_rel[2]))
                    err.append(float(line_rel[3]))
            error = 0
            pred_medium = 0
            for p in range(len(pred)):
                pred_medium += pred[p]/len(pred)
            error = abs(pred_medium-valor)/valor
            rmse = 0
            for e in range(len(err)):
                rmse += err[e]*err[e]/len(pred)
                err[e] = abs(err[e])
            rmse = math.sqrt(rmse)
            index_min = err.index(min(err))
            index_max = err.index(max(err))
            file.close()
            f = open("print_new_data_leave_one_nooptimize.dep", "a")
            f.write("UPDRS: " + str(valor) + "\n")
            f.write("PREDICTION: " + str(pred_medium) + "\n")
            f.write("RMSE: " + str(rmse) + "\n")
            f.write("ABSOLUTE ERROR: " + str(abs(pred_medium-valor)) + "\n")
            f.write("RELATIVE ERROR final: " + str(error) + "\n")
            f.write("Best result with audio: " + str(index_min+1) + " Relative error: " + str(err[index_min]/valor) + "\n")
            f.write("Worst result with audio: " + str(index_max+1) + " Relative error: " + str(err[index_max]/valor) + "\n")
            f.close()
        else:
            f = open("print_new_data_leave_one_nooptimize.dep", "a")
            f.write("The pred file for C="+str(params[0])+" and L="+str(params[1])+" has not been created" + "\n")
            f.close()
else:
    f = open("print_new_data_leave_one_nooptimize.dep", "a")
    f.write("The bash script baseline_svm_arff.sh has not been created")
    f.close()
