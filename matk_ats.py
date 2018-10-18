import matplotlib
matplotlib.use('agg')

import matk
import parse_ats
import atsxml

def model(pars, hostname='dum', processor=1):
    m = atsxml.get_root('../test0-i.xml')
    atsxml.replace_by_path(m, ['base_porosity', 'peat', 'value'], pars['poro'])

    atsxml.run(m, nproc=1, mpiexec='mpirun', stdout='stdout.out', stderr='stdout.err', cpuset=processor)
    return True


njobs = 8
hosts = {'dum': map(str, range(njobs))}

p = matk.matk(model=model)
p.add_par('poro', min=0.25, max=0.75, value=0.5)
s = p.parstudy(nvals=[8,])
s.savetxt('sample.txt')
s.run(cpus=hosts, workdir_base='run', reuse_dirs=True)
