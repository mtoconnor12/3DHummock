import matk
import numpy
from scipy import arange, randn, exp

## Following the tutorial set at: http://dharp.github.io/matk/getting_started.html

# Define a model
def dbexpl(p):
    t=arange(0,100,20.)
    y = (p['par1']*exp(-p['par2']*t) + p['par3']*exp(-p['par4']*t))
    ydict = dict([('obs'+str(i+1), v)  for i,v in enumerate(y)])
    return ydict

# Make a matk object from the model
p = matk.matk(model=dbexpl)

# Add matk parameters
p.add_par('par1',min=0,max=1,value=0.5)
p.add_par('par2',min=0,max=0.2,value=0.1)
p.add_par('par3',min=0,max=1,value=0.5)
p.add_par('par4',min=0,max=0.2,value=0.1)

# Check current params
print p.parvalues #mean value
print p.parnames # parameter name
print p.parmins # min value
print p.parmaxs # max value

print p.pars # prints it all
print p.pars['par1'] # prints only the first value

# Add observations (obs are values you want to compare model results to)
observations = [1., 0.14, 0.021, 2.4e-3, 3.4e-4]
for i,o in enumerate(observations): p.add_obs( 'obs'+str(i+1), value=o)

sims = p.forward()
print sims
print p.obs
print p.simvalues
#print p.ssr


