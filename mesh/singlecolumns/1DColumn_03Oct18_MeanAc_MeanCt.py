import sys, os

sys.path.append(os.path.join(os.environ['ATS_SRC_DIR'],'tools','meshing_ats'))
import meshing_ats
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import math

x = np.linspace(0,1,2) # array from 0 to 1 with 2 points at 0 and 1
y = np.linspace(0,1,2) # array from 0 to 1 with 2 points at 0 and 1

[X,Y] = np.meshgrid(x,y)
Zsurf = np.zeros((2,2))

m2 = meshing_ats.Mesh2D.from_2DSurface(x,y,Zsurf) #1D x, 1D y, and 2D Z

# layer extrusion
layer_types = []
layer_data = []
layer_ncells = []
layer_mat_ids = []

z=0
Z = []
n1 = 10 # ac thickness = 4 cm (1cm-thick layers * 2 layers) 
n2 = 7 # ct thickness = 0 cm (2cm-thick layers * 0 layers)
n3 = 20 # min thickness upper nodes
n4 = 10 # min thickness lower nodes
n5 = 12 # bedrock thickness

for i in range(n1): # acrotelm
    layer_types.append('constant')
    layer_data.append(0.01)
    layer_ncells.append(1)
    layer_mat_ids.append(1001)
    z = z + 0.01
    Z.append(z)
print (z)  

for i in range(n2): # catotelm
    layer_types.append('constant')
    layer_data.append(0.02)
    layer_ncells.append(1)
    layer_mat_ids.append(1002)
    z = z + 0.02
    Z.append(z)
print (z)

dz = .02
for i in range(n3): # mineral loess
    dz *= 1.1
    layer_types.append("constant")
    layer_data.append(dz)
    layer_ncells.append(1)
    layer_mat_ids.append(1003)
    #print ('3rd layer',z)
    z = z + dz
    Z.append(z)
print (z)

for i in range(n4): # mineral loess
    dz *= 1.2
    layer_types.append("constant")
    layer_data.append(dz)
    layer_ncells.append(1)
    layer_mat_ids.append(1003)
    #print ('3rd layer',z)
    z = z + dz
    Z.append(z)
print (z)

for i in range(n5): # bedrock
    dz *= 1.2
    layer_types.append("constant")
    layer_data.append(dz)
    layer_ncells.append(1)
    layer_mat_ids.append(1004)
    #print ('5th layer',z)
    z = z + dz
    Z.append(z)
	
print (z)
print(len(layer_types),layer_types[-1])
print(len(layer_mat_ids),layer_mat_ids[-1])

#layer_types.append('snapped')
#layer_data.append(-40.0) # bottom location
#layer_ncells.append(2)
#layer_mat_ids.append(1004)

m3 = meshing_ats.Mesh3D.extruded_Mesh2D(m2, layer_types, 
                                        layer_data, 
                                        layer_ncells, 
                                        layer_mat_ids)

m3.write_exodus("column-04Oct18_MeanAc_MeanCt.exo")