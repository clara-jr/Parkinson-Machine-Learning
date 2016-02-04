#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

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
        step *= 10

# Greedy - Find optimal parameter C for L=1.0 static -> Find optimal parameter L for C=optimalC static

params = [1.0E-3, 1.0] # [C, L]
init = [1.0E-5, 0.1]
end = [2, 2]
step = [9.0E-5, 0.9]
experiments = [6, 2] # C = 0.00001 0.0001 0.001 0.01 0.1 1.0; L = 0.1 1.0

for cont in range(len(params)):
    values = []
    spearman = []
    string = []
    parallel = "parallel -j " + str(experiments[cont]) + " ./baseline_train_devel.sh {1} {2}"
    for i in range(len(params)):
        string.append(" ::: " + str(params[i]))
    string[cont] = " :::"
    for param in frange(init[cont], end[cont], step[cont]):
        values.append(param)
        string[cont] += " " + str(param)
    for i in range(len(params)):
        parallel += string[i]
    print "Training " + parallel
    os.system(parallel)
    for exp in range(experiments[cont]):
        params[cont] = values[exp]
        file = open('eval/train_devel/ComParE2015_Parkinson.SVR.C'+str(params[0])+'.L'+str(params[1])+'.result', 'r')
        data = file.readlines();
        for x in data:
            line = x.split(" ");
        s = line[len(line)-1]
        spearman.append(float(s))
        file.close()
    index = spearman.index(max(spearman))
    params[cont] = values[index]

print "Optimal C = " + str(params[0])
print "Optimal L = " + str(params[1])
