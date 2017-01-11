import numpy as np
lssrange=np.arange(50*10**-6,550*10**-6,50*10**-6)
Nrange=np.arange(2000.,41000,1000)
with open("Parameters.txt", 'w') as f:
    for i in lssrange:
        f.write(str(i)+",")
    f.write("\n")
    for i in Nrange:
        f.write(str(i)+",")
