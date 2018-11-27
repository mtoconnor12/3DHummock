import matplotlib
matplotlib.use('agg')

import numpy as np
from matk import matk
import parse_ats
import atsxml

def model(pars, hostname='dum', processor=1):
	# ATS ##############################################################################
    	# Modify base ats xml input file and run ats
	branchName = "hillslope-30mSuite"
	fname = branchName + "-" + str(pars['slope']) + "m_" + str(pars['bac']) + "bac_" + str(pars['bct']) + "bct"
	
	m = atsxml.get_root('../test7_hillslope-30mSuite_template_CenturySim_20cmBC.xml')
	
	atsxml.replace_by_path(m,['mesh','domain','read mesh file parameters','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','computational domain acrotelm','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','computational domain catotelm','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','computational domain mineral','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','computational domain bedrock','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','surface','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['regions','bottom face','region: labeled set','file'],'../../mesh/' + branchName + '/' + fname + '.exo')
	atsxml.replace_by_path(m,['cycle driver','restart from checkpoint file'],'../checkpoint_files_20cmBC/checkpoint_' + fname + '.h5')

    	atsxml.run(m, nproc=1, mpiexec='mpirun', stdout='stdout.out', stderr='stdout.err', cpuset=processor)
	return True


# Create cpusets, 4 cpus to a set
# This is necessary so that the ATS runs get spread evenly over processors and doesn't stack up on processors
# On our servers, the host key ('dum' below) isn't necessary since we run all jobs on the same server.
# On clusters, you may be sending different runs to different hosts (computers). 
# In that case, the dictionary keys are important for indicating the host.
# The dictionary values (lists of integers) identify which processors to put each ATS run.
njobs = 18
nparams = 3
hosts = {'dum': map(str, range(njobs))}

# Instantiate MATK object specifying the "model" function defined above as the MATK "model"
p = matk(model=model)

# Add parameters that you want to sample over and their ranges
p.add_par('slope',min=0.01, max=0.1, value=0.05)
p.add_par('bac', min=0.01, max=0.22, value=0.1)
p.add_par('bct',min=0.02, max=0.4, value=0.14)

# Create matrix of parameter combinations
m = [0.01,0.1]
ac = [0.01,0.1,0.22]
ct = [0.02,0.14,0.4]

d = np.empty([njobs,nparams])
c = 0
for i in range(2):
	for j in range(3):
		for k in range(3):
			d[c] = [m[i],ac[j],ct[k]]
			c = c + 1			

#d = [[0.01,0.01,0.02],[0.01,0.01,0.14],[0.01,0.01,0.4],[0.01,0.1,0.02],[0.01,0.1,0.14],[0.01,0.1,0.4],[0.01,0.

# Create MATK sampleset
s = p.create_sampleset(d)

# Create parameter study of all combinations of min and max values for each parameter
# s = p.parstudy(nvals=[2,3,3])
# Save samples to file for inspection
# s.savetxt('sample.txt')
# Run sampleset using "hosts" dictionary defined above. 
s.run(cpus=hosts, workdir_base='run_fromCheckpoint_CenturySim_20cmBC', reuse_dirs=True)
