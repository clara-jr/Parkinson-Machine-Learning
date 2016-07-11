#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

updrs = [25, 69, 0, 49, 66, 34, 27, 18, 38, 52, 56, 57, 74, 71, 50, 55, 87, 24, 23, 54, 59, 21, 22, 19, 6, 48]
n_audios = 49
paciente_desconocido = 2

if os.path.exists('extract.sh'):

    os.system("rm print.dep")
    for p in range(len(updrs)):
        for a in range(n_audios):
            f = open("print.dep", "a")
            f.write("Converting audio " + str(a+1) + " of pacient " + str(p) + "\n")
            f.close()
            if not os.path.exists("features/palabras_" + str(a+1) + "_" + str(p) + ".arff"):
                # ./extract.sh wav_file feat_file class
                os.system("./extract.sh palabras_" + str(a+1) + "_" + str(p) + ".ch1.wav palabras_" + str(a+1) + "_" + str(p) + ".arff "+ str(updrs[p]))

            if p==0 and a==0:
                os.system("cp features/palabras_1_0.arff features/New_Data.train.arff")
            else:
                if p != paciente_desconocido:
                    data = open("features/New_Data.train.arff", "a")
                    file = open("features/palabras_" + str(a+1) + "_" + str(p) + ".arff", 'r')
                    data.write(file.readlines()[-1])
                    file.close()
            #os.system("rm features/palabras_" + str(a+1) + "_" + str(p) + ".arff")

    data.close()
    os.system("cp features/New_Data.train.arff features/New_Data.devel.arff")

else:
    f = open("print.dep", "a")
    f.write("The bash script extract.sh has not been created")
    f.close()
