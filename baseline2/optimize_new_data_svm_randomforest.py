#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

# range with float step SVM

def frange(start, stop, step=1.0):
    while start < stop:
        yield start
        start +=step
        if start >= 0.1:
            step = 0.1
        else:
            step *= 10

# range with float step RandomForest

def frange2(start, stop, step=1.0):
    while start < stop:
        yield start
        start +=step

for group in range(5):

    TRAIN = "New_Data_"+str(group+1)+"_v2"
    results = []
    number_results = []
    os.system("rm print_new_data_svm_randomforest_"+str(group+1)+".dep")

    # SVM

    # Parameters:
    # C: c -- The complexity parameter C.(default 1.0).
    # L: epsilonParameter -- The epsilon parameter of the epsilon insensitive loss function.(default 0.001).

    # Process:
    # L = 1.0 static -> Find optimal C -> C = optimal C static -> Find optimal L -> Final Result

    # Greedy - Find optimal parameter C for L=1.0 static -> Find optimal parameter L for C=optimalC static

    params = [1.0E-3, 1.0] # [C, L]
    init = [1.0E-5, 0.1]
    end = [1.0, 1.0]
    step = [9.0E-5, 0.1]
    experiments = [14, 10] # C = 0.00001 0.0001 0.001 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; L = 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0

    if os.path.exists("baseline_svm_arff.sh"):

        for cont in range(len(params)):
            values = []
            spearman = []
            string = []
            parallel = "parallel -j " + str(experiments[cont]) + " ./baseline_svm_arff.sh {1} {2} " + TRAIN
            for i in range(len(params)):
                string.append(" ::: " + str(params[i]))
            string[cont] = " :::"
            for param in frange(init[cont], end[cont], step[cont]):
                values.append(param)
                string[cont] += " " + str(param)
            for i in range(len(params)):
                parallel += string[i]
            f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
            f.write("Training " + parallel + "\n" + "\n")
            f.close()
            os.system(parallel)
            for exp in range(experiments[cont]):
                params[cont] = values[exp]
                if os.path.exists('eval/train_devel/'+TRAIN+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.result'):
                    file = open('eval/train_devel/'+TRAIN+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.result', 'r')
                    data = file.readlines();
                    for x in data:
                        line = x.split(" ");
                    s = line[len(line)-1]
                    spearman.append(float(s))
                    file.close()
                    f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
                    f.write("Results for model C="+str(params[0])+" L="+str(params[1]) + "\n")
                    f.write("Spearman correlation coefficient: " + s + "\n")
                    f.close()
                else:
                    spearman.append(0)
                    f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
                    f.write("The result file for C="+str(params[0])+" and L="+str(params[1])+" has not been created" + "\n")
                    f.close()
            index = spearman.index(max(spearman))
            params[cont] = values[index]

        f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
        f.write("Optimal C = " + str(params[0]) + "\n")
        f.write("Optimal L = " + str(params[1]) + "\n")

        f.write("Retraining final model C = " + str(params[0]) + " and L = " + str(params[1]) + "\n")
        f.close()
        os.system('./baseline_svm_arff.sh '+str(params[0])+' '+str(params[1])+' '+TRAIN)
        file = open('eval/train_devel/'+TRAIN+'.SVR.C'+str(params[0])+'.L'+str(params[1])+'.result', 'r')
        data = file.readlines();
        for x in data:
            line = x.split(" ");
        s = line[len(line)-1]
        file.close()
        f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
        f.write("Spearman correlation coefficient final: " + s + "\n")

        results.append("SVM C = "+str(params[0])+" L = "+str(params[1])+" Spearman correlation coefficient = "+s)
        number_results.append(float(s))

        f.write("Retraining initial model C = 0.001 and L = 1.0" + "\n")
        f.close()
        os.system('./baseline_svm_arff.sh 0.001 1.0 '+TRAIN)
        file = open('eval/train_devel/'+TRAIN+'.SVR.C0.001.L1.0.result', 'r')
        data = file.readlines();
        for x in data:
            line = x.split(" ");
        s = line[len(line)-1]
        file.close()
        f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
        f.write("Spearman correlation coefficient initial: " + s + "\n")
        f.close()

    else:
        f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
        f.write("The bash script baseline_svm_arff.sh has not been created")
        f.close()

    f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
    f.write("-------------------------------------------------------------------" + "\n" + "\n")
    f.close()

    # ARFF and LIBSVM RandomForest

    # Parameters:
    # I: numTrees -- The number of trees to be generated.
    # S: seed -- The random number seed to be used.

    # Greedy

    params = [100, 1]
    init = [100, 1]
    end = [501, 11]
    step = [50, 1]
    experiments = [9, 10]

    if os.path.exists("baseline_randomforest_arff.sh"):

        for cont in range(len(params)):
            values = []
            spearman = []
            string = []
            parallel = "parallel -j " + str(experiments[cont]) + " ./baseline_randomforest_arff.sh {1} {2} " + TRAIN
            for i in range(len(params)):
                string.append(" ::: " + str(params[i]))
            string[cont] = " :::"
            for param in frange2(init[cont], end[cont], step[cont]):
                values.append(param)
                string[cont] += " " + str(param)
            for i in range(len(params)):
                parallel += string[i]
            f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
            f.write("Training " + parallel + "\n" + "\n")
            f.close()
            os.system(parallel)
            for exp in range(experiments[cont]):
                params[cont] = values[exp]
                if os.path.exists('eval/train_devel/'+TRAIN+'.RandomForest.I'+str(params[0])+'.S'+str(params[1])+'.result'):
                    file = open('eval/train_devel/'+TRAIN+'.RandomForest.I'+str(params[0])+'.S'+str(params[1])+'.result', 'r')
                    data = file.readlines();
                    for x in data:
                        line = x.split(" ");
                    s = line[len(line)-1]
                    spearman.append(float(s))
                    file.close()
                    f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
                    f.write("Results for model I="+str(params[0])+" S="+str(params[1])+"\n")
                    f.write("Spearman correlation coefficient: " + s + "\n")
                    f.close()
                else:
                    spearman.append(0)
                    f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
                    f.write("The result file for I="+str(params[0])+" S="+str(params[1])+"\n")
                    f.close()
            index = spearman.index(max(spearman))
            params[cont] = values[index]

        f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
        f.write("Optimal I = " + str(params[0]) + "\n")
        f.write("Optimal S = " + str(params[1]) + "\n")

        f.write("Retraining final model I="+str(params[0])+" S="+str(params[1])+"\n")
        f.close()
        os.system("./baseline_randomforest_arff.sh "+str(params[0])+" "+str(params[1])+" "+TRAIN)
        file = open('eval/train_devel/'+TRAIN+'.RandomForest.I'+str(params[0])+'.S'+str(params[1])+'.result', 'r')
        data = file.readlines();
        for x in data:
            line = x.split(" ");
        s = line[len(line)-1]
        file.close()
        f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
        f.write("Spearman correlation coefficient final: " + s)

        results.append("RandomForest I = "+str(params[0])+" S = "+str(params[1])+" Spearman correlation coefficient = "+s)
        number_results.append(float(s))

        f.write("Retraining initial model I=100 S=1 \n")
        f.close()
        os.system("./baseline_randomforest_arff.sh 100 1 "+TRAIN)
        file = open('eval/train_devel/'+TRAIN+'.RandomForest.I100.S1.result', 'r')
        data = file.readlines();
        for x in data:
            line = x.split(" ");
        s = line[len(line)-1]
        file.close()
        f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
        f.write("Spearman correlation coefficient initial: " + s)
        f.close()

    else:
        f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
        f.write("The bash script baseline_randomforest_arff.sh has not been created")
        f.close()

    f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
    f.write("-------------------------------------------------------------------" + "\n" + "\n")
    f.close()

    final_index = number_results.index(max(number_results))
    f = open("print_new_data_svm_randomforest_"+str(group+1)+".dep", "a")
    f.write(results[final_index])
    f.close()
