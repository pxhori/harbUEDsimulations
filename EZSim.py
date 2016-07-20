# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 09:45:01 2016

@author: paul
"""
import argparse
import os
from datetime import datetime
dt = datetime.now()
dt=dt.strftime('d%Y.%m.%dt%H.%M.%S')
#Define the distribution defaults (simulation defaults are in 'default.in')
laserPulseDuration=100.*10**-15
laserSpotSize=.01*10**-3
NumberofElectrons=10000
aprad=.5

parser = argparse.ArgumentParser(description='Set the Parameters')
parser.add_argument('--describe', type=str, help='Description of the simulation, if not specified date and time is used', default=dt)
parser.add_argument('--aprad', type=str, help='The aperture Radius (mm)', default=aprad)
parser.add_argument('--lpd', type=str, help='Laser Pulse Duration (seconds)', default=laserPulseDuration)
parser.add_argument('--lss', type=str, help='Laser Spot Size (meters)', default=laserSpotSize)
parser.add_argument('--N', type=str, help='Number of Electrons', default=NumberofElectrons)
parser.add_argument('--delfiles', type=int, help="Choose whether to keep (0) or delete (1) phase space files, default to delete", default=1)
args=parser.parse_args()
args.aprad=float(args.aprad)
args.lpd=float(args.lpd)
args.lss=float(args.lss)
args.N=int(args.N)
if args.describe==dt:
    os.system("python AstraInputGenerator.py --aprad={0:.10f} --lpd={1:.20f} --lss={2:.20f} --N={3} ".format(args.aprad, args.lpd, args.lss, args.N)+"--describe="+args.describe)
    fname="aprad{}lpd{}lss{}N{}".format(args.aprad,args.lpd,args.lss,args.N)+dt
else:
    os.system("python AstraInputGenerator.py --aprad={0:.10f} --lpd={1:.20f} --lss={2:.20f} --N={3} ".format(args.aprad, args.lpd, args.lss, args.N)+"--describe="+args.describe+dt)
    fname="aprad{}lpd{}lss{}N{}".format(args.aprad,args.lpd,args.lss,args.N)+args.describe+dt
os.system("./Astra "+fname+".in")
os.system("python statisticsgenerator.py --delfiles={}".format(args.delfiles))