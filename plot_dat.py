#!usr/bin/env python
"""Plots any dat file assuming time is in seconds.
"""
import numpy as np
from matplotlib import pyplot as plt
import sys

mat = np.loadtxt(sys.argv[1])
t = mat[:,0]/86400/365  # time in days
y = mat[:,1] # thing we're plotting
plt.plot(t,y)
plt.xlabel('Time [yrs]')
plt.title(sys.argv[1])
plt.yscale('log')
plt.show()

