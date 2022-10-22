import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from mosdef_cassandra.analysis import ThermoProps

thermo = ThermoProps("./npt.out.prp")
density = thermo.prop("Mass_Density")
reference = 672.0
start = 1500000

idx = np.where(thermo.prop("MC_STEP") >= start)[0][0]
plt.plot(thermo.prop("MC_STEP"), density, label="Simulations")
plt.plot(thermo.prop("MC_STEP")[idx:], density[idx:], color="green")
plt.axhline(reference, color='r', linestyle='-', label='Reference')
mean = np.mean(density[idx:])
plt.axhline(mean, color='darkgreen', linestyle='-', label='Simulation mean')
plt.title(f"Density equilibration \n Mean starting at {start:.2E} steps: {np.round(mean, 2)} kg / $m^3$")
plt.xlabel("MC Step")
plt.ylabel("Density kg / m$^3$")
plt.legend(loc="lower right")
plt.show()
