#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import math

index_sort = [25, 12, 5, 11, 23, 24, 13, 15, 14, 19, 22, 7, 4, 21, 9, 10, 1, 17, 0, 20, 8, 3, 6, 18, 16]

# Parameters:
# C: c -- The complexity parameter C.(default 1.0).
# L: epsilonParameter -- The epsilon parameter of the epsilon insensitive loss function.(default 0.001).

# Process:
# L = 1.0 static -> Find optimal C -> C = optimal C static -> Find optimal L -> Final Result

# range with float step

def frange(start, stop, step=1.0):
    while start < stop:
        yield start
        start +=step
        if start >= 0.1:
            step = 0.1
        else:
            step *= 10

# Greedy - Find optimal parameter C for L=1.0 static -> Find optimal parameter L for C=optimalC static

if os.path.exists('baseline_train_devel_new_data.sh'):

    for pacient in range(len(index_sort)):

        params = [1.0E-3, 1.0] # [C, L]
        init = [1.0E-5, 0.1]
        end = [1.0, 1.0]
        step = [9.0E-5, 0.1]
        experiments = [14, 10] # C = 0.00001 0.0001 0.001 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; L = 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0

        os.system("rm print_new_data_"+str(index_sort[pacient])+"_leave_one.dep")
        FEATURE = "Experiment_New_Data_"+str(index_sort[pacient])+"_leave_one"

        for cont in range(len(params)):
            values = []
            err_comparison = []
            string = []
            parallel = "parallel -j " + str(experiments[cont]) + " ./baseline_train_devel_new_data.sh {1} {2} " + FEATURE
            for i in range(len(params)):
                string.append(" ::: " + str(params[i]))
            string[cont] = " :::"
            for param in frange(init[cont], end[cont], step[cont]):
                values.append(param)
                string[cont] += " " + str(param)
            for i in range(len(params)):
                parallel += string[i]
            f = open("print_new_data_"+str(index_sort[pacient])+"_leave_one.dep", "a")
            f.write("Training " + parallel + "\n")
            f.close()
            os.system(parallel)
            for exp in range(experiments[cont]):
                params[cont] = values[exp]
                if os.path.exists('eval/train_devel/Experiment_New_Data_'+str(index_sort[pacient])+'_leave_one.SVR.C'+str(params[0])+'.L'+str(params[1])+'.pred'):
                    file = open('eval/train_devel/Experiment_New_Data_'+str(index_sort[pacient])+'_leave_one.SVR.C'+str(params[0])+'.L'+str(params[1])+'.pred', 'r')
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
                        pred_medium += pred[p]/48
                    error = abs(pred_medium-valor)/valor
                    err_comparison.append(float(error))
                    rmse = 0
                    for e in range(len(err)):
                        rmse += err[e]*err[e]/48
                    rmse = math.sqrt(rmse)
                    file.close()
                    f = open("print_new_data_"+str(index_sort[pacient])+"_leave_one.dep", "a")
                    f.write("Results for model C="+str(params[0])+" L="+str(params[1]) + "\n")
                    f.write("UPDRS: " + str(valor) + "\n")
                    f.write("PREDICTION: " + str(pred_medium) + "\n")
                    f.write("RMSE: " + str(rmse) + "\n")
                    f.write("ABSOLUTE ERROR: " + str(abs(pred_medium-valor)) + "\n")
                    f.write("RELATIVE ERROR: " + str(error) + "\n")
                    f.close()
                else:
                    err_comparison.append(100)
                    f = open("print_new_data_"+str(index_sort[pacient])+"_leave_one.dep", "a")
                    f.write("The pred file for C="+str(params[0])+" and L="+str(params[1])+" has not been created" + "\n")
                    f.close()
            index = err_comparison.index(min(err_comparison))
            params[cont] = values[index]

        f = open("print_new_data_"+str(index_sort[pacient])+"_leave_one.dep", "a")
        f.write("Optimal C = " + str(params[0]) + "\n")
        f.write("Optimal L = " + str(params[1]) + "\n")

        f.write("Retraining final model C = " + str(params[0]) + " and L = " + str(params[1]) + "\n")
        f.close()
        os.system('./baseline_train_devel_new_data.sh '+str(params[0])+' '+str(params[1])+' '+FEATURE)
        file = open('eval/train_devel/Experiment_New_Data_'+str(index_sort[pacient])+'_leave_one.SVR.C'+str(params[0])+'.L'+str(params[1])+'.pred', 'r')
        data = file.readlines();
        valor = 0
        pred = []
        for x in data:
            line = x.split(" ");
            line_rel = []
            for l in range(len(line)):
                if line[l] != '':
                    line_rel.append(line[l])
            if len(line_rel) == 5:
                valor = float(line_rel[1])
                pred.append(float(line_rel[2]))
        error = 0
        pred_medium = 0
        for p in range(len(pred)):
            pred_medium += pred[p]/48
        error = abs(pred_medium-valor)/valor
        rmse = 0
        for e in range(len(err)):
            rmse += err[e]*err[e]/48
        rmse = math.sqrt(rmse)
        file.close()
        f = open("print_new_data_"+str(index_sort[pacient])+"_leave_one.dep", "a")
        f.write("UPDRS: " + str(valor) + "\n")
        f.write("PREDICTION: " + str(pred_medium) + "\n")
        f.write("RMSE: " + str(rmse) + "\n")
        f.write("ABSOLUTE ERROR: " + str(abs(pred_medium-valor)) + "\n")
        f.write("RELATIVE ERROR final: " + str(error) + "\n")

        f.write("Retraining initial model C = 0.001 and L = 1.0" + "\n")
        f.close()
        os.system('./baseline_train_devel_new_data.sh 0.001 1.0 '+FEATURE)
        file = open('eval/train_devel/Experiment_New_Data_'+str(index_sort[pacient])+'_leave_one.SVR.C0.001.L1.0.pred', 'r')
        data = file.readlines();
        valor = 0
        pred = []
        for x in data:
            line = x.split(" ");
            line_rel = []
            for l in range(len(line)):
                if line[l] != '':
                    line_rel.append(line[l])
            if len(line_rel) == 5:
                valor = float(line_rel[1])
                pred.append(float(line_rel[2]))
        error = 0
        pred_medium = 0
        for p in range(len(pred)):
            pred_medium += pred[p]/48
        error = abs(pred_medium-valor)/valor
        rmse = 0
        for e in range(len(err)):
            rmse += err[e]*err[e]/48
        rmse = math.sqrt(rmse)
        file.close()
        f = open("print_new_data_"+str(index_sort[pacient])+"_leave_one.dep", "a")
        f.write("UPDRS: " + str(valor) + "\n")
        f.write("PREDICTION: " + str(pred_medium) + "\n")
        f.write("RMSE: " + str(rmse) + "\n")
        f.write("ABSOLUTE ERROR: " + str(abs(pred_medium-valor)) + "\n")
        f.write("RELATIVE ERROR initial: " + str(error) + "\n")
        f.close()

else:
    f = open("print_new_data.dep", "a")
    f.write("The bash script baseline_train_devel_new_data.sh has not been created")
    f.close()
