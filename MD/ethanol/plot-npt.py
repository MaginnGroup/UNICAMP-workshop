# Plotting script for LAMMPS property file
# For NPT equilibration run

import matplotlib.pyplot as plt
import numpy as np
import json

###################
# NPT-EQUILIBRATION
###################

# Load the data output by the MD simulation
# into numpy arrays

data_npt = np.genfromtxt("properties.npt.dat")

# The column order is defined in the lammps input
# file. Python indexing starts with 0. That means, 
# that the first column is refered as the zeroth
# column

timestep = data_npt[:, 0]
density_npt = data_npt[:, 1]

#####################################
# Create a plot for the NPT densities
#####################################

fig, ax = plt.subplots(1, 1)

ax.spines["bottom"].set_linewidth(3)
ax.spines["left"].set_linewidth(3)
ax.spines["right"].set_linewidth(3)
ax.spines["top"].set_linewidth(3)

#ax.grid()
#ax.title.set_text('Ethanol density at 298K')
ax.set_xlabel(r'Timestep')
ax.set_ylabel('Density $(g/cm^3)$')
ax.yaxis.tick_left()
#ax.set_xlim([-1500, 300])
#ax.set_ylim([220, 350])
ax.plot(timestep, density_npt, '-', color="black", label="NPT")
npt_last_timestep = timestep[-1]


# The number 0.7873 is taken from the paper shared                                                                    
# in class                                                                                                            
ax.axhline(y=0.7873, color='r', linestyle='-', label='Reference')

ax.legend(loc="best")
ax.yaxis.set_label_position("left")

annotation = "Figure 1. Ethanol density at 298K"
plt.annotate(annotation, (0,0), (-150, -40), xycoords='axes points', textcoords='offset points', va='top')


plt.show()
