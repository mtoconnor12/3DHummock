#!usr/bin/env python
"""Plots any dat file assuming time is in seconds.
"""
import numpy as np
from matplotlib import pyplot as plt
import sys

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

for i in range(1,18):
	#print i
	mat = np.loadtxt('run.' + str(i) + '/subsurface_outlet_flux.dat')
	t = mat[:,0]/86400/365  # time in days
	y = mat[:,1] # thing we're plotting
	leg_ordered[i-1] = leg[i-1] 
	plt.plot(t,y)

plt.xlabel('Time [yrs]')
plt.title('subsurface outlet flux')
plt.yscale('log')
plt.legend(leg_ordered)
plt.show() 
