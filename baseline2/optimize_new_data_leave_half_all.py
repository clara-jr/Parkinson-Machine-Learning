#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import math
import scipy
from scipy import stats

version = "leave_half_all_elasso"
n_locutores_half = 25

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

if os.path.exists('baseline_svm_libsvm.sh'):

    params = [1.0E-3, 1.0] # [C, L]
    init = [1.0E-5, 0.1]
    end = [1.0, 1.0]
    step = [9.0E-5, 0.1]
    experiments = [14, 10] # C = 0.00001 0.0001 0.001 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; L = 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0

    os.system("rm print_new_data_"+version+".dep")
    FEATURE = "Experiment_New_Data_"+version

    for cont in range(len(params)):
        values = []
        spearman_comparison = []
        string = []
        parallel = "parallel -j " + str(experiments[cont]) + " ./baseline_svm_libsvm.sh {1} {2} " + FEATURE
        for i in range(len(params)):
            string.append(" ::: " + str(params[i]))
        string[cont] = " :::"
        for param in frange(init[cont], end[cont], step[cont]):
            values.append(param)
            string[cont] += " " + str(param)
        for i in range(len(params)):
            parallel += string[i]
        f = open("print_new_data_"+version+".dep", "a")
        f.write("Training " + parallel + "\n")
        f.close()
        os.system(parallel)
        for exp in range(experiments[cont]):
            params[cont] = values[exp]
            if os.path.exists('eval/train_devel/Experiment_New_Data_'+version+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.pred'):
                file = open('eval/train_devel/Experiment_New_Data_'+version+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.pred', 'r')
                data = file.readlines();
                valor = []
                pred = []
                err = []
                for x in data:
                    line = x.split(" ");
                    line_rel = []
                    for l in range(len(line)):
                        if line[l] != '':
                            line_rel.append(line[l])
                    if len(line_rel) == 5:
                        valor.append(float(line_rel[1]))
                        pred.append(float(line_rel[2]))
                        err.append(float(line_rel[3]))
                pred_locutor = []
                valor_locutor = []
                for ini in range(n_locutores_half):
                    pred_locutor.append(0)
                    valor_locutor.append(0)
                error_rel = 0
                error_abs = 0
                for locutor in range(n_locutores_half):
                    valor_locutor[locutor] = valor[(len(pred)/n_locutores_half)*locutor]
                    for p in range(len(pred)/n_locutores_half):
                        pred_locutor[locutor] += pred[p+(len(pred)/n_locutores_half)*locutor]/(len(pred)/n_locutores_half)
                    error_abs += abs(pred_locutor[locutor]-valor_locutor[locutor])/n_locutores_half
                    error_rel += (abs(pred_locutor[locutor]-valor_locutor[locutor])/valor_locutor[locutor])/n_locutores_half
                s = scipy.stats.spearmanr(valor_locutor, pred_locutor)
                if math.isnan(float(s[0])):
                    s = [0]
                spearman_comparison.append(float(s[0]))
                rmse = 0
                for e in range(len(err)):
                    rmse += err[e]*err[e]/len(pred)
                rmse = math.sqrt(rmse)
                file.close()
                f = open("print_new_data_"+version+".dep", "a")
                f.write("Results for model C="+str(params[0])+" L="+str(params[1]) + "\n")
                f.write("REAL: " + str(valor_locutor) + "\n")
                f.write("PREDICTION: " + str(pred_locutor) + "\n")
                f.write("RMSE: " + str(rmse) + "\n")
                f.write("ABSOLUTE ERROR: " + str(error_abs) + "\n")
                f.write("RELATIVE ERROR: " + str(error_rel) + "\n")
                f.write("Spearman correlation coefficient: " + str(s[0]) + "\n")
                f.close()
            else:
                spearman_comparison.append(-1)
                f = open("print_new_data_"+version+".dep", "a")
                f.write("The pred file for C="+str(params[0])+" and L="+str(params[1])+" has not been created" + "\n")
                f.close()
        index = spearman_comparison.index(max(spearman_comparison))
        params[cont] = values[index]

    f = open("print_new_data_"+version+".dep", "a")
    f.write("Optimal C = " + str(params[0]) + "\n")
    f.write("Optimal L = " + str(params[1]) + "\n")

    f.write("Retraining final model with test set C = " + str(params[0]) + " and L = " + str(params[1]) + "\n")
    f.close()
    os.system('./baseline_svm_libsvm.sh '+str(params[0])+' '+str(params[1])+' '+FEATURE)
    file = open('eval/train_devel/Experiment_New_Data_'+version+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.test.pred', 'r')
    data = file.readlines();
    valor = []
    pred = []
    err = []
    for x in data:
        line = x.split(" ");
        line_rel = []
        for l in range(len(line)):
            if line[l] != '':
                line_rel.append(line[l])
        if len(line_rel) == 5:
            valor.append(float(line_rel[1]))
            pred.append(float(line_rel[2]))
            err.append(float(line_rel[3]))
    pred_locutor = []
    valor_locutor = []
    for ini in range(n_locutores_half):
        pred_locutor.append(0)
        valor_locutor.append(0)
    error_rel = 0
    error_abs = 0
    for locutor in range(n_locutores_half):
        valor_locutor[locutor] = valor[(len(pred)/n_locutores_half)*locutor]
        for p in range(len(pred)/n_locutores_half):
            pred_locutor[locutor] += pred[p+(len(pred)/n_locutores_half)*locutor]/(len(pred)/n_locutores_half)
        error_abs += abs(pred_locutor[locutor]-valor_locutor[locutor])/n_locutores_half
        error_rel += (abs(pred_locutor[locutor]-valor_locutor[locutor])/valor_locutor[locutor])/n_locutores_half
    s = scipy.stats.spearmanr(valor_locutor, pred_locutor)
    if math.isnan(float(s[0])):
        s = [0]
    spearman_comparison.append(float(s[0]))
    rmse = 0
    for e in range(len(err)):
        rmse += err[e]*err[e]/len(pred)
    rmse = math.sqrt(rmse)
    file.close()
    f = open("print_new_data_"+version+".dep", "a")
    f.write("Results for model C="+str(params[0])+" L="+str(params[1]) + "\n")
    f.write("REAL: " + str(valor_locutor) + "\n")
    f.write("PREDICTION: " + str(pred_locutor) + "\n")
    f.write("RMSE: " + str(rmse) + "\n")
    f.write("ABSOLUTE ERROR: " + str(error_abs) + "\n")
    f.write("RELATIVE ERROR: " + str(error_rel) + "\n")
    f.write("Spearman correlation coefficient: " + str(s[0]) + "\n")
    f.close()

else:
    f = open("print_new_data_"+version+".dep", "a")
    f.write("The bash script baseline_svm_libsvm.sh has not been created")
    f.close()
