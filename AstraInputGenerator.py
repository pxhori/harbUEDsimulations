import argparse
import numpy as np
import random as r

#Default Parameters
c=2.998*10**8
#r.seed(2343)
me=9.1*10**-31
laserPulseDuration=100.*10**-15
laserSpotSize=.01*10**-3
energySpread=1.602*10**-20*2
FWHM2Gauss = (1/2.35482)
NumberofElectrons=10000
SimulatedParticles=10000


inputarguments=[]
#This reads the default inputs from the "example.in" file
with open("default.in") as defaults:
    defaults=defaults.readlines()
    for line in defaults:
        inputarguments.append(line.split())
#this is where you add options
parser = argparse.ArgumentParser(description='Set the Parameters')
parser.add_argument('--describe', type=str, help='description of the simulation',default="")
parser.add_argument('--aprad', type=float, help='The aperture Radius (mm)')
parser.add_argument('--lpd', type=float, help='Laser Pulse Duration (seconds)', default=laserPulseDuration)
parser.add_argument('--lss', type=float, help='Laser Spot Size (meters)', default=laserSpotSize)
parser.add_argument('--N', type=int, help='Number of Electrons', default=NumberofElectrons)
args=parser.parse_args()
#allows default aprad to be left
if args.aprad:
    aprad=args.aprad
    inputarguments[37][4]="Ap_R(1)={},".format(aprad)
else:
    aprad=.5

#Set Parameters
laserPulseDuration=args.lpd
laserSpotSize=args.lss
NumberofElectrons=args.N
#writes the new input file (Not distribution, instructions)
fname="aprad{}lpd{}lss{}N{}".format(aprad,laserPulseDuration,laserSpotSize,NumberofElectrons)+args.describe
#Changes name of distribution file in input file
inputarguments[6][2]="'"+fname+".ini',"

f=open(fname+".in", "w")
for line in inputarguments:
    f.write("".join(line))
    f.write("\n")
    print("".join(line))
    
f.close()


#Here begins the input file generation

macrocharge=NumberofElectrons/SimulatedParticles*1.6*10**-10
E_0=energySpread*FWHM2Gauss
#G=1.-qe*E_0/(me*c*c)
#beta=np.sqrt(1.-G*G)
rxy=laserSpotSize*FWHM2Gauss
tau = laserPulseDuration*FWHM2Gauss
x=[r.gauss(0.,rxy) for x in np.arange(0,NumberofElectrons,1)]
y=[r.gauss(0.,rxy) for y in np.arange(0,NumberofElectrons,1)]
t=[r.gauss(0.,tau)/(10**-9) for z in np.arange(0,NumberofElectrons,1)]
E = []
while len(E) < NumberofElectrons:
    Energy = r.gauss(0, E_0)
    if Energy>=0:
        E.append(Energy)

p=[np.sqrt(E[i]*E[i]/(c*c)+2*me*E[i])*1.87115736*10**27 for i in np.arange(0,NumberofElectrons,1)]
phi=[r.uniform(-np.pi/2.,np.pi/2) for x in np.arange(0,NumberofElectrons,1)]
theta=[r.uniform(0.,2*np.pi) for x in np.arange(0,NumberofElectrons,1)]
px=[p[i]*np.cos(theta[i])*np.sin(phi[i]) for i in np.arange(0,NumberofElectrons,1)]
py=[p[i]*np.sin(theta[i])*np.sin(phi[i]) for i in np.arange(0,NumberofElectrons,1)]
pz=[p[i]*np.cos(phi[i]) for i in np.arange(0,NumberofElectrons,1)]

f = open(fname+".ini","w")
f.write('{0: 12.4E}{1: 12.4E}{2: 12.4E}{3: 12.4E}{4: 12.4E}{5: 12.4E}{6: 12.4E}{7: 12.4E}{8: 4d}{9: 4d}\n'.format(0.,0.,0.,0.,0.,0.,(.0),macrocharge,1,-1))
for i in np.arange(1,NumberofElectrons,1):
    f.write('{0: 12.4E}{1: 12.4E}{2: 12.4E}{3: 12.4E}{4: 12.4E}{5: 12.4E}{6: 12.4E}{7: 12.4E}{8: 4d}{9: 4d}\n'.format(x[i],y[i],0,px[i],py[i],pz[i],t[i],macrocharge,1,-1))
f.close()