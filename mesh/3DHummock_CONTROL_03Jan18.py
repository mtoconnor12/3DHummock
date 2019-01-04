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
lenY = 2
lenXDomain = 1000
dxDomain = 20
dy = 0.1
m = 0.05

nx = lenXDomain/dxDomain
ny = lenY/dy
x = np.linspace(-500,500,nx)
y = np.linspace(0,lenY,ny)
[X,Y] = np.meshgrid(x,y)
Z = m*X

m2 = meshing_ats.Mesh2D.from_2DSurface(x,y,Z) #1D x, 1D y, and 2D Z

# layer extrusion
layer_types = []
layer_data = []
layer_ncells = []
layer_mat_ids = []

z=0
Z = []
bac = 0.1
bct = 0.2
dz_ac = 0.01 # spacing of acrotelm cells, m
dz_ct = 0.02 # spacing of catotelm cells, m
n1 = int(bac/dz_ac) # ac thickness = 4 cm (1cm-thick layers * 2 layers) 
n2 = int(bct/dz_ct) # ct thickness = 0 cm (2cm-thick layers * 0 layers)
n3 = 20 # number of mineral cells, upper nodes
n4 = 10 # number of mineral cells, lower nodes
n5 = 12 # bedrock thickness

for i in range(n1): # acrotelm
	layer_types.append('constant')
	layer_data.append(dz_ac)
	layer_ncells.append(1)
	layer_mat_ids.append(1001)
	z = z + dz_ac
	Z.append(z)
print (z)  

for i in range(n2): # catotelm
	layer_types.append('constant')
	layer_data.append(dz_ct)
	layer_ncells.append(1)
	layer_mat_ids.append(1002)
	z = z + dz_ct
	Z.append(z)
print (z)

dz = dz_ct
for i in range(n3): # mineral loess
	dz *= 1.1
	layer_types.append("constant")
	layer_data.append(dz)
	layer_ncells.append(1)
	layer_mat_ids.append(1003)
	z = z + dz
	Z.append(z)
print (z)

for i in range(n4): # mineral loess
	dz *= 1.2
	layer_types.append("constant")
	layer_data.append(dz)
	layer_ncells.append(1)
	layer_mat_ids.append(1003)
	z = z + dz
	Z.append(z)
print (z)

for i in range(n5): # bedrock
	dz *= 1.2
	layer_types.append("constant")
	layer_data.append(dz)
	layer_ncells.append(1)
	layer_mat_ids.append(1004)
	z = z + dz
	Z.append(z)
print (z)
print(len(layer_types),layer_types[-1])
print(len(layer_mat_ids),layer_mat_ids[-1])

m3 = meshing_ats.Mesh3D.extruded_Mesh2D(m2, layer_types, 
                                        layer_data, 
                                        layer_ncells, 
                                        layer_mat_ids)
m3.write_exodus("3DHummock_CONTROL_03Jan18.exo")

