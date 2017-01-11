# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 09:20:00 2017

@author: user
"""

import numpy as np
from scipy.interpolate import griddata as grid
import csv

poissondata=np.genfromtxt("OUTPOI.TXT", skip_header=261)
astradata=[]
for line in poissondata:
    for theta in np.arange(0.,2*np.pi,np.pi/180): #This part makes the data go around in a circle (cylindrically symettric)
        #appending [x,y,z,Ex,Ey,Ez]
        astradata.append([line[2]*np.cos(theta),line[2]*np.sin(theta),line[3],line[4]*np.cos(theta),line[4]*np.sin(theta),line[5]])
astradata=np.array(astradata)

#this tests the code by plotting the vector field of x and y for some value of z
"""
astradata=astradata[(6*50*18):(7*50*18),:]

plt.plot(astradata[:,0],astradata[:,3],'.')
"""
#The horrible thing at the end simply defines the number of steps to be the square root of the total number of points divided by the number of z values
Nx=list(.01*np.linspace(astradata[:,0].min(),astradata[:,0].max(),num=np.sqrt((len(astradata[:,0])/len(list(set(astradata[:,2])))))))
Ny=list(.01*np.linspace(astradata[:,1].min(),astradata[:,1].max(),num=np.sqrt((len(astradata[:,0])/len(list(set(astradata[:,2])))))))
#Nz values extracted directly, these won't need to be interpolated
Nz=sorted(list(set(.01*astradata[:,2])))
#Creates file header for astra
fileheader=[[len(list(Nx))]+Nx,[len(Ny)]+Ny,[len(Nz)]+Nz]
#First make a 3d mesh coordinate grid, then use interpolate.grid to output Ex,
#Ey, and Ez grids.
X, Y, Z = np.meshgrid(Nx,Ny,Nz)
Exdata=grid(astradata[:,:3]*.01,astradata[:,3],(X,Y,Z), method="nearest")
Eydata=grid(astradata[:,:3]*.01,astradata[:,4],(X,Y,Z), method="nearest")
Ezdata=grid(astradata[:,:3]*.01,astradata[:,5],(X,Y,Z), method="nearest")
#Bring it the way astra likes the data to be written (x and y plot for each z value)
Exdata=np.rollaxis(Exdata*.0001,2)
Eydata=np.rollaxis(Eydata*.0001,2)
Ezdata=np.rollaxis(Ezdata*.0001,2)
#Finally, write the three files the way Astra wants
with open("DC-3D.ex","w") as outfile:
    writer=csv.writer(outfile,delimiter=' ')
    for i in np.arange(0,len(fileheader),1):
        writer.writerow(fileheader[i])
    for array in Exdata:
        for line in array:
            writer.writerow(line)
with open("DC-3D.ey","w") as outfile:
    writer=csv.writer(outfile,delimiter=' ')
    for i in np.arange(0,len(fileheader),1):
        writer.writerow(fileheader[i])
    for array in Eydata:
        for line in array:
            writer.writerow(line)
with open("DC-3D.ez","w") as outfile:
    writer=csv.writer(outfile,delimiter=' ')
    for i in np.arange(0,len(fileheader),1):
        writer.writerow(fileheader[i])
    for array in Ezdata:
        for line in array:
            writer.writerow(line)
