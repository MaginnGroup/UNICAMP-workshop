"""
Plotting script for pylat json file
"""

import matplotlib.pyplot as plt
import numpy as np
import json

#####################################
# Create a new plot (fig2, ax2) that
# will contain the RDF from PyLAT
#####################################

fig, ax = plt.subplots(1, 1)
ax.set_xlabel(r"Distance ($\AA$)")
ax.set_ylabel("$g(r)$")

# Open the ethanol.json file (or whatever name
# you gave to it when executing PyLAT)
# and use the json library to parse its
# content

with open("etoh.json", mode="r") as f:
    rdf = json.load(f)

# Plot the RDF
ax.plot(
    rdf["RDF"]["distance"], rdf["RDF"]["etoh-etoh"], "-", color="black", label="RDF"
)

#####################################
# Create a new plot (fig3, ax3) that
# will contain the MSD from PyLAT
#####################################

fig2, ax2 = plt.subplots(1, 1)
ax2.set_xlabel(r"Time (ps)")
ax2.set_ylabel("MSD")

with open("etoh.json", mode="r") as f:
    msd = json.load(f)

# The time in PyLAT is in fs. The x axis of
# Figure 7 of the paper is in ps. We need to
# divide by 1000.0

time = np.array(msd["MSD"]["time"]) / 1000.0

ax2.plot(time, msd["MSD"]["etoh"], "-", color="black", label="MSD")
ax2.set_xlim([0, 10])
ax2.set_ylim([0, 10])

plt.show()
