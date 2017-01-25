# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 09:20:00 2017

@author: user
"""

import numpy as np
from scipy.interpolate import griddata as grid
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
rmax=.002
#imports and sorts according to R data from poisson's SF7 file
poissondata=np.genfromtxt("OUTSF7.TXT", skip_header=34)
poissondata=list([list(poissondataline) for poissondataline in poissondata])
poissondata.sort(key=lambda x: x[1])
poissondata=np.array(poissondata)
#get rid of useless poissonsuperfishrows
#make poissondata have only R Z Er Ez
poissondata=np.delete(poissondata,[4,5],axis=1)
#fix units to be in astra units of meter and MV/m
poissondata[:,0] *= .01
poissondata[:,1] *= .01
poissondata[:,2] *= .0001
poissondata[:,3] *= .0001
Nr=sorted(list(set(poissondata[:,0])))
Nr=[r for r in Nr if r <= rmax]
Nx=Ny=sorted([-x for x in Nr]+Nr[1:])
Nz=sorted(list(set(poissondata[:,1])))

X, Y, Z = np.meshgrid(Nx,Ny,Nz)
#Creates file header for astra
fileheader=[[len(list(Nx))]+Nx,[len(Ny)]+Ny,[len(Nz)]+Nz]
#create table of x y r theta and i, which is the order preserver
griddata=[]
i=0
for y in Ny:
    for x in Nx:
        griddata.append([x,y,np.sqrt(x*x+y*y),np.arctan2(y,x),i])
        i+=1
griddata.sort(key=lambda x: x[2])
griddata=np.array(griddata)
i=0
location=[]
#This part separates the whole array from poisson into chucks with the same z
for z in sorted(list(set(poissondata[:,1]))):
    #Find where current z value starts in poissondata
    location.append(max(np.where(poissondata[:,1]<=z)[0]))
poissonzsection=[]
#This lets you go to the next different z, no matter the spacing
#between different zs.
start=0
for selector in location:
    poissonzsection.append(poissondata[start:selector])
    start=selector
Rmesh= np.meshgrid(griddata[:,2])
i=0
Edata=[]
for pzsection in poissonzsection:
    Er=grid(pzsection[:,:1],pzsection[:,2],(Rmesh), method="linear", fill_value=0.)
    Ez=grid(pzsection[:,:1],pzsection[:,3],(Rmesh), method="linear", fill_value=0.)    
    i=0
    for dline in griddata:       
        #appending (Ex,Ey,Ez,x,y,i) (i is the order preserver)
        Edata.append([Er[0,i]*np.cos(dline[3]),Er[0,i]*np.sin(dline[3]),Ez[0,i],dline[0],dline[1],dline[-1]])
        i+=1

#breaks up Edata into a list of points by component ordered in Z 
#to print it out
Gridspacing=len(Nx)*len(Ny)
EdataChunks=np.array([Edata[i:i+Gridspacing] for i in range(0,len(Edata),Gridspacing)])
#put it in the easiest format to write it out in astra format
Exdata=[]
Eydata=[]
Ezdata=[]
for Edatazsection in EdataChunks:
    #sorting by i to preserve the order of cycling through y values for each x
    Edatazsection=Edatazsection[Edatazsection[:,-1].argsort()]
    Exdata.append(list(Edatazsection[:,0]))
    Eydata.append(list(Edatazsection[:,1]))
    Ezdata.append(list(Edatazsection[:,2]))
Exdataastraformat=[]
Eydataastraformat=[]
Ezdataastraformat=[]
for zsection in Exdata:
    linespacing=len(Nx)
    zsectionchunk=[zsection[i:i+linespacing] for i in range(0,len(zsection),linespacing)]
    Exdataastraformat.append(zsectionchunk)
Exdataastraformat=np.array(Exdataastraformat)
for zsection in Eydata:
    linespacing=len(Ny)
    zsectionchunk=[zsection[i:i+linespacing] for i in range(0,len(zsection),linespacing)]
    Eydataastraformat.append(zsectionchunk)
Eydataastraformat=np.array(Eydataastraformat)
for zsection in Ezdata:
    linespacing=len(Nx)
    zsectionchunk=[zsection[i:i+linespacing] for i in range(0,len(zsection),linespacing)]
    Ezdataastraformat.append(zsectionchunk)
Ezdataastraformat=np.array(Ezdataastraformat)
#write out the data
with open("DC-3D.ex","w") as outfile:
    writer=csv.writer(outfile,delimiter=' ')
    for i in np.arange(0,len(fileheader),1):
        writer.writerow(fileheader[i])
    for array in Exdataastraformat:
        for line in array:
            writer.writerow(line)
with open("DC-3D.ey","w") as outfile:
    writer=csv.writer(outfile,delimiter=' ')
    for i in np.arange(0,len(fileheader),1):
        writer.writerow(fileheader[i])
    for array in Eydataastraformat:
        for line in array:
            writer.writerow(line)
with open("DC-3D.ez","w") as outfile:
    writer=csv.writer(outfile,delimiter=' ')
    for i in np.arange(0,len(fileheader),1):
        writer.writerow(fileheader[i])
    for array in Ezdataastraformat:
        for line in array:
            writer.writerow(line)