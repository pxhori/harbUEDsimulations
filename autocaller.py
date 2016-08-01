# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 12:12:20 2016

@author: paul
"""
import csv
import os
import time
parameters=[]
with open("Parameters.txt") as f:
    reader=csv.reader(f, delimiter=",")   
    for row in reader:
        parameters.append(row)
lssrange=[float(x) for x in parameters[0] if not ''==x]
Nrange=[int(float(x)) for x in parameters[1] if not ''==x]
i=1
f=open("log.txt", "w")
f.write("run,lss,N")
for lss in lssrange:
    for N in Nrange:
        os.system("python EZSim.py --lss={0:.20f} --N={1:} ".format(lss, N)+"--describe=Run_"+str(i))
        f.write("{},{},{}\n".format(i,lss,N))      
        i+=1
        time.sleep(.1)
f.close()