#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import scipy
from scipy import stats
import math

parkinson_class = ["updrs"]
parkinson_experiments = ["1", "2", "3", "4", "5"]
n_locutores = 25
n_grupos = [5, 5, 5, 5, 5]
version = "homoupdrs"
script_bash = ["baseline_linearregression_arff.sh", "baseline_simplelinearregression_arff.sh", "baseline_zeror_arff.sh"]
algorithms = ["LinearRegression", "SimpleLinearRegression", "ZeroR"]
os.system("rm print_new_data_algorithms_"+version+".dep")

for n in range(len(script_bash)):

    if os.path.exists(script_bash[n]):

        for park_class in range(len(parkinson_class)):

            for group in range(len(parkinson_experiments)):

                FEATURE = "Experiment_New_Data_"+str(group+1)+"_"+parkinson_class[park_class]+"_"+version
                bash = "./"+script_bash[n]+ " " + FEATURE
                f = open("print_new_data_algorithms_"+version+".dep", "a")
                f.write("Training " + bash + "\n")
                f.close()
                os.system(bash)

                if os.path.exists('eval/train_devel/'+FEATURE+'.'+algorithms[n]+'.pred'):
                    file = open('eval/train_devel/'+FEATURE+'.'+algorithms[n]+'.pred', 'r')
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
                    f = open("print_new_data_algorithms_"+version+".dep", "a")
                    f.write("Spearman correlation coefficient: " + str(s[0]) + "\n")
                    f.write("REAL: " + str(valor_locutor) + "\n")
                    f.write("PREDICTION: " + str(pred_locutor) + "\n")
                    f.write("RMSE: " + str(rmse) + "\n")
                    f.write("ABSOLUTE ERROR: " + str(err_abs) + "\n")
                    f.write("RELATIVE ERROR: " + str(err_rel) + "\n")
                    f.close()

        f = open("print_new_data_algorithms_"+version+".dep", "a")
        f.write("-------------------------------------------------------------------" + "\n" + "\n")
        f.close()

    else:
        f = open("print_new_data_algorithms_"+version+".dep", "a")
        f.write("The bash script "+script_bash[n]+" has not been created")
        f.close()
