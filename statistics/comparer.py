# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 10:00:52 2016

@author: paul
"""
import numpy as np
import csv
import matplotlib.pyplot as plt
data=[]
with open("ediff_gun_avg_var1.txt") as f:
    reader=csv.reader(f, delimiter=' ')
    for row in reader:
        data.append([x for x in row if not '' == x])
    data.remove(data[-1])
    gptheading=data[0]
    data.remove(data[0])
    gptdata=np.array(data)
    gptdata=gptdata.astype(float)
gptdata[:,0]=gptdata[:,0]*10**9

astradata=[]
"""
for i in np.arange(1,10,1):
    data=[]
    with open("Benchmark1nopinhole{}.csv".format(i)) as f:
        reader=csv.reader(f,delimiter=',')
        for row in reader:
            data.append(row)
        headingastra=data[0]
        data.remove(data[0])
        data=np.array(data).astype(float)
    data[:,13]=data[:,13]*1000000
    astradata.append(data)
"""
data=[]
with open("Benchmark1nopinholecorrectv.csv") as f:
    reader=csv.reader(f,delimiter=',')
    for row in reader:
        data.append(row)
    headingastra=data[0]
    data.remove(data[0])
    data=np.array(data).astype(float)
data[:,13]=data[:,13]
astradata.append(data)
headings=[gptheading,headingastra]
fig=plt.figure()
ax1=fig.add_subplot(111)
"""
for i in np.arange(0,1,1):
    ax1.scatter(astradata[i][:,0],astradata[i][:,10],s=2)
"""
ax1.scatter(astradata[0][:,0],astradata[0][:,18],s=2)
ax1.scatter(gptdata[:,0],gptdata[:,11],s=11,marker='v',c='red')
plt.autoscale(enable=True,tight=True)
plt.show()