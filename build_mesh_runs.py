import sys,os
import subprocess
sys.path.append(os.path.join(os.environ['AMANZI_SRC_DIR'],'tools','amanzi_xml'))
sys.path.append(os.path.join(os.environ['ATS_SRC_DIR'],'tools','utils','atsxml'))
import atsxml
sys.path.append(os.path.join(os.environ['ATS_SRC_DIR'],'tools','meshing_ats'))
import meshing_ats
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import math

## This should be run from the TEST folder.  It will cd into each run folder for each.

# m = slope in [-]
# bac = thickness of acrotelm in m
# bct = thickness of catotelm in m

def make_30m_mesh(m,bac,bct,fname):
	x = np.linspace(0,30,31)
	x0,z0 = 0, 0
	Zsurf = z0 + m * (x - x0)
	m2 = meshing_ats.Mesh2D.from_Transect(x,Zsurf)

	# layer extrusion
	layer_types = []
	layer_data = []
	layer_ncells = []
	layer_mat_ids = []

	z=0
	Z = []
	dz_ac = 0.01 # spacing of acrotelm cells, m
	dz_ct = 0.02 # spacing of catotelm cells, m
	n1 = int(bac/dz_ac) # ac thickness = 4 cm (1cm-thick layers * 2 layers) 
	n2 = int(bct/dz_ct) # ct thickness = 0 cm (2cm-thick layers * 0 layers)
	n3 = 20 # number of mineral cells, upper nodes
	n4 = 10 # number of mineral cells, lower nodes
	n5 = 12 # bedrock thickness
	
	print(n1)

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
	
	meshName = fname + ".exo"

	m3 = meshing_ats.Mesh3D.extruded_Mesh2D(m2, layer_types, 
											layer_data, 
											layer_ncells, 
											layer_mat_ids)

	m3.write_exodus(meshName)
	
homedir = os.getcwd() ## This should be run from the HOME folder for the whole shebang.  It will cd into each run folder for each.
branchName = "hillslope-30mSuite"

## Pick the slopes and thicknesses 
m = [0.01,0.1]
bac = [0.05,0.1,0.15]
bct = [0.06,0.12,0.18]

## Run the loop to build the meshes
os.chdir(homedir + "/mesh")
os.mkdir(branchName)
os.chdir(homedir)

for i in range(2):
	for j in range(3):
		for k in range(3):
			fname = branchName + "-" + str(m[i]) + "m_" + str(bac[j]) + "bac_" + str(bct[k]) + "bct"
			os.chdir(homedir + "/mesh/" + branchName)
			make_30m_mesh(m[i],bac[j],bct[k],fname)

os.chdir(homedir + "/test7")
					
for i in range(2):
	for j in range(3):
		for k in range(3):
			fname = branchName + "-" + str(m[i]) + "m_" + str(bac[j]) + "bac_" + str(bct[k]) + "bct"
			os.mkdir(fname)
			os.chdir(fname)
			m = atsxml.get_root('../test7_hillslope-30mSuite_template.xml')
			atsxml.replace_by_path(m,['mesh','domain','read mesh file parameters','file'],'../../mesh/' + fname + '.exo')
			atsxml.replace_by_path(m,['regions','computational domain acrotelm','region: labeled set','file'],'../../mesh/' + fname + '.exo')
			atsxml.replace_by_path(m,['regions','computational domain catotelm','region: labeled set','file'],'../../mesh/' + fname + '.exo')
			atsxml.replace_by_path(m,['regions','computational domain mineral','region: labeled set','file'],'../../mesh/' + fname + '.exo')
			atsxml.replace_by_path(m,['regions','computational domain bedrock','region: labeled set','file'],'../../mesh/' + fname + '.exo')
			atsxml.replace_by_path(m,['regions','surface','region: labeled set','file'],'../../mesh/' + fname + '.exo')
			atsxml.replace_by_path(m,['regions','bottom face','region: labeled set','file'],'../../mesh/' + fname + '.exo')
			atsxml.run(m)
			os.chdir(homedir + "/test7")


			
			## tested out both the replace command from ethan on white board AND the atsxml command "replace-mesh" and got errors.  need to sort out how to edit the xml file, save the edited file, and run that in ats.