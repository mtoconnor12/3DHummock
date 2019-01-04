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
lenX = 6
lenY = 2
lenXDomain = 500
dx = 0.1
dy = 0.1
dxDomain = 10
m = 0.05

nx1 = lenX/dx
ny1 = lenY/dy
x1 = np.linspace(0,lenX,nx1)
y1 = np.linspace(0,lenY,ny1)
[X1,Y1] = np.meshgrid(x1,y1)
Z1 = A*np.sin(k1*X1)*np.sin(k2*Y1) + m*X1

nx2 = lenXDomain/dxDomain
ny2 = lenY/dy
x2 = np.linspace(lenX,lenXDomain,nx2)
y2 = np.linspace(0,lenY,ny2)
[X2,Y2] = np.meshgrid(x2,y2)
Z2 = m*X2

x = np.concatenate((x1,x2),axis=0)
y = np.concatenate((y1,y2),axis=0)
Z = np.concatenate((Z1,Z2),axis=0)

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
m3.write_exodus("3DHummock_40x_40y_70z_19Nov18.exo")
#m3.write_exodus("column-peat20cm.exo")

