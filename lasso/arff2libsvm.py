#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# import sys

def arff2libsvm(inputfilename, outputfilename):
    file_in = open(inputfilename,'r')
    lines = file_in.readlines()
    file_in.close()
    file_out = open(outputfilename,'w')
    beginToRead = False
    for line in lines:
        if beginToRead == True:
            if len(line) > 5: # not an empty line
                # read this line
                dataList = line.split(',')
                resultLine = ''
                resultLine += dataList[-1].strip()
                resultLine += ' '
                for i in range(1,len(dataList)-1):
                    resultLine += str(i)
                    resultLine += (":"+dataList[i]+" ")
                file_out.write(resultLine+"\n")
        if line[0:5] == '@data':
            beginToRead = True
    file_out.close()

# if(len(sys.argv) < 3):
    # print("usage: python arff2libsvm.py inputfilename outputfilename")
# else:
    # inputfilename = sys.argv[1]
    # outputfilename = sys.argv[2]
    # arff2libsvm(inputfilename, outputfilename)

parkinson_class = ["updrs", "hoenhyahr", "hoenhyahr_categorise"]
version = "homoupdrs"
n_pacientes = 26
n_grupos = 5
train_devel = ["train", "devel"]

for t_d in range(len(train_devel)):
    for i in range(len(parkinson_class)):
        inputfilename = "../data/Experiment_New_Data_all_"+parkinson_class[i]+"_"+version+"."+train_devel[t_d]+".arff"
        outputfilename = "../data/Experiment_New_Data_all_"+parkinson_class[i]+"_"+version+"."+train_devel[t_d]+".libsvm"
        arff2libsvm(inputfilename, outputfilename)
        for n in range(n_grupos):
            inputfilename = "../data/Experiment_New_Data_"+str(n+1)+"_"+parkinson_class[i]+"_"+version+"."+train_devel[t_d]+".arff"
            outputfilename = "../data/Experiment_New_Data_"+str(n+1)+"_"+parkinson_class[i]+"_"+version+"."+train_devel[t_d]+".libsvm"
            arff2libsvm(inputfilename, outputfilename)
    for pacient in range(n_pacientes):
        if pacient != 2:
            inputfilename = "../data/Experiment_New_Data_"+str(pacient)+"_leave_one."+train_devel[t_d]+".arff"
            outputfilename = "../data/Experiment_New_Data_"+str(pacient)+"_leave_one."+train_devel[t_d]+".libsvm"
            arff2libsvm(inputfilename, outputfilename)
