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

#####################################
# Create a plot for the NVT density
# (just for visualization purposes,
# as it will not change with time
#####################################

data_nvt = np.genfromtxt("properties.nvt.dat")

timestep = data_nvt[:, 0]
density_nvt = data_nvt[:, 1]
density_mean = np.mean(np.mean(data_nvt[:, 1]))
# We will plot the NVT density in the same plot
# as the NPT density. This why we use the same
# ax object

ax.plot(npt_last_timestep + timestep, density_nvt, '-', color="blue", label="NVT")

# The number 0.7873 is taken from the paper shared
# in class
ax.axhline(y=0.7873, color='r', linestyle='-', label='Reference')

ax.legend(loc="best")
ax.yaxis.set_label_position("left")

annotation = "Figure 1. Ethanol density at 298K"
plt.annotate(annotation, (0,0), (-150, -40), xycoords='axes points', textcoords='offset points', va='top')

# Print the mean of the density
print("Density mean: ", density_mean)

#####################################
# Create a new plot (fig2, ax2) that  
# will contain the RDF from PyLAT 
#####################################

fig2, ax2 = plt.subplots(1, 1)
ax2.set_xlabel(r'Distance ($\AA$)')
ax2.set_ylabel('$g(r)$')

# Open the ethanol.json file (or whatever name
# you gave to it when executing PyLAT)
# and use the json library to parse its
# content

with open("etoh.json", mode="r") as f:
    rdf = json.load(f)

# Plot the RDF
ax2.plot(rdf["RDF"]["distance"], rdf["RDF"]["etoh-etoh"], '-', color="black", label="RDF")

#####################################
# Create a new plot (fig3, ax3) that  
# will contain the MSD from PyLAT 
#####################################

fig3, ax3 = plt.subplots(1, 1)
ax3.set_xlabel(r'Time (ps)')
ax3.set_ylabel('MSD')

with open("etoh.json", mode="r") as f:
    msd = json.load(f)

# The time in PyLAT is in fs. The x axis of 
# Figure 7 of the paper is in ps. We need to
# divide by 1000.0

time = np.array(msd["MSD"]["time"]) / 1000.0

ax3.plot(time, msd["MSD"]["etoh"], '-', color="black", label="MSD")
ax3.set_xlim([0, 10])
ax3.set_ylim([0, 10])

plt.show()
