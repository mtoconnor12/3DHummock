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

num_runs = 18

directory = "./run.1"
keys, times, dat = parse_ats.readATS(directory, "visdump_data.h5", timeunits='yr')
ind = 9
col_dat = transect_data.transect_data(['saturation_ice'], keys=np.s_[ind], directory=directory)
nvar, nt, nx, nz = col_dat.shape

wtd = np.nan * np.ones((num_runs, nx),'d')

for j in range(1,num_runs):
	directory = "./run."+str(j)
	keys, times, dat = parse_ats.readATS(directory, "visdump_data.h5", timeunits='yr')

	## SELECT TIME INTERVAL TO PULL AND PLOT:
	# Visdumps are spit out every 30 days.  Index 0 is January of year 1; 12 is January year 2; etc...
	ind = 12*9 + 9

	col_dat = transect_data.transect_data(['saturation_ice'], keys=np.s_[ind], directory=directory)
	times_subset = times[ind]

	#print times_subset

	nvar, nt, nx, nz = col_dat.shape
	#print nt

	# z_surf and z_bott is extrapolated based on dz, and is not necessarily exact if 
	# dz varies in the top (respectively bottom) two cells
	z_surf = col_dat[1,0,:,-1] + (col_dat[1,0,:,-1] - col_dat[1,0,:,-2])/2. # average of the uppermost and second-to-uppermost rows, shifted up to the top row
	z_bott = col_dat[1,0,:,0] - (col_dat[1,0,:,1] - col_dat[1,0,:,0])/2. # average of the bottom and second-to-bottom rows, shifted up to the bottom row

	#print((col_dat[1,0,:,-1] - col_dat[1,0,:,-2])/2.)

	# We want the index of the deepest cell that has no ice.

	# Determine the index of the lowest unsaturated cell at each time and x coordinate.
	# Note that this is the right choice for water table, as a saturated zone might exist 
	# on TOP of an unsaturated zone, for a perched aquifer, so we DON'T want the highest 
	# saturated cell

	# print(col_dat[1,1,:,-1])
	#print(wtd.shape)
	for i in range(nx): # search each column across the domain
		where_unsat = np.where(col_dat[2,0,i,:] == 0)[0]
		if len(where_unsat) == 0:
			# nothing is unsaturated
			wtd[j,i] = 0.
		elif where_unsat[0] == 0:
			# nothing is saturated, wtd is the full column thickness (i.e. the bottom)
			wtd[j,i] = z_surf[i] - z_bott[i]
		else:
			# wt is in the domain -- average the first unsaturated with the last 
			# saturated, then subtract from the surf to get depth
			#print i
			#print z_surf[i]
			#print col_dat.shape	
			#print where_unsat.shape
			#print col_dat[1,:,i,where_unsat[0]-1]
			wtd[j,i] = z_surf[i] - (col_dat[1,:,i,where_unsat[0]] + col_dat[1,:,i,where_unsat[0]-1])/2 
		#print(where_unsat)
		
# plot
fig,ax = plt.subplots(1,1, figsize=(18,6))
cm = colors.cm_mapper(0,num_runs-1)
for j in range(1,num_runs):
	ax.plot(col_dat[0,0,:,0], -wtd[j,:], color=cm(j), label="{0} run".format(j))
ax.set_xlabel("x [m]")
ax.set_ylabel("depth to ice table [m]")
ax.legend()
plt.show()
