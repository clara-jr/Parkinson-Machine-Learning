#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import scipy
from scipy import stats
import math

parkinson_class = ["updrs", "hoenhyahr_categorise"]
parkinson_experiments = ["all", "1", "2", "3", "4", "5"]
n_locutores = 25
n_grupos = [1, 5, 5, 5, 5, 5]
# version = "v1"
# version = "v2"
version = "homoupdrs"

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

if os.path.exists('baseline_svm_arff.sh'):

    for park_class in range(len(parkinson_class)):

        for n in range(len(parkinson_experiments)):

            params = [1.0E-3, 1.0] # [C, L]
            init = [1.0E-5, 0.1]
            end = [1.0, 1.0]
            step = [9.0E-5, 0.1]
            experiments = [14, 10] # C = 0.00001 0.0001 0.001 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; L = 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0

            os.system("rm print_new_data_"+parkinson_experiments[n]+"_"+parkinson_class[park_class]+"_"+version+".dep")
            FEATURE = "Experiment_New_Data_"+parkinson_experiments[n]+"_"+parkinson_class[park_class]+"_"+version+""

            for cont in range(len(params)):
                values = []
                spearman_comparison = []
                string = []
                parallel = "parallel -j " + str(experiments[cont]) + " ./baseline_svm_arff.sh {1} {2} " + FEATURE
                for i in range(len(params)):
                    string.append(" ::: " + str(params[i]))
                string[cont] = " :::"
                for param in frange(init[cont], end[cont], step[cont]):
                    values.append(param)
                    string[cont] += " " + str(param)
                for i in range(len(params)):
                    parallel += string[i]
                f = open("print_new_data_"+parkinson_experiments[n]+"_"+parkinson_class[park_class]+"_"+version+".dep", "a")
                f.write("Training " + parallel + "\n")
                f.close()
                os.system(parallel)
                for exp in range(experiments[cont]):
                    params[cont] = values[exp]
                    if os.path.exists('eval/train_devel/Experiment_New_Data_'+parkinson_experiments[n]+"_"+parkinson_class[park_class]+'_'+version+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.pred'):
                        file = open('eval/train_devel/Experiment_New_Data_'+parkinson_experiments[n]+"_"+parkinson_class[park_class]+'_'+version+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.pred', 'r')
                        data = file.readlines();
                        valor = []
                        pred = []
                        for x in data:
                            line = x.split(" ");
                            line_rel = []
                            for l in range(len(line)):
                                if line[l] != '':
                                    line_rel.append(line[l])
                            if len(line_rel) == 5:
                                valor.append(float(line_rel[1]))
                                pred.append(float(line_rel[2]))
                        pred_locutor = []
                        valor_locutor = []
                        for ini in range(n_locutores/n_grupos[n]):
                            pred_locutor.append(0)
                            valor_locutor.append(0)
                        for locutor in range(n_locutores/n_grupos[n]):
                            valor_locutor[locutor] = valor[(len(pred)/(n_locutores/n_grupos[n]))*locutor]
                            for p in range(len(pred)/(n_locutores/n_grupos[n])):
                                pred_locutor[locutor] += pred[p+(len(pred)/(n_locutores/n_grupos[n]))*locutor]/(len(pred)/(n_locutores/n_grupos[n]))
                            if parkinson_class[park_class] == "hoenhyahr_categorise":
                                if round(pred_locutor[locutor]) > 7.0:
                                    pred_locutor[locutor] = 7.0
                                elif round(pred_locutor[locutor]) < 1.0:
                                    pred_locutor[locutor] = 1.0
                                else:
                                    pred_locutor[locutor] = round(pred_locutor[locutor])
                        s = scipy.stats.spearmanr(valor_locutor, pred_locutor)
                        if math.isnan(float(s[0])):
                            s = [0]
                        spearman_comparison.append(float(s[0]))
                        file.close()
                        f = open("print_new_data_"+parkinson_experiments[n]+"_"+parkinson_class[park_class]+"_"+version+".dep", "a")
                        f.write("Results for model C="+str(params[0])+" L="+str(params[1]) + "\n")
                        f.write("REAL: " + str(valor_locutor) + "\n")
                        f.write("PREDICTION: " + str(pred_locutor) + "\n")
                        f.write("Spearman correlation coefficient: " + str(s[0]) + "\n")
                        f.close()
                    else:
                        spearman_comparison.append(-1)
                        f = open("print_new_data_"+parkinson_experiments[n]+"_"+parkinson_class[park_class]+"_"+version+".dep", "a")
                        f.write("The result file for C="+str(params[0])+" and L="+str(params[1])+" has not been created" + "\n")
                        f.close()
                index = spearman_comparison.index(max(spearman_comparison))
                params[cont] = values[index]

            f = open("print_new_data_"+parkinson_experiments[n]+"_"+parkinson_class[park_class]+"_"+version+".dep", "a")
            f.write("Optimal C = " + str(params[0]) + "\n")
            f.write("Optimal L = " + str(params[1]) + "\n")

            f.write("Retraining final model C = " + str(params[0]) + " and L = " + str(params[1]) + "\n")
            f.close()
            os.system('./baseline_svm_arff.sh '+str(params[0])+' '+str(params[1])+' '+FEATURE)
            file = open('eval/train_devel/Experiment_New_Data_'+parkinson_experiments[n]+"_"+parkinson_class[park_class]+'_'+version+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.pred', 'r')
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
            err_locutor_abs = []
            err_locutor_rel = []
            rmse_locutor = []
            for ini in range(n_locutores/n_grupos[n]):
                pred_locutor.append(0)
                valor_locutor.append(0)
                rmse_locutor.append(0)
            for locutor in range((n_locutores/n_grupos[n])):
                valor_locutor[locutor] = valor[(len(pred)/(n_locutores/n_grupos[n]))*locutor]
                for p in range(len(pred)/(n_locutores/n_grupos[n])):
                    pred_locutor[locutor] += pred[p+(len(pred)/(n_locutores/n_grupos[n]))*locutor]/(len(pred)/(n_locutores/n_grupos[n]))
                    rmse_locutor[locutor] += err[p+(len(pred)/(n_locutores/n_grupos[n]))*locutor]*err[p+(len(pred)/(n_locutores/n_grupos[n]))*locutor]/(len(pred)/(n_locutores/n_grupos[n]))
                if parkinson_class[park_class] == "hoenhyahr_categorise":
                    if round(pred_locutor[locutor]) > 7.0:
                        pred_locutor[locutor] = 7.0
                    elif round(pred_locutor[locutor]) < 1.0:
                        pred_locutor[locutor] = 1.0
                    else:
                        pred_locutor[locutor] = round(pred_locutor[locutor])
                err_locutor_abs.append(abs(valor_locutor[locutor]-pred_locutor[locutor]))
                err_locutor_rel.append(abs(valor_locutor[locutor]-pred_locutor[locutor])/valor_locutor[locutor])
                rmse_locutor[locutor] = math.sqrt(rmse_locutor[locutor])
            err_abs = 0
            err_rel = 0
            rmse = 0
            for locutor in range(n_locutores/n_grupos[n]):
                err_abs += err_locutor_abs[locutor]/(n_locutores/n_grupos[n])
                err_rel += err_locutor_rel[locutor]/(n_locutores/n_grupos[n])
                rmse += rmse_locutor[locutor]/(n_locutores/n_grupos[n])
            s = scipy.stats.spearmanr(valor_locutor, pred_locutor)
            if math.isnan(float(s[0])):
                s = [0]
            file.close()
            f = open("print_new_data_"+parkinson_experiments[n]+"_"+parkinson_class[park_class]+"_"+version+".dep", "a")
            f.write("Spearman correlation coefficient final: " + str(s[0]) + "\n")
            f.write("REAL: " + str(valor_locutor) + "\n")
            f.write("PREDICTION: " + str(pred_locutor) + "\n")
            f.write("RMSE: " + str(rmse) + "\n")
            f.write("ABSOLUTE ERROR: " + str(err_abs) + "\n")
            f.write("RELATIVE ERROR: " + str(err_rel) + "\n")

            f.write("Retraining initial model C = 0.001 and L = 1.0" + "\n")
            f.close()
            os.system('./baseline_svm_arff.sh 0.001 1.0 '+FEATURE)
            file = open('eval/train_devel/Experiment_New_Data_'+parkinson_experiments[n]+"_"+parkinson_class[park_class]+'_'+version+'.SVR.C0.001.L1.0.pred', 'r')
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
            err_locutor_abs = []
            err_locutor_rel = []
            rmse_locutor = []
            for ini in range(n_locutores/n_grupos[n]):
                pred_locutor.append(0)
                valor_locutor.append(0)
                rmse_locutor.append(0)
            for locutor in range(n_locutores/n_grupos[n]):
                valor_locutor[locutor] = valor[(len(pred)/(n_locutores/n_grupos[n]))*locutor]
                for p in range(len(pred)/(n_locutores/n_grupos[n])):
                    pred_locutor[locutor] += pred[p+(len(pred)/(n_locutores/n_grupos[n]))*locutor]/(len(pred)/(n_locutores/n_grupos[n]))
                    rmse_locutor[locutor] += err[p+(len(pred)/(n_locutores/n_grupos[n]))*locutor]*err[p+(len(pred)/(n_locutores/n_grupos[n]))*locutor]/(len(pred)/(n_locutores/n_grupos[n]))
                if parkinson_class[park_class] == "hoenhyahr_categorise":
                    if round(pred_locutor[locutor]) > 7.0:
                        pred_locutor[locutor] = 7.0
                    elif round(pred_locutor[locutor]) < 1.0:
                        pred_locutor[locutor] = 1.0
                    else:
                        pred_locutor[locutor] = round(pred_locutor[locutor])
                err_locutor_abs.append(abs(valor_locutor[locutor]-pred_locutor[locutor]))
                err_locutor_rel.append(abs(valor_locutor[locutor]-pred_locutor[locutor])/valor_locutor[locutor])
                rmse_locutor[locutor] = math.sqrt(rmse_locutor[locutor])
            err_abs = 0
            err_rel = 0
            rmse = 0
            for locutor in range(n_locutores/n_grupos[n]):
                err_abs += err_locutor_abs[locutor]/(n_locutores/n_grupos[n])
                err_rel += err_locutor_rel[locutor]/(n_locutores/n_grupos[n])
                rmse += rmse_locutor[locutor]/(n_locutores/n_grupos[n])
            s = scipy.stats.spearmanr(valor_locutor, pred_locutor)
            if math.isnan(float(s[0])):
                s = [0]
            file.close()
            f = open("print_new_data_"+parkinson_experiments[n]+"_"+parkinson_class[park_class]+"_"+version+".dep", "a")
            f.write("Spearman correlation coefficient initial: " + str(s[0]) + "\n")
            f.write("REAL: " + str(valor_locutor) + "\n")
            f.write("PREDICTION: " + str(pred_locutor) + "\n")
            f.write("RMSE: " + str(rmse) + "\n")
            f.write("ABSOLUTE ERROR: " + str(err_abs) + "\n")
            f.write("RELATIVE ERROR: " + str(err_rel) + "\n")
            f.close()

else:
    f = open("print_new_data.dep", "a")
    f.write("The bash script baseline_svm_arff.sh has not been created")
    f.close()
