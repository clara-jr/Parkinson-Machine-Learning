#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import sys

updrs = [25, 69, 0, 49, 66, 42, 27, 18, 38, 52, 56, 57, 74, 71, 50, 55, 87, 24, 23, 54, 59, 21, 22, 19, 6, 48]
edad = [70, 64, 0, 64, 67, 78, 67, 63, 50, 77, 57, 68, 59, 62, 68, 65, 80, 66, 70, 75, 79, 69, 54, 73, 57, 45]
dif_edad = [13, 19, 0, 7, 6, 3, 7, 8, 21, 8, 24, 10, 14, 6, 3, 17, 11, 10, 1, 10, 24, 17, 12, 8, 5, 6]
sexo = ['H', 'H', '', 'H', 'M', 'H', 'H', 'H', 'M', 'M', 'M', 'H', 'H', 'H', 'H', 'M', 'H', 'H', 'M', 'H', 'M', 'H', 'H', 'H', 'H', 'M']
hy = [2, 2, 0, 2.5, 2.5, 2, 2, 2, 2, 2.5, 2, 3, 4, 2, 2, 2, 5, 2, 1, 3, 4, 2, 2, 2, 2, 2]
hy_categ = [3, 3, 0, 4, 4, 3, 3, 3, 3, 4, 3, 5, 6, 3, 3, 3, 7, 3, 1, 5, 6, 3, 3, 3, 3, 3]

# define the function blocks
def edad_func():
    return edad
def dif_edad_func():
    return dif_edad
def sexo_func():
    return sexo
def hy_func():
    return hy
def hy_categ_func():
    return hy_categ

# map the inputs to the function blocks
options = {"edad" : edad_func,
           "dif_edad" : dif_edad_func,
           "sexo" : sexo_func,
           "hy" : hy_func,
           "hy_categ" : hy_categ_func
}

if os.path.exists('extract.sh'):

    os.system("rm print.dep")
    for p in range(len(updrs)):
        for a in range(49):
            if !os.path.exists("features/palabras_" + str(a+1) + "_" + str(p) + ".arff"):
                f = open("print.dep", "a")
                f.write("Converting audio " + str(a+1) + " of pacient " + str(p) + "\n")
                f.close()
                # ./extract.sh wav_file feat_file class
                os.system("./extract.sh palabras_" + str(a+1) + "_" + str(p) + ".ch1.wav palabras_" + str(a+1) + "_" + str(p) + ".arff "+ str(updrs[p]))
            if len(sys.argv) == 2: # wav2arff_new_params param
            	param = sys.argv[1]
                try:
                    params = options[param]()
                    type_param = "numeric"
                    if param == "sexo":
                        type_param = "string"
                    os.system("cp features/palabras_" + str(a+1) + "_" + str(p) + ".arff features/palabras_" + str(a+1) + "_" + str(p) + "_" + param + "_prueba.arff")
                    arff_read = open("features/palabras_" + str(a+1) + "_" + str(p) + ".arff",'r')
                    filedata = arff_read.read()
                    arff_read.close()
                    newdata = filedata.replace("@attribute name string\n","@attribute name string\n@attribute " + param + " " + type_param + "\n")
                    if type_param == "string":
                        newdata = newdata.replace("'unknown',","'unknown','"+str(params[p])+"',")
                    else:
                        newdata = newdata.replace("'unknown',","'unknown',"+str(params[p])+",")
                    arff_write = open("features/palabras_" + str(a+1) + "_" + str(p) + "_" + param + ".arff",'w')
                    arff_write.write(newdata)
                    arff_write.close()
                except:
                    f = open("print.dep", "a")
                    f.write("Default case param is different to the values defined")
                    f.close()
            else:
                f = open("print.dep", "a")
                f.write("")
                f.close()
else:
    f = open("print.dep", "a")
    f.write("The bash script extract.sh has not been created")
    f.close()
