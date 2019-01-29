import matplotlib
matplotlib.use('agg')

import numpy as np
from matk import matk
import parse_ats
import atsxml

#checkpointRunName = "_27Nov18"

def model(pars, hostname='dum', processor=1):
	# ATS ##############################################################################
    	# Modify base ats xml input file and run ats
	branchName = "Paper2_ParamSweep_300m"
	fname = branchName + "-" + str(pars['bac']) + "bac_" + str(pars['bct']) + "bct"
	
	m = atsxml.get_root('../test7_' + 'Paper2_NoCheckpoint_NoVerbosity_Default.xml')
	
	atsxml.replace_by_path(m,['mesh','domain','read mesh file parameters','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','computational domain acrotelm','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','computational domain catotelm','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','computational domain mineral','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','computational domain bedrock','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','surface','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','bottom face','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['state','permeability','function','acrotelm','function','function-constant','value'],pars['Kac'])
	atsxml.replace_by_path(m,['state','permeability','function','catotelm','function','function-constant','value'],pars['Kct'])
	atsxml.replace_by_path(m,['state','permeability','function','rest domain','function','function-constant','value'],pars['Kmn'])

    	atsxml.run(m, nproc=1, mpiexec='mpirun', stdout='stdout.out', stderr='stdout.err', cpuset=processor)
	return True


# Create cpusets, 4 cpus to a set
# This is necessary so that the ATS runs get spread evenly over processors and doesn't stack up on processors
# On our servers, the host key ('dum' below) isn't necessary since we run all jobs on the same server.
# On clusters, you may be sending different runs to different hosts (computers). 
# In that case, the dictionary keys are important for indicating the host.
# The dictionary values (lists of integers) identify which processors to put each ATS run.
njobs = 32
nparams = 6
hosts = {'dum': map(str, range(njobs))}

# Instantiate MATK object specifying the "model" function defined above as the MATK "model"
p = matk(model=model)

# Add parameters that you want to sample over and their ranges
p.add_par('bac', min=0.01, max=0.22, value=0.1)
p.add_par('bct',min=0.02, max=0.4, value=0.14)
p.add_par('Kac',min=1.03e-3, max=2.8e-3, value=1.92e-3)
p.add_par('Kct',min=2.52e-6, max=3.51e-5, value = 5e-6)
p.add_par('Kmn',min=2.09e-6, max=1.25e-5, value = 5e-6)
p.add_par('RunNum',min=1,max=32, value = 6)

# Create list of landscape type names
colNames = ['TussockTundraHi','TussockTundraLo','WaterTrack','WoodyShrubsHillslope','SedgeHi','WoodyShrubsRiparianHi','SedgeLo','FrostBoils']

# Create matrix of parameter combinations
ac = [0.09,0.17]
ct = [0.06,0.14]

Kac = [9.35e-11,2.54e-10]
Kct = [2.29e-13,3.18e-12]
Kmn = [1.90e-13,1.14e-12]

d = np.empty([njobs,nparams])
c = 0
runName = 'TussockTundraHi'
suffix = '_18Dec18'
checkpointSuffix = '_05Dec18'
for i1 in range(2):
	for i2 in range(2):
		for i3 in range(2):
			for i4 in range(2):
				for i5 in range(2):
					d[c] = [ac[i1],ct[i2],Kac[i3],Kct[i4],Kmn[i5],c+1]
					c = c + 1			

#d = [[0.01,0.01,0.02],[0.01,0.01,0.14],[0.01,0.01,0.4],[0.01,0.1,0.02],[0.01,0.1,0.14],[0.01,0.1,0.4],[0.01,0.

# Create MATK sampleset
s = p.create_sampleset(d)

# Create parameter study of all combinations of min and max values for each parameter
# s = p.parstudy(nvals=[2,3,3])
# Save samples to file for inspection
# s.savetxt('sample.txt')
# Run sampleset using "hosts" dictionary defined above. 
s.run(cpus=hosts, workdir_base=runName + suffix, reuse_dirs=True)
