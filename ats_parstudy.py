import numpy
import mesh
from scipy.interpolate import griddata
import parse_ats
import atsxml
from matk import matk
import geophysics_ats
import cPickle as pickle
from collections import OrderedDict


def model(pars,hostname='dum',processor=4):

    # ATS ##############################################################################
    # Modify base ats xml input file and run ats
    m = atsxml.get_root('../test7-v_fwd.xml')
    atsxml.replace_by_path(m,['base_porosity','rest domain','value'],pars['poro_m'])
    atsxml.replace_by_path(m,['base_porosity','peat','value'],pars['poro_p'])
    atsxml.replace_by_path(m,['permeability','rest domain','value'],10**pars['perm_m'])
    atsxml.replace_by_path(m,['permeability','peat','value'],10**pars['perm_p'])
    atsxml.replace_by_path(m,['computational domain upper mineral','thermal conductivity of soil [W/(m-K)]'],pars['kth_m'])
    atsxml.replace_by_path(m,['computational domain peat','thermal conductivity of soil [W/(m-K)]'],pars['kth_p'])
    atsxml.run(m,nproc=4,stdout='stdout.out',stderr='stdout.err',cpuset=processor) 

    # Read results from ATS observation files
    out = OrderedDict()
    sec_per_day = 86400
    for i in range(1,4):
        d = numpy.genfromtxt('temp%d.dat'%i)
        for r in d[numpy.where(d[:,0]>153*sec_per_day)]:
            out['T%d_%d'%(i,r[0]/sec_per_day)] = r[1]
        d = numpy.genfromtxt('sat%d.dat'%i)
        for r in d[numpy.where(d[:,0]>153*sec_per_day)]:
            out['S%d_%d'%(i,r[0]/sec_per_day)] = r[1]

    return out

# Create cpusets, 4 cpus to a set
# This is necessary so that the ATS runs get spread evenly over processors and doesn't stack up on processors
# On our servers, the host key ('dum' below) isn't necessary since we run all jobs on the same server.
# On clusters, you may be sending different runs to different hosts (computers). 
# In that case, the dictionary keys are important for indicating the host.
# The dictionary values (lists of integers) identify which processors to put each ATS run.
njobs = 15
hosts = {'dum':[','.join([str(i+j) for j in range(4)]) for i in range(0,njobs*4,4)]}

# Instantiate MATK object specifying the "model" function defined above as the MATK "model"
p = matk(model=model)

# Add parameters that you want to sample over and their ranges
p.add_par('poro_m',min=0.5, max=0.7, value=0.6)
p.add_par('poro_p', min=0.7, max=0.9, value=0.8)
p.add_par('perm_m',min=-14., max=-12., value=-13)
p.add_par('perm_p', min=-13., max=-11., value=-12)
p.add_par('kth_m', min=1., max=3., value=2.)
p.add_par('kth_p', min=0.05, max=.5, value=0.225)

# Create parameter study of all combinations of min and max values (2 values each) for each parameter
s = p.parstudy(nvals=[2,2,2,2,2,2])
# Save samples to file for inspection
s.savetxt('sample.txt')
# Run sampleset using "hosts" dictionary defined above. 
s.run(cpus=hosts,workdir_base='run',outfile='sample.out',logfile='sample.log',reuse_dirs=True)

