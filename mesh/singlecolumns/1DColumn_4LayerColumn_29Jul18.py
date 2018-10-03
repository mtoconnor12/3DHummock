import sys, os

sys.path.append(os.path.join(os.environ['ATS_SRC_DIR'],'tools','meshing_ats'))
import meshing_ats

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

m2 =meshing_ats.Mesh2D.read_VTK('column.vtk')

# layer extrusion
layer_types = []
layer_data = []
layer_ncells = []
layer_mat_ids = []

z=0
Z = []
n1,n2 = 8, 8 # two 16cm-thick layers of peat: acrotelm over catotelm 

# for i in range(2): # 2 cm moss layer with 1 cm resolution
    # layer_types.append('constant')
    # layer_data.append(0.01)
    # layer_ncells.append(1)
    # layer_mat_ids.append(1001)
    # z = z + 0.01
    # Z.append(z)
# print (z)

for i in range(n1): # acrotelm
    layer_types.append('constant')
    layer_data.append(0.02)
    layer_ncells.append(1)
    layer_mat_ids.append(1001)
    z = z + 0.02
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
for i in range(42): # mineral loess
    dz *= 1.05
    layer_types.append("constant")
    layer_data.append(dz)
    layer_ncells.append(1)
    layer_mat_ids.append(1003)
    #print ('3rd layer',z)
    z = z + dz
    Z.append(z)
print (z)

for i in range(12): # bedrock
    dz *= 1.2
    layer_types.append("constant")
    layer_data.append(dz)
    layer_ncells.append(1)
    layer_mat_ids.append(1004)
    #print ('3rd layer',z)
    z = z + dz
    Z.append(z)
print (z)

for i in range(8): # bedrock
    dz *= 1.2
    layer_types.append("constant")
    layer_data.append(dz)
    layer_ncells.append(1)
    layer_mat_ids.append(1004)
    #print ('5th layer',z)
    z = z + dz
    Z.append(z)
	
print (z)
layer_types.append('snapped')
layer_data.append(-40.0) # bottom location
layer_ncells.append(2)
layer_mat_ids.append(1004)

m3 = meshing_ats.Mesh3D.extruded_Mesh2D(m2, layer_types, 
                                        layer_data, 
                                        layer_ncells, 
                                        layer_mat_ids)

m3.write_exodus("column-4Zones_29Jul18.exo")