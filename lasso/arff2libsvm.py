#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

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

train_devel = ["train", "devel", "test"]
version = "leave_half"
version_two = "leave_half_two"
version_all = "leave_half_all"
index_sort = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

for t_d in range(len(train_devel)):
    for pacient in range(len(index_sort)):
        inputfilename = "../data/Experiment_New_Data_"+str(index_sort[pacient])+"_"+version+"."+train_devel[t_d]+".arff"
        outputfilename = "../data/Experiment_New_Data_"+str(index_sort[pacient])+"_"+version+"."+train_devel[t_d]+".libsvm"
        arff2libsvm(inputfilename, outputfilename)
for t_d in range(len(train_devel)):
    for pacient in range(len(index_sort)):
        if pacient != len(index_sort)-1:
            inputfilename = "../data/Experiment_New_Data_"+str(index_sort[pacient])+"_"+str(index_sort[pacient+1])+"_"+version_two+"."+train_devel[t_d]+".arff"
            outputfilename = "../data/Experiment_New_Data_"+str(index_sort[pacient])+"_"+str(index_sort[pacient+1])+"_"+version_two+"."+train_devel[t_d]+".libsvm"
            arff2libsvm(inputfilename, outputfilename)
for t_d in range(len(train_devel)):
    inputfilename = "../data/Experiment_New_Data_"+version_all+"."+train_devel[t_d]+".arff"
    outputfilename = "../data/Experiment_New_Data_"+version_all+"."+train_devel[t_d]+".libsvm"
    arff2libsvm(inputfilename, outputfilename)
