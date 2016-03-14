#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

updrs = [25, 69, 0, 49, 66, 34, 27, 18, 38, 52, 56, 57, 74, 71, 50, 55, 87, 24, 23, 54, 59, 21, 22, 19, 6, 48]
edad = [70, 64, 0, 64, 67, 64, 67, 63, 50, 77, 57, 68, 59, 62, 68, 65, 80, 66, 70, 75, 79, 69, 54, 73, 57, 45]
edad_sort = sorted(edad)
index_sort = sorted(range(len(edad)), key=lambda k: edad[k])
index_sort.pop(0)
index_sort2 = sorted(range(len(edad)), key=lambda k: edad[k])
index_sort2.pop(0)
# [25, 8, 22, 10, 24, 12, 13, 7, 1, 3, 5, 15, 17, 4, 6, 11, 14, 21, 0, 18, 23, 19, 9, 20, 16]

for index in range(5):
    for index2 in range(5):
        index_sort2[index2+index*5] = index_sort[index+5*index2]
# [25, 12, 5, 11, 23, 8, 13, 15, 14, 19, 22, 7, 17, 21, 9, 10, 1, 4, 0, 20, 24, 3, 6, 18, 16]
index_sort = index_sort2

if os.path.exists('extract.sh'):

    train = open("features/New_Data_1.train.arff", "a")
    devel = open("features/New_Data_1.devel.arff", "a")
    for group in range(5):
        for pacient in range(5):
            for audio in range(48):
                if group != 4:
                    if group == 0 and pacient==0 and audio==0:
                        os.system("cp features/palabras_1_" + str(index_sort[pacient+group*5]) + ".arff features/New_Data_1_v2.train.arff")
                    else:
                        file = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient+group*5]) + ".arff", 'r')
                        train.write(file.readlines()[-1])
                        file.close()
                else:
                    if pacient==0 and audio==0:
                        os.system("cp features/palabras_1_" + str(index_sort[pacient+group*5]) + ".arff features/New_Data_1_v2.devel.arff")
                    else:
                        file = open("features/palabras_" + str(audio+1) + "_" + str(index_sort[pacient+group*5]) + ".arff", 'r')
                        devel.write(file.readlines()[-1])
                        file.close()
    train.close()
    devel.close()

else:
    f = open("print.dep", "a")
    f.write("The bash script extract.sh has not been created")
    f.close()
