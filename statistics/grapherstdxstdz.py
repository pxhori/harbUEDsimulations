# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 11:17:42 2016

@author: user
"""
import numpy as np
import matplotlib.pyplot as plt

data=np.genfromtxt('Run_38.csv', delimiter=',', skip_header=1)
fig=plt.figure()
#stdx
ax1=fig.add_subplot(121)
ax1.plot(data[:,1]*1000,data[:,6]*1000000*2.355, "o", ms=1)
ax1.set_title("fwhmx (micrometers) vs avgz (mm)")

#PulseLength
ax2=fig.add_subplot(122)
ax2.plot(data[:,1]*1000,10**15*data[:,5]*2.355/(data[-1,10]*2.998*10**8), "o", ms=1)
ax2.set_title("pulse length (fs) vs avgz (mm)")



plt.tight_layout()
plt.show()
