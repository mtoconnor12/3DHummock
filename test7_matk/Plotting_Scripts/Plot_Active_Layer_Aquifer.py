import sys,os
sys.path.append(os.path.join(os.environ['ATS_SRC_DIR'],'tools', 'utils'))
import parse_xmf, parse_ats
import column_data, transect_data
import colors
import mesh
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import colorbar

## Testing the datetime functionality
dt = datetime.fromordinal(733828)
dt
dt.strftime('%Y%m%d')

directory = "./hillslope-test-allMinColumn"

keys, times, dat = parse_ats.readATS(directory, "visdump_data.h5", timeunits='yr')

## SELECT TIME INTERVAL TO PULL AND PLOT:
# Visdumps are spit out every 30 days.  Index 0 is January of year 1; 12 is January year 2; etc...
ind_start = 180 + 270
ind_end = 181 + 720 # if you want it to run to the end of the list, type '-1' for the last item on the list.
ind_int = 1 # there is one checkpoint file every 30 days

col_dat = transect_data.transect_data(['saturation_gas','saturation_ice'], keys=np.s_[ind_start:ind_end:ind_int], directory=directory)
times_subset = times[ind_start:ind_end:ind_int]

print times_subset

nvar, nt, nx, nz = col_dat.shape
print nt

# z_surf and z_bott is extrapolated based on dz, and is not necessarily exact if 
# dz varies in the top (respectively bottom) two cells
z_surf = col_dat[1,0,:,-1] + (col_dat[1,0,:,-1] - col_dat[1,0,:,-2])/2. # average of the uppermost and second-to-uppermost rows, shifted up to the top row
z_bott = col_dat[1,0,:,0] - (col_dat[1,0,:,1] - col_dat[1,0,:,0])/2. # average of the bottom and second-to-bottom rows, shifted up to the bottom row

print((col_dat[1,0,:,-1] - col_dat[1,0,:,-2])/2.)
#print(col_dat[1,0,:,-2])

plt.plot(col_dat[1,0,:,-1] + (col_dat[1,0,:,-1] - col_dat[1,0,:,-2])/2.)
plt.show()

# We want the index of the deepest cell that has no ice.

# Determine the index of the lowest unsaturated cell at each time and x coordinate.
# Note that this is the right choice for water table, as a saturated zone might exist 
# on TOP of an unsaturated zone, for a perched aquifer, so we DON'T want the highest 
# saturated cell.
wtd = np.nan * np.ones((col_dat.shape[1], col_dat.shape[2]),'d')

## Determine water table
# print(col_dat[1,1,:,-1])
print(wtd.shape)
for i in range(nx): # search each column across the domain
    for k in range(nt): # search each time
        where_unsat = np.where(col_dat[2,k,i,:] > 0.01)[0]
        if len(where_unsat) == 0:
            # everything is saturated
            wtd[k,i] = 0.
        elif where_unsat[0] == 0:
            # nothing is saturated, wtd is the full column thickness (i.e. the bottom)
            wtd[k,i] = z_surf[i] - z_bott[i]
        else:
            # wt is in the domain -- average the deepest unsaturated cell with the next deepest cell, which is 
            # saturated, then subtract from the surf to get depth
            #print(col_dat[2,k,i,:])
            #print(where_unsat)
            wtd[k,i] = z_surf[i] - (col_dat[1,k,i,where_unsat[0]] + col_dat[1,k,i,where_unsat[0] - 1])/2 
        #print(where_unsat)
        #print(where_unsat[0])-1
        #print(col_dat[1,k,i,where_unsat[0]])
        #print(col_dat[1,k,i,where_unsat[0]-1])
        
## Determine ice table
itd = np.nan * np.ones((col_dat.shape[1], col_dat.shape[2]),'d')

for i in range(nx): # search each column across the domain
    for k in range(nt): # search each time
        where_unsat = np.where(col_dat[3,k,i,:] == 0)[0]
        if len(where_unsat) == 0:
            # nothing is unsaturated
            itd[k,i] = 0.
        elif where_unsat[0] == 0:
            # nothing is saturated, wtd is the full column thickness (i.e. the bottom)
            itd[k,i] = z_surf[i] - z_bott[i]
        else:
            # wt is in the domain -- average the first unsaturated with the last 
            # saturated, then subtract from the surf to get depth
            itd[k,i] = z_surf[i] - (col_dat[1,k,i,where_unsat[0]] + col_dat[1,k,i,where_unsat[0]-1])/2 
        
# plot
fig,ax = plt.subplots(1,1,figsize=(18,6))
cm = colors.cm_mapper(0,nt-1)
#print nt

#ax = ax.ravel()
#for i in range(2):
for k in range(nt):
    ax.plot(col_dat[0,0,:,0], -wtd[k,:], color='b', label="{0} years".format(times_subset[k]))
    ax.plot(col_dat[0,0,:,0], -itd[k,:], color='c', label="{0} years".format(times_subset[k]))
ax.set_xlabel("x [m]")
ax.set_ylabel("depth to water table [m]")
ax.legend()
plt.show()
