# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 11:17:42 2016

@author: user
"""
import numpy as np
import matplotlib.pyplot as plt

data=np.genfromtxt('1.csv', delimiter=',', skip_header=1)
fig=plt.figure()
#avgbx
ax1=fig.add_subplot(223)
ax1.plot(data[:,1]*1000,data[:,8]*1000000, "o", ms=1)
ax1.set_title("avgbx*1000000 vs avgz (mm)")

#avbgz
ax2=fig.add_subplot(224)
ax2.plot(data[:,1]*1000,data[:,10], "o", ms=1)
ax2.set_title("avgbz vs avgz (mm)")

#stdbx
ax3=fig.add_subplot(221)
ax3.plot(data[:,1]*1000,data[:,14]*1000, "o", ms=1)
ax3.set_title("stdbx*1000 vs avgz (mm)")

#stdbz
ax4=fig.add_subplot(222)
ax4.plot(data[:,1]*10000,data[:,13]*1000, "o", ms=1)
ax4.set_title("stdbz*1000 vs avgz (mm)")


plt.tight_layout()
plt.show()
