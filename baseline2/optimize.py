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

# Greedy - Find optimal parameter C for L=1.0 static -> Find optimal parameter L for C=opt[0] static

params = [1.0E-3, 1.0] # [C, L]
init = [1.0E-5, 1.0E-5]
end = [2, 2]
step = [9.0E-5, 9.0E-5]

for i in range(len(params)):
    values = []
    spearman = []
    for param in frange(init[i], end[i], step[i]): # 0.00001 0.0001 0.001 0.01 0.1 1
        params[i] = param
        values.append(param)
        print "Training C="+str(params[0])+" L="+str(params[1])
        os.system('./baseline_train_devel.sh '+str(params[0])+' '+str(params[1]))
        file = open('eval/train_devel/ComParE2015_Parkinson.SVR.C'+str(params[0])+'.L'+str(params[1])+'.result', 'r')
        data = file.readlines();
        for x in data:
            line = x.split(" ");
        s = line[len(line)-1]
        spearman.append(float(s))
        file.close()
    index = spearman.index(max(spearman))
    params[i] = values[index]

print "Optimal C = " + str(params[0])
print "Optimal L = " + str(params[1])
