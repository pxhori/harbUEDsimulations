# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 09:49:26 2016

@author: paul
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:46:42 2016

@author: paul
"""

import glob
import numpy as np
import matplotlib.pyplot as plt
import collections as c
from itertools import cycle
lines = ["p","o","d","*"]
linecycler = cycle(lines)
#path sets key for filtering through files
path="*.csv"
#makes log.txt into array
log=np.genfromtxt('log.txt', delimiter=',', skip_header=1)
multipoint=c.namedtuple("multipoint",["run","lss","electronatsample","electronatcathode","emittance","length","fwhmx"])
#this makes isolating the run number possible
start="Run_"
end=".csv"
plotdata=[]
multipoints=[]
#create named tuples with attributes of run
for fname in glob.glob(path):
    if "Run" in fname and ".py" not in fname:
        runnumber=int(((fname.split(start))[1].split(end)[0]))
        csvdata=[]
        csvdata=np.genfromtxt(fname, delimiter=",")
        multipoints.append(multipoint(runnumber,int(log[runnumber-1][1]*10**6),int(csvdata[-1][12]),int(log[runnumber-1][2]),csvdata[-1][17],10**15*csvdata[-1][5]*2.355/(csvdata[-1][10]*2.998*10**8),csvdata[-1][6]*2.355*1000000))
#figure out how many different lss values there are in the data set
"""
If variable number of data output points in run, uses these instead of the above        
        csvdata=np.genfromtxt(fname, delimiter=",", skip_header=1)
        csvdata=csvdata[-1]
"""
        #the number in xemitdata is the extracted column!!
lssvalues=[]
for data in multipoints:
    if data.lss not in lssvalues:
        lssvalues.append(data.lss)
#plot for each value of lss
for lss in sorted(lssvalues):
    plotdata=[]
    for multipoint in multipoints:
        if multipoint.lss==lss:
            plotdata.append([float(multipoint.electronatsample),float(multipoint.emittance),multipoint.length,float(multipoint.fwhmx),multipoint.electronatcathode,multipoint.run])
    plotdata=np.array(plotdata)
    style=next(linecycler)
    plt.figure(1)    
    plt.plot(plotdata[:,0],plotdata[:,2],style,label=str(lss))
    plt.figure(2)
    plt.plot(plotdata[:,0],plotdata[:,1],style,label=str(lss))
    plt.figure(3)
    plt.plot(plotdata[:,0],plotdata[:,3],style,label=str(lss))
    plt.figure(4)
    plt.plot(plotdata[:,4],plotdata[:,0],style,label=str(lss))
    #sort plotdata by run number
    plotdata=plotdata[plotdata[:,-1].argsort()]
    "Optional saving data to file"
    np.savetxt(str(lss)+".mra",plotdata,delimiter=' ', comments="", header="Electronsatsample Emittance Pulselength Fwhmx Electronsatcathode run")
plt.figure(1)
plt.legend(bbox_to_anchor=(.21, 1), loc=1,)
plt.title("Pulse Length vs. E-Number for Varying LSS (micron)")
plt.ylabel("Pulse Length (fs)")
plt.xlabel("Electron Number at Sample")
plt.figure(2)
plt.legend(bbox_to_anchor=(-.05, 1), loc=1,)
plt.title("Emittance vs. E-Number for Varying LSS (micron)")
plt.ylabel("Emittance (pi mrad mm)")
plt.xlabel("Electron Number at Sample")
plt.figure(3)
plt.legend(bbox_to_anchor=(-.05, 1), loc=1,)
plt.title("Beam Size vs. E-Number for Varying LSS (micron)")
plt.ylabel("Beam Size (um)")
plt.xlabel("Electron Number at Sample")
plt.figure(4)
plt.legend(bbox_to_anchor=(-.05, 1), loc=1,)
plt.title("Electron at Sample vs. Electron at Cathode")
plt.ylabel("Electron Number at Sample")
plt.xlabel("Electron Number at Cathode")
plt.show()
