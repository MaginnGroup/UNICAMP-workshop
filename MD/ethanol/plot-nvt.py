# Plotting script for LAMMPS property file
# NVT trajectory
import matplotlib.pyplot as plt
import numpy as np
import json

#####################################
# Create a plot for the NVT density
# (just for visualization purposes,
# as it will not change with time
#####################################

data_nvt = np.genfromtxt("properties.nvt.dat")

timestep = data_nvt[:, 0]
pressure_nvt = data_nvt[:, 3]

fig, ax = plt.subplots(1, 1)

ax.spines["bottom"].set_linewidth(3)
ax.spines["left"].set_linewidth(3)
ax.spines["right"].set_linewidth(3)
ax.spines["top"].set_linewidth(3)
ax.set_xlabel(r'Timestep')
ax.set_ylabel('Pressure atm')
ax.yaxis.tick_left()



ax.plot(timestep, pressure_nvt, '-', color="blue", label="NVT")

ax.legend(loc="best")
ax.yaxis.set_label_position("left")

annotation = "Figure 1. Ethanol pressure at 298K"
plt.annotate(annotation, (0,0), (-150, -40), xycoords='axes points', textcoords='offset points', va='top')

plt.show()
