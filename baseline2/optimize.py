#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import math

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

params = [1.0E-3, 1.0] # [C, L]
init = [1.0E-5, 0.1]
end = [1.0, 1.0]
step = [9.0E-5, 0.1]
experiments = [14, 10] # C = 0.00001 0.0001 0.001 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; L = 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0

FEATURE = "ComParE2015_Parkinson"
# FEATURE = "New_Data_all"

if os.path.exists('baseline_svm_arff.sh'):

    os.system("rm print.dep")

    for cont in range(len(params)):
        values = []
        spearman = []
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
        f = open("print.dep", "a")
        f.write("Training " + parallel + "\n")
        f.close()
        os.system(parallel)
        for exp in range(experiments[cont]):
            params[cont] = values[exp]
            if os.path.exists('eval/train_devel/'+FEATURE+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.result'):
                file = open('eval/train_devel/'+FEATURE+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.result', 'r')
                data = file.readlines();
                for x in data:
                    line = x.split(" ");
                s = line[len(line)-1]
                spearman.append(float(s))
                file.close()
                f = open("print.dep", "a")
                f.write("Results for model C="+str(params[0])+" L="+str(params[1]) + "\n")
                f.write("Spearman correlation coefficient: " + s + "\n")
                f.close()
            else:
                spearman.append(0)
                f = open("print.dep", "a")
                f.write("The result file for C="+str(params[0])+" and L="+str(params[1])+" has not been created" + "\n")
                f.close()
        index = spearman.index(max(spearman))
        params[cont] = values[index]

    f = open("print.dep", "a")
    f.write("Optimal C = " + str(params[0]) + "\n")
    f.write("Optimal L = " + str(params[1]) + "\n")

    f.write("Retraining final model C = " + str(params[0]) + " and L = " + str(params[1]) + "\n")
    f.close()
    os.system('./baseline_svm_arff.sh '+str(params[0])+' '+str(params[1]))
    file = open('eval/train_devel/'+FEATURE+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.pred', 'r')
    data = file.readlines();
    err = []
    valor = []
    for x in data:
        line = x.split(" ");
        line_rel = []
        for l in range(len(line)):
            if line[l] != '':
                line_rel.append(line[l])
        if len(line_rel) == 5:
            valor.append(float(line_rel[1]))
            err.append(float(line_rel[3]))
    error = 0
    rmse = 0
    for e in range(len(err)):
        error += abs(err[e])/(valor[e]*len(err))
        rmse += err[e]*err[e]/len(err)
    rmse = math.sqrt(rmse)
    file.close()
    file = open('eval/train_devel/'+FEATURE+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.result', 'r')
    data = file.readlines();
    for x in data:
        line = x.split(" ");
    s = line[len(line)-1]
    spearman.append(float(s))
    file.close()
    f = open("print.dep", "a")
    f.write("Spearman correlation coefficient final: " + s + "\n")
    f.write("RMSE: " + str(rmse) + "\n")
    f.write("RELATIVE ERROR: " + str(error) + "\n")

    f.write("Retraining initial model C = 0.001 and L = 1.0" + "\n")
    f.close()
    os.system('./baseline_svm_arff.sh 0.001 1.0')
    file = open('eval/train_devel/'+FEATURE+'.SVR.C0.001.L1.0.pred', 'r')
    data = file.readlines();
    err = []
    valor = []
    for x in data:
        line = x.split(" ");
        line_rel = []
        for l in range(len(line)):
            if line[l] != '':
                line_rel.append(line[l])
        if len(line_rel) == 5:
            valor.append(float(line_rel[1]))
            err.append(float(line_rel[3]))
    error = 0
    rmse = 0
    for e in range(len(err)):
        error += abs(err[e])/(valor[e]*len(err))
        rmse += err[e]*err[e]/len(err)
    rmse = math.sqrt(rmse)
    file.close()
    file = open('eval/train_devel/'+FEATURE+'.SVR.C0.001.L1.0.result', 'r')
    data = file.readlines();
    for x in data:
        line = x.split(" ");
    s = line[len(line)-1]
    spearman.append(float(s))
    file.close()
    f = open("print.dep", "a")
    f.write("Spearman correlation coefficient initial: " + s + "\n")
    f.write("RMSE: " + str(rmse) + "\n")
    f.write("RELATIVE ERROR: " + str(error) + "\n")

else:
    f = open("print.dep", "a")
    f.write("The bash script baseline_svm_arff.sh has not been created")
    f.close()
