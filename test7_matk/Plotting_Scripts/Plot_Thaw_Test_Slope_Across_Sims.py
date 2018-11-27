#!usr/bin/env python
"""Plots any dat file assuming time is in seconds.
"""
import sys,os
sys.path.append(os.path.join(os.environ['ATS_SRC_DIR'],'tools', 'utils'))
import parse_xmf, parse_ats
import column_data, transect_data
import colors
import mesh
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import colorbar



nruns = 18
c = 0
leg = [None]*nruns
m = [0.01,0.1]
bac = [0.01,0.1,0.22]
bct = [0.02,0.14,0.4]

for i in range(2):
	for j in range(3):
		for k in range(3):
			print m[i]
			leg[c] = ['m=' + str(m[i]) + ' bac=' + str(bac[j]) + ' bct=' + str(bct[k])]
			c = c + 1

		

leg_ordered = [None]*18

# Low-sloping domains: simulations 1-9
# Hi-sloping domains: simulations 10-18

fix,axarr = plt.subplots(3,3,sharey=True,sharex=True)
c = 1
ind = 12*9 + 9
for i in range(3):
	for j in range(3):	
		directory = "./run."+str(c)
		keys, times, dat = parse_ats.readATS(directory, "visdump_data.h5", timeunits='yr')
		
		col_dat = transect_data.transect_data(['saturation_ice'], keys=np.s_[ind], directory=directory)
		times_subset = times[ind]
		nvar, nt, nx, nz = col_dat.shape
		wtd = np.nan*np.ones((nx),'d')
		print(wtd.shape)
		z_surf = col_dat[1,0,:,-1] + (col_dat[1,0,:,-1] - col_dat[1,0,:,-2])/2. # average of the uppermost and second-to-uppermost rows, shifted up to the top row
		z_bott = col_dat[1,0,:,0] - (col_dat[1,0,:,1] - col_dat[1,0,:,0])/2. # average of the bottom and second-to-bottom rows, shifted up to the bottom row

		for k in range(nx):
			where_unsat = np.where(col_dat[2,0,k,:] == 0)[0]
			if len(where_unsat) == 0:
				wtd[k] = 0.
			elif where_unsat[0] == 0:
				wtd[k] = z_surf[k] - z_bott[k]
			else:
				#print k
				#print z_surf[k]
				#print col_dat[1,:,k,where_unsat[0]]
				print where_unsat[0]-1
				print wtd
				wtd[k] = z_surf[k] - (col_dat[1,:,k,where_unsat[0]] + col_dat[1,:,k,where_unsat[0]-1])/2 
			#print(where_unsat)
			
		axarr[i,j].plot(col_dat[0,0,:,0],-wtd)
		
		#### Hi Slope
		directory = "./run."+str(c + 9)
		keys, times, dat = parse_ats.readATS(directory, "visdump_data.h5", timeunits='yr')
		
		col_dat = transect_data.transect_data(['saturation_ice'], keys=np.s_[ind], directory=directory)
		times_subset = times[ind]
		nvar, nt, nx, nz = col_dat.shape
		wtd = np.nan*np.ones((nx),'d')
		
		z_surf = col_dat[1,0,:,-1] + (col_dat[1,0,:,-1] - col_dat[1,0,:,-2])/2. # average of the uppermost and second-to-uppermost rows, shifted up to the top row
		z_bott = col_dat[1,0,:,0] - (col_dat[1,0,:,1] - col_dat[1,0,:,0])/2. # average of the bottom and second-to-bottom rows, shifted up to the bottom row

		for k in range(nx):
			where_unsat = np.where(col_dat[2,0,k,:] == 0)[0]
			if len(where_unsat) == 0:
				wtd[k] = 0.
			elif where_unsat[0] == 0:
				wtd[k] = z_surf[k] - z_bott[k]
			else:
				wtd[k] = z_surf[k] - (col_dat[1,:,k,where_unsat[0]] + col_dat[1,:,k,where_unsat[0]-1])/2 
			#print(where_unsat)
			
		axarr[i,j].plot(col_dat[0,0,:,0],-wtd)
		c = c + 1

		plt.legend(['low slope','high slope'])
plt.show() 
