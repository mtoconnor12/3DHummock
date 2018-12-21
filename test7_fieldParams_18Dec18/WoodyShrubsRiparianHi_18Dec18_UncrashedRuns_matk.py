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
	branchName = "hillslope-fieldParams_18Dec18"
	fname = branchName + "-" + str(pars['bac']) + "bac_" + str(pars['bct']) + "bct"
	
	m = atsxml.get_root('../test7_' + branchName + '_template' + '_18Dec18_UncrashedRuns' + '_input.xml')
	
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
	atsxml.replace_by_path(m,['cycle driver','restart from checkpoint file'],'../checkpoint_files/' + runName + checkpointSuffix + '/' + runName + checkpointSuffix + '.' + str(pars['RunNum']) + 'checkpoint_last.h5')

    	atsxml.run(m, nproc=1, mpiexec='mpirun', stdout='stdout.out', stderr='stdout.err', cpuset=processor)
	return True


# Create cpusets, 4 cpus to a set
# This is necessary so that the ATS runs get spread evenly over processors and doesn't stack up on processors
# On our servers, the host key ('dum' below) isn't necessary since we run all jobs on the same server.
# On clusters, you may be sending different runs to different hosts (computers). 
# In that case, the dictionary keys are important for indicating the host.
# The dictionary values (lists of integers) identify which processors to put each ATS run.
njobs = 20
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

d = np.empty([njobs,nparams])
d = [[0.08,0.1,1.05e-11,1.7e-12,1.05e-15,1],[0.08,0.1,1.05e-11,1.7e-12,7.11e-14,2],[0.08,0.1,1.05e-11,6.03e-12,1.05e-15,3],[0.08,0.2,1.05e-11,1.7e-12,1.05e-15,9],[0.08,0.2,1.05e-11,1.7e-12,7.11e-14,10],[0.08,0.2,1.05e-11,6.03e-12,1.05e-15,11],[0.08,0.2,1.05e-11,6.03e-12,7.11e-14,12],[0.08,0.2,1.57e-10,1.7e-12,7.11e-14,14],[0.08,0.2,1.57e-10,6.03e-12,1.05e-15,15],[0.08,0.2,1.57e-10,6.03e-12,7.11e-14,16],[0.16,0.1,1.05e-11,1.7e-12,1.05e-15,17],[0.16,0.1,1.05e-11,1.7e-12,7.11e-14,18],[0.16,0.1,1.05e-11,6.03e-12,1.05e-15,19],[0.16,0.2,1.05e-11,1.7e-12,1.05e-15,25],[0.16,0.2,1.05e-11,1.7e-12,7.11e-14,26],[0.16,0.2,1.05e-11,6.03e-12,1.05e-15,27],[0.16,0.2,1.05e-11,6.03e-12,7.11e-14,28],[0.16,0.2,1.57e-10,1.7e-12,1.05e-15,29],[0.16,0.2,1.57e-10,6.03e-12,1.05e-15,31],[0.16,0.2,1.57e-10,6.03e-12,7.11e-14,32]]
# Create MATK sampleset
runName = 'WoodyShrubsRiparianHi'
checkpointSuffix = '_18Dec18'
s = p.create_sampleset(d)

# Create parameter study of all combinations of min and max values for each parameter
# s = p.parstudy(nvals=[2,3,3])
# Save samples to file for inspection
# s.savetxt('sample.txt')
# Run sampleset using "hosts" dictionary defined above. 
s.run(cpus=hosts, workdir_base=runName + '_18Dec18_UncrashedRuns', reuse_dirs=True)
