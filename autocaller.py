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
#create log file
i=1
f=open("log.txt", "w")
f.write("run,lss,N\n")
for lss in lssrange:
    for N in Nrange:
        f.write("{},{},{}\n".format(i,lss,N))      
        i+=1
f.close()
os.system("cp log.txt statistics/")
#Actually run the program
i=1
for lss in lssrange:
    for N in Nrange:
        os.system("python EZSim.py --lss={0:.20f} --N={1:} ".format(lss, N)+"--describe='Run_"+str(i)+"'")     
        time.sleep(.1)
        print("\nRun "+str(i)+" is finished! \n")
        i+=1


