import glob
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
#This allows you to specify whether to keep or delete the files at the end (default is to delete
parser = argparse.ArgumentParser(description='Set the Parameters')
parser.add_argument('--delfiles', type=int, help="Choose whether to keep or delete phase space files, default to delete", default=1)
args=parser.parse_args()
path="*.001"
me=9.1*10**-31
c=2.998*10**8
def parser(): 
    data=[]
    with open(fname) as f:
        f=f.readlines()     
        #gets reference particle data
        ref=f[0].split()
        ref=[float(x) for x in ref]
        #neglects charge and status flags
        ref[-1]=0
        ref[-2]=0
        ref[-3]=0
        #puts all in data, transforming co-ordinates from relative to reference particle to absolute
        for line in f:
            if int(line[-4:])==3 or int(line[-4:])==5:
                data.append((line).split())
        data=np.array(data).astype(float)+ref
        if data[0][-1] == 5:
            data[0,:7]=data[0,0:7]-ref[0:7]
        else:
            pass
        
        return data
def statisticsgenerator(data,me,c):
        xdata=data[:,0]
        ydata=data[:,1]
        zdata=data[:,2]
        pxdata=data[:,3]*5.34428595*10**-28 #convert from eV/c to kg*m/s
        pydata=data[:,4]*5.34428595*10**-28
        pzdata=data[:,5]*5.34428595*10**-28
        tdata=data[:,6]
        p2=pxdata*pxdata+pydata*pydata+pzdata*pzdata
        v2=p2/(me*me+p2/(c*c))
        vxdata=pxdata*np.sqrt((1.-v2/(c*c)))/me
        vydata=pydata*np.sqrt((1.-v2/(c*c)))/me
        vzdata=pzdata*np.sqrt((1.-v2/(c*c)))/me
        Gdata=1./(np.sqrt(1.-v2/(c*c)))
        avgx=xdata.mean()
        avgy=ydata.mean()
        avgy=ydata.mean()
        avgz=zdata.mean()
        avgr=np.sqrt(avgx*avgx+avgy*avgy)
        stdx=xdata.std()
        stdy=ydata.std()
        stdz=zdata.std()
        avgBx=vxdata.mean()/c
        avgBy=vydata.mean()/c
        avgBz=vzdata.mean()/c
        Bxdata=vxdata/c
        Bydata=vydata/c
        avgG=Gdata.mean()
        xc=xdata-avgx
        xpc=Bxdata-avgBx
        yc=ydata-avgy
        ypc=Bydata-avgBy
        nemixrms=avgG*np.sqrt(((xc*xc).mean())*((xpc*xpc).mean())-((xc*xpc).mean())**2)
        nemiyrms=avgG*np.sqrt(((yc*yc).mean())*((ypc*ypc).mean())-((yc*ypc).mean())**2)
        emixrms=avgG*np.sqrt(((xc*xc).mean())*((xpc*xpc).mean())-((xc*xpc).mean())**2)
        emiyrms=avgG*np.sqrt(((yc*yc).mean())*((ypc*ypc).mean())-((yc*ypc).mean())**2)
        nemirrms=avgG*np.sqrt(emixrms*emiyrms-abs((xc*yc).mean()*(xpc*ypc).mean()-(xc*ypc).mean()*(xpc*yc).mean()))
        tc=tdata-tdata.mean()
        Gc=Gdata-avgG
        nemizrms=me*c*c/(1.6*10**-19)*np.sqrt((tc*tc).mean()*(Gc*Gc).mean()-(tc*Gc).mean()**2)
        return tdata.mean(), avgz, avgx, avgy, avgr, stdz, stdx, stdy, avgBx, avgBy, avgBz, avgG, len(xdata), nemirrms, nemizrms, data,
    
stats=[]
for fname in glob.glob(path):
    #extracts output data into np array
    if "emit" not in fname and "Log" not in fname and "ref" not in fname and "3d" not in fname:
        t, avgz, avgx, avgy, avgr, stdz, stdx, stdy, avgBx, avgBy, avgBz, avgG, numpar, nemirrms, nemizrms, data=statisticsgenerator(parser(),me,c)
        stats.append([t, avgz, avgx, avgy, avgr, stdz, stdx, stdy, avgBx, avgBy, avgBz, avgG, numpar, nemirrms, nemizrms])
        if args.delfiles==True:        
            os.remove(fname)
        else:
            pass
    else:
        continue
    
stats=sorted(stats, key=lambda stat: stat[0])
stats=np.array(stats)
'''
plt.figure(1)
plt.xlabel("t (ns)")
plt.ylabel("nemirrms (pi*mm*mrad)")
plt.plot(stats[:,0],stats[:,13]*1000000)
plt.figure(2)
plt.xlabel("t (ns)")
plt.ylabel("nemizrms (eV*s)")
plt.plot(stats[:,0],stats[:,14])
plt.show()
'''
if os.path.isdir("statistics")==False:
    os.makedirs("statistics")
else:
    pass
np.savetxt("statistics/"+fname[:-9]+".csv", stats, header="t (ns), avgz (m), avgx (m), avgy (m), avgr (m), stdz (m), stdx (m), stdy (m), avgBx , avgBy, avgBz, avgG, numpar, nemirrms (pi m rad), nemizrms (eV s)", delimiter=",")