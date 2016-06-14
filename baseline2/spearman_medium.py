#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import scipy
from scipy import stats
import math

os.system("rm print_new_data_spearman_leave_half_without_medium.dep")
algorithms = ["SVR.C1e-05.L0.9.test", "SVR.C0.0001.L1.0.test", "", "SVR.C0.001.L0.9.test", "SVR.C0.0001.L1.0.test", "SVR.C1e-05.L1.0.test", "SVR.C0.001.L0.1.test", "SVR.C1e-05.L0.7.test", "SVR.C1e-05.L0.7.test", "SVR.C0.001.L0.2.test", "SVR.C1e-05.L0.1.test", "SVR.C1e-05.L1.0.test", "SVR.C0.001.L0.1.test", "SVR.C0.001.L1.0.test", "SVR.C0.001.L0.7.test", "SVR.C1e-05.L0.1.test", "SVR.C1e-05.L0.1.test", "SVR.C1e-05.L0.9.test", "SVR.C0.001.L0.3.test", "SVR.C0.001.L1.0.test", "SVR.C0.001.L1.0.test", "SVR.C1e-05.L0.8.test", "SVR.C1e-05.L0.7.test", "SVR.C1e-05.L0.8.test", "SVR.C0.0001.L0.2.test", "SVR.C1e-05.L0.1.test"]
n_locutores = 26

for pacient in range(n_locutores):
    if pacient != 2:
        FEATURE = "Experiment_New_Data_"+str(pacient)+"_leave_half"
        if os.path.exists('eval/train_devel/'+FEATURE+'.'+algorithms[pacient]+'.pred') :
            if pacient == 0:
                os.system("cp eval/train_devel/"+FEATURE+"."+algorithms[pacient]+".pred print_new_data_spearman_leave_half_without_medium.pred")
            else:
                file = open('eval/train_devel/'+FEATURE+'.'+algorithms[pacient]+'.pred', 'r')
                pred = open('print_new_data_spearman_leave_half_without_medium.pred', 'a')
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
if os.path.exists('print_new_data_spearman_leave_half_without_medium.pred'):
    file = open('print_new_data_spearman_leave_half_without_medium.pred', 'r')
    data = file.readlines();
    err_abs = []
    err_rel = []
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
            pred.append(float(line_rel[3]))
            err_abs.append(abs(float(line_rel[3])))
            err_rel.append(abs(float(line_rel[3]))/float(line_rel[1]))
    error_abs = 0
    error_rel = 0
    rmse = 0
    for audio in range(len(err_abs)):
        error_abs += err_abs[audio]/len(err_abs)
        error_rel += err_rel[audio]/len(err_rel)
        rmse += err_abs[audio]*err_abs[audio]/(len(err_abs))
    rmse = math.sqrt(rmse)
    s = scipy.stats.spearmanr(valor, pred)
    file.close()
    f = open("print_new_data_spearman_leave_half_without_medium.dep", "a")
    f.write("Spearman correlation coefficient: " + str(s[0]) + "\n")
    f.write("RMSE: " + str(rmse) + "\n")
    f.write("ABSOLUTE ERROR: " + str(error_abs) + "\n")
    f.write("RELATIVE ERROR: " + str(error_rel) + "\n")
    f.close()
