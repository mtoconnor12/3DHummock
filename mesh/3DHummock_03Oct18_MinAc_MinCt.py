import sys, os

sys.path.append(os.path.join(os.environ['ATS_SRC_DIR'],'tools','meshing_ats'))
print(sys.path)
import meshing_ats
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import math

# From a fucntion
# To get topography from a function, define it here, e.g., z = sine(x)
A = 0.15
k1 = math.pi
k2 = math.pi
m = 0.1

x = np.linspace(0,2,101)
y = np.linspace(0,2,101)


[X,Y] = np.meshgrid(x,y)

Z = A*np.sin(k1*X)*np.sin(k2*Y) + m*X


#plt.contourf(X,Y,Z)

""" 
# 2D Hillslope from a fucntion
# Topography from a function: e.g., z = sine(x)

x = np.linspace(0,500,501)
x0,z0 = 0, 5
z = z0 + 0.25 * (x - x0)

plt.plot(x, z, '.')
plt.title('Mesh, Polygon Area C')
plt.show()
m2 = meshing_ats.Mesh2D.from_Transect(x,z)
"""

import meshing_ats
m2 = meshing_ats.Mesh2D.from_2DSurface(x,y,Z) #1D x, 1D y, and 2D Z
#m2.plot()


# layer extrusion
layer_types = []
layer_data = []
layer_ncells = []
layer_mat_ids = []

z=0
Z = []
n1,n2 = 4, 20 #8cm peat 
#n1, n2 = 10, 14 #20cm peat

for i in range(2):
    layer_types.append('constant')
    layer_data.append(0.01)
    layer_ncells.append(1)
    layer_mat_ids.append(1001)
    z = z + 0.01
    Z.append(z)
print (z)

for i in range(n1): #8cm peat n=4, 20cm peat n=10
    layer_types.append('constant')
    layer_data.append(0.02)
    layer_ncells.append(1)
    layer_mat_ids.append(1002)
    z = z + 0.02
    Z.append(z)
print (z)  
for i in range(n2): #8cm peat, n=20, 20cm peat n = 14
    layer_types.append('constant')
    layer_data.append(0.02)
    layer_ncells.append(1)
    layer_mat_ids.append(1003)
    z = z + 0.02
    Z.append(z)
print (z)
dz = .02
for i in range(21):
    dz *= 1.05
    layer_types.append("constant")
    layer_data.append(dz)
    layer_ncells.append(1)
    layer_mat_ids.append(1003)
    #print ('3rd layer',z)
    z = z + dz
    Z.append(z)
print (z)

for i in range(17):
    dz *= 1.2
    layer_types.append("constant")
    layer_data.append(dz)
    layer_ncells.append(1)
    layer_mat_ids.append(1003)
    #print ('3rd layer',z)
    z = z + dz
    Z.append(z)
print (z)


for i in range(8):
    dz *= 1.2
    layer_types.append("constant")
    layer_data.append(dz)
    layer_ncells.append(1)
    layer_mat_ids.append(1003)
    #print ('5th layer',z)
    z = z + dz
    Z.append(z)
print (z)
#layer_types.append('snapped') #snapped is to flat the bottom
#layer_data.append(-40.0) # bottom location
#layer_ncells.append(2) # these two cells will make the bottom at 40 m
#layer_mat_ids.append(1003)

m3 = meshing_ats.Mesh3D.extruded_Mesh2D(m2, layer_types, 
                                        layer_data, 
                                        layer_ncells, 
                                        layer_mat_ids)
m3.write_exodus("testgrid_mtoAttempt.exo")
#m3.write_exodus("column-peat20cm.exo")

