#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import scipy
from scipy import stats
import math

os.system("rm print_new_data_spearman_medium_vowels.dep")
pred_file = ["SVR_half_vowels", "SVR_half_vowels_attributes"]
algorithms = ["SVR", "SVR"]
n_locutores = 25
n_grupos = 5

for n in range(len(algorithms)):
    for group in range(n_grupos):
        if n == 0:
            FEATURE = "Experiment_New_Data_"+str(group+1)+"_updrs_homoupdrs_half_vowels"
        else:
            FEATURE = "Experiment_New_Data_"+str(group+1)+"_updrs_homoupdrs_half_vowels_attributes"
        if group == 0:
            algorithms[n] = "SVR.C0.0001.L0.3.test"
        elif group == 1:
            algorithms[n] = "SVR.C0.001.L0.9.test"
        elif group == 2:
            algorithms[n] = "SVR.C0.001.L1.0.test"
        elif group == 3:
            algorithms[n] = "SVR.C1e-05.L0.8.test"
        else:
            algorithms[n] = "SVR.C0.0001.L0.9.test"
        if os.path.exists('eval/train_devel/'+FEATURE+'.'+algorithms[n]+'.pred'):
            if group == 0:
                os.system("cp eval/train_devel/"+FEATURE+"."+algorithms[n]+".pred print_new_data_spearman_medium_"+pred_file[n]+".pred")
            else:
                file = open('eval/train_devel/'+FEATURE+'.'+algorithms[n]+'.pred', 'r')
                pred = open('print_new_data_spearman_medium_'+pred_file[n]+'.pred', 'a')
                data = file.readlines();
                for x in data:
                    line = x.split(" ");
                    line_rel = []
                    for l in range(len(line)):
                        if line[l] != '':
                            line_rel.append(line[l])
                    if len(line_rel) == 5:
                        pred.write(x)
                file.close()
                pred.close()
    if os.path.exists('print_new_data_spearman_medium_'+pred_file[n]+'.pred'):
        file = open('print_new_data_spearman_medium_'+pred_file[n]+'.pred', 'r')
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
        for ini in range(n_locutores):
            pred_locutor.append(0)
            valor_locutor.append(0)
            rmse_locutor.append(0)
        for locutor in range(n_locutores):
            valor_locutor[locutor] = valor[(len(pred)/n_locutores)*locutor]
            for p in range(len(pred)/n_locutores):
                pred_locutor[locutor] += pred[p+(len(pred)/n_locutores)*locutor]/(len(pred)/n_locutores)
                rmse_locutor[locutor] += err[p+(len(pred)/n_locutores)*locutor]*err[p+(len(pred)/n_locutores)*locutor]/(len(pred)/n_locutores)
            err_locutor_abs.append(abs(valor_locutor[locutor]-pred_locutor[locutor]))
            err_locutor_rel.append(abs(valor_locutor[locutor]-pred_locutor[locutor])/valor_locutor[locutor])
            rmse_locutor[locutor] = math.sqrt(rmse_locutor[locutor])
        err_abs = 0
        err_rel = 0
        rmse = 0
        for locutor in range(n_locutores):
            err_abs += err_locutor_abs[locutor]/n_locutores
            err_rel += err_locutor_rel[locutor]/n_locutores
            rmse += rmse_locutor[locutor]/n_locutores
        s = scipy.stats.spearmanr(valor_locutor, pred_locutor)
        if math.isnan(float(s[0])):
            s = [0]
        file.close()
        f = open("print_new_data_spearman_medium_vowels.dep", "a")
        f.write("Results with " + pred_file[n] + "\n")
        f.write("Spearman correlation coefficient: " + str(s[0]) + "\n")
        f.write("REAL: " + str(valor_locutor) + "\n")
        f.write("PREDICTION: " + str(pred_locutor) + "\n")
        f.write("RMSE: " + str(rmse) + "\n")
        f.write("ABSOLUTE ERROR: " + str(err_abs) + "\n")
        f.write("RELATIVE ERROR: " + str(err_rel) + "\n")
        f.write("-------------------------------------------------------------------" + "\n" + "\n")
        f.close()
