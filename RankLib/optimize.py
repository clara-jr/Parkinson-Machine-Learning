#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

# Parameters:
#1	[ -bag <r> ]	Number of bags (default=300)
#2 	[ -tc <k> ]	Number of threshold candidates for tree spliting. -1 to use all feature values (default=256)
#3 	[ -estop <e> ]	Stop early when no improvement is observed on validaton data in e consecutive rounds (default=100)
#4 	[ -mls <n> ]	Min leaf support -- minimum #samples each leaf has to contain (default=1)
#5 	[ -srate <r> ]	Sub-sampling rate (default=1.0)
#6 	[ -frate <r> ]	Feature sampling rate (default=0.3)
#7 	[ -tree <t> ]	Number of trees in each bag (default=1)
#8 	[ -leaf <l> ]	Number of leaves for each tree (default=100)
#9 	[ -shrinkage <factor> ]	Shrinkage, or learning rate (default=0.1)

# range with float step

def frange(start, stop, step=1.0):
    while start < stop:
        yield start
        start +=step

# Greedy

TRAIN = "ComParE2015_Parkinson_mfc18_elasso_f20.train.libsvm"
MODEL1 = TRAIN
TEST = "ComParE2015_Parkinson_mfc18_elasso_f20.devel.libsvm"

params = [300, 256, 100, 1, 1.0, 0.2, 1, 100, 0.1]
# .bag-300-tc-256-es-100-ml-1-sr-1.0-fr-0.2-tr-1-le-100-sh-0.1
# parallel -j 2 ./traintest1.sh {1} {2} {3} {4} {5} {6} {7} {8} {9} $TRAIN $TEST $MODEL1 ::: 100 200 300 ::: 200 256 312 ::: 50 100 150 ::: 1 2 3 ::: 0.5 1.0 1.5 ::: 0.1 0.2 0.3 0.4 ::: 1 2 3 ::: 50 100 150 200 ::: 0.05 0.1 0.15 0.2 0.25
init = [100, 200, 50, 1, 0.5, 0.1, 1, 50, 0.05]
end = [301, 313, 151, 4, 1.6, 0.5, 4, 201, 0.3]
step = [100, 56, 50, 1, 0.5, 0.1, 1, 50, 0.05]
experiments = [3, 3, 3, 3, 3, 4, 3, 4, 5]

if os.path.exists('traintest1.sh'):

    os.system("rm print.dep")

    for cont in range(len(params)):
        values = []
        spearman = []
        string = []
        parallel = "parallel -j " + str(experiments[cont]) + " ./traintest1.sh {1} {2} {3} {4} {5} {6} {7} {8} {9} " + TRAIN + " " + TEST + " " + MODEL1
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
            if os.path.exists('eval/train_devel/results-'+MODEL1+'.b-'+str(params[0])+'-tc-'+str(params[1])+'-es-'+str(params[2])+'-ml-'+str(params[3])+'-sr-'+str(params[4])+'-fr-'+str(params[5])+'-tr-'+str(params[6])+'-le-'+str(params[7])+'-sh-'+str(params[8])+'.dep'):
                file = open('eval/train_devel/results-'+MODEL1+'.b-'+str(params[0])+'-tc-'+str(params[1])+'-es-'+str(params[2])+'-ml-'+str(params[3])+'-sr-'+str(params[4])+'-fr-'+str(params[5])+'-tr-'+str(params[6])+'-le-'+str(params[7])+'-sh-'+str(params[8])+'.dep', 'r')
                data = file.readlines();
                for x in data:
                    line = x.split(" ");
                s = line[len(line)-1]
                spearman.append(float(s))
                file.close()
                f = open("print.dep", "a")
                f.write("Results for model BAG="+str(params[0])+" TC="+str(params[1])+" ESTOP="+str(params[2])+" MLS="+str(params[3])+" SRATE="+str(params[4])+" FRATE="+str(params[5])+" TREE="+str(params[6])+" LEAF="+str(params[7])+" SHRINKAGE="+str(params[8]) + "\n")
                f.write("Spearman correlation coefficient: " + s + "\n")
                f.close()
            else:
                spearman.append(0)
                f = open("print.dep", "a")
                f.write("The result file for BAG="+str(params[0])+" TC="+str(params[1])+" ESTOP="+str(params[2])+" MLS="+str(params[3])+" SRATE="+str(params[4])+" FRATE="+str(params[5])+" TREE="+str(params[6])+" LEAF="+str(params[7])+" SHRINKAGE="+str(params[8])+" has not been created" + "\n")
                f.close()
        index = spearman.index(max(spearman))
        params[cont] = values[index]

    f = open("print.dep", "a")
    f.write("Optimal BAG = " + str(params[0]) + "\n")
    f.write("Optimal TC = " + str(params[1]) + "\n")
    f.write("Optimal ESTOP = " + str(params[2]) + "\n")
    f.write("Optimal MLS = " + str(params[3]) + "\n")
    f.write("Optimal SRATE = " + str(params[4]) + "\n")
    f.write("Optimal FRATE = " + str(params[5]) + "\n")
    f.write("Optimal TREE = " + str(params[6]) + "\n")
    f.write("Optimal LEAF = " + str(params[7]) + "\n")
    f.write("Optimal SHRINKAGE = " + str(params[8]) + "\n")

    f.write("Retraining final model BAG="+str(params[0])+" TC="+str(params[1])+" ESTOP="+str(params[2])+" MLS="+str(params[3])+" SRATE="+str(params[4])+" FRATE="+str(params[5])+" TREE="+str(params[6])+" LEAF="+str(params[7])+" SHRINKAGE="+str(params[8]) + "\n")
    f.close()
    os.system("./traintest1.sh "+str(params[0])+" "+str(params[1])+" "+str(params[2])+" "+str(params[3])+" "+str(params[4])+" "+str(params[5])+" "+str(params[6])+" "+str(params[7])+" "+str(params[8])+" "+TRAIN+" "+TEST+" "+MODEL1)
    file = open('eval/train_devel/results-'+MODEL1+'.b-'+str(params[0])+'-tc-'+str(params[1])+'-es-'+str(params[2])+'-ml-'+str(params[3])+'-sr-'+str(params[4])+'-fr-'+str(params[5])+'-tr-'+str(params[6])+'-le-'+str(params[7])+'-sh-'+str(params[8])+'.dep', 'r')
    data = file.readlines();
    for x in data:
        line = x.split(" ");
    s = line[len(line)-1]
    file.close()
    f = open("print.dep", "a")
    f.write("Spearman correlation coefficient final: " + s)

    f.write("Retraining initial model BAG=300 TC=256 ESTOP=100 MLS=1 SRATE=1.0 FRATE=0.2 TREE=1 LEAF=100 SHRINKAGE=0.1 \n")
    f.close()
    os.system("./traintest1.sh 300 256 100 1 1.0 0.2 1 100 0.1 "+TRAIN+" "+TEST+" "+MODEL1)
    file = open('eval/train_devel/results-'+MODEL1+'.b-300-tc-256-es-100-ml-1-sr-1.0-fr-0.2-tr-1-le-100-sh-0.1.dep', 'r')
    data = file.readlines();
    for x in data:
        line = x.split(" ");
    s = line[len(line)-1]
    file.close()
    f = open("print.dep", "a")
    f.write("Spearman correlation coefficient initial: " + s)
    f.close()

else:
    f = open("print.dep", "a")
    f.write("The bash script traintest1.sh has not been created")
    f.close()
