#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import xlrd

doc = xlrd.open_workbook('ComParE2015_Parkinson_meta.xlsx')
sheet_train = doc.sheet_by_index(0)
sheet_devel = doc.sheet_by_index(1)

updrs_train = []
updrs_devel = []

for element_train in range(1470):
    updrs_train.append(sheet_train.cell_value(element_train+1,3))
for element_devel in range(630):
    updrs_devel.append(sheet_devel.cell_value(element_devel+1,3))

if os.path.exists('extract.sh'):

    # devel_0001.wav devel_0630.wav
    # train_0001.wav train_1470.wav

    for train in range(1470):
        os.system("./extract.sh train_"+str(train+1).zfill(4)+".wav train_"+str(train+1).zfill(4)+".arff "+ str(updrs_train[train]))
        if train==0:
            os.system("cp features_comp/train_0001.arff features_comp/Comp_Parkinson.train.arff")
        else:
            train_arff = open("features_comp/Comp_Parkinson.train.arff", "a")
            file = open("features_comp/train_"+str(train+1).zfill(4)+".arff", 'r')
            train_arff.write(file.readlines()[-1])
            file.close()
    train_arff.close()

    for devel in range(630):
        os.system("./extract.sh devel_"+str(devel+1).zfill(4)+".wav devel_"+str(devel+1).zfill(4)+".arff "+ str(updrs_devel[devel]))
        if devel==0:
            os.system("cp features_comp/devel_0001.arff features_comp/Comp_Parkinson.devel.arff")
        else:
            devel_arff = open("features_comp/Comp_Parkinson.devel.arff", "a")
            file = open("features_comp/devel_"+str(devel+1).zfill(4)+".arff", 'r')
            devel_arff.write(file.readlines()[-1])
            file.close()
    devel_arff.close()

else:
    f = open("print.dep", "a")
    f.write("The bash script extract.sh has not been created")
    f.close()
