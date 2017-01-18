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
#define interested r and z region in meters
r=.00200000
dr=.00001
z=.01100000
dz=.00055
Nr=list(np.arange(0,r+dr/2,dr))
#Define the parameters for the rectangular grid here, or leave to match with 
#what is given from poisson but as a rectangle
Nx=Ny=list(np.arange(-r,r+dr/2,dr))
Nz=list(np.arange(0,z+dr,dz))
#makes rectangular grid
X, Y, Z = np.meshgrid(Nx,Ny,Nz)
#Creates file header for astra
fileheader=[[len(list(Nx))]+Nx,[len(Ny)]+Ny,[len(Nz)]+Nz]
#imports and sorts according to R data from poisson's SF7 file
poissondata=np.genfromtxt("OUTSF7.TXT", skip_header=33)
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
#create table of x y r theta
griddata=[]
for x in Nx:
    for y in Ny:
        griddata.append([x,y,np.sqrt(x*x+y*y),np.arctan2(y,x)])
griddata.sort(key=lambda x: x[2])
griddata=np.array(griddata)
i=0
location=[]
#This part separates the whole array from poisson into chucks with the same z
for z in sorted(list(set(poissondata[:,1]))):
    #Find where current z value starts in poissondata
    location.append(max(np.where(poissondata[:,1]<=z)[0]))
#NOTE THAT THIS IS THE ONLY PLACE THAT IT IS REQUIRED TO BE UNIFORMLY SPACED
#IN Z.  Change this part if you want to change up the z spacing for 
#some reason.
spacing=location[2]-location[1]-1
poissonzsection=[]
for selector in location:
    poissonzsection.append(poissondata[selector-spacing:selector+1])
Rmesh= np.meshgrid(griddata[:,2])
i=0
Edata=[]
for pzsection in poissonzsection:
    Er=grid(pzsection[:,:1],pzsection[:,2],(Rmesh), method="linear", fill_value=0.)
    Ez=grid(pzsection[:,:1],pzsection[:,3],(Rmesh), method="linear", fill_value=0.)    
    i=0
    for dline in griddata:       
        #appending (Ex,Ey,Ez)
        Edata.append([Er[0,i]*np.cos(dline[3]),Er[0,i]*np.sin(dline[3]),Ez[0,i]])
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
#this is just to fiugre out the plots

#plt.quiver(griddata[:,0], griddata[:,1], Exdataastraformat[80,:,:], Eydataastraformat[80,:,:],scale=1)
depth=175
location=str(depth*dz)
Evalues=[]
plottingdata=np.array([[Exdataastraformat[depth,i,:],Eydataastraformat[depth,i,:]] for i in np.arange(0,len(Exdataastraformat[depth,:,:]),1)])
#3d plot attempt
for xline in plottingdata:
    for i in np.arange(0,len(Exdataastraformat[depth,:,:]),1):
        Evalues.append(np.sqrt(xline[0][i]**2+xline[1][i]**2))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(griddata[:,0],griddata[:,1],Evalues)
plt.title("Er Magnitude vs. X and Y at z= "+location)
plt.show()
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