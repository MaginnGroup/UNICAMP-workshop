"""
Plotting script for LAMMPS property file
for NPT equilibration run
"""

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


half_idx = len(density_npt) // 2
equil_density = density_npt[half_idx:]
equil_timestep = timestep[half_idx:]
mean_density = np.round(np.mean(equil_density), 4)
# The number 0.7873 is taken from the paper shared
# in class
mean_reference = 0.7873

ax.title.set_text(f"Ethanol density at 298K. Mean: {mean_density} $g/cm^3$")
ax.set_xlabel(r"Timestep")
ax.set_ylabel("Density $(g/cm^3)$")
ax.yaxis.tick_left()

ax.plot(timestep, density_npt, "-", color="black", label="NPT")
ax.plot(equil_timestep, equil_density, "-", color="blue", label="Equilibrated NPT")

ax.axhline(y=mean_density, color="b", linestyle="-", label="Mean Equilibrated NPT")
ax.axhline(y=mean_reference, color="r", linestyle="-", label="Reference")

ax.legend(loc="best")
ax.yaxis.set_label_position("left")

plt.show()
