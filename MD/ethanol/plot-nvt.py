"""
Plotting script for LAMMPS property file
NVT trajectory
"""

import matplotlib.pyplot as plt
import numpy as np
import json

####################################
# Create a plot for the NVT pressure
####################################

data_nvt = np.genfromtxt("properties.nvt.dat")

timestep = data_nvt[:, 0]
p = data_nvt[:, 3]
toteng = data_nvt[:, 6]
pe = data_nvt[:, 5]
ke = data_nvt[:, 4]

fig, ax = plt.subplots(1, 1)

ax.spines["bottom"].set_linewidth(3)
ax.spines["left"].set_linewidth(3)
ax.spines["right"].set_linewidth(3)
ax.spines["top"].set_linewidth(3)
ax.set_xlabel("Timestep")
ax.set_ylabel("Pressure (atm)")
ax.yaxis.tick_left()

ax.plot(timestep, p, "-", color="black", label="Pressure")

ax.legend(loc="best")
ax.yaxis.set_label_position("left")

fig2, ax2 = plt.subplots(1, 1)

ax2.spines["bottom"].set_linewidth(3)
ax2.spines["left"].set_linewidth(3)
ax2.spines["right"].set_linewidth(3)
ax2.spines["top"].set_linewidth(3)
ax2.set_xlabel("Timestep")
ax2.set_ylabel("Energy (kcal/mol)")
ax2.yaxis.tick_left()

ax2.plot(timestep, toteng, "-", color="black", label="Total energy")
ax2.plot(timestep, pe, "-", color="red", label="Potential energy")
ax2.plot(timestep, ke, "-", color="blue", label="Kinetic energy")

ax2.legend(loc="best")
ax2.yaxis.set_label_position("left")

plt.show()
