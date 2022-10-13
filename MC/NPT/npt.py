import mbuild
import foyer
import mosdef_cassandra as mc
from mosdef_cassandra.analysis import ThermoProps
import unyt as u
import matplotlib.pyplot as plt

temperature = 300.0
pressure = 1.0
boxl = 3.0
nmols = 50
simlength = 100000

# Use mbuild to create molecules
ethanol = mbuild.load("ethanol.mol2")

# Create an empty mbuild.Box
box = mbuild.Box(lengths=[boxl, boxl, boxl])

# Load force field
trappe = foyer.Forcefield(name="trappe-ua")

# Use foyer to apply force field
ethanol = trappe.apply(ethanol)

# Create box and species list
box_list = [box]
species_list = [ethanol]

# Use Cassandra to insert some initial number of species
mols_to_add = [[nmols]]

# Define the System
system = mc.System(box_list, species_list, mols_to_add=mols_to_add)
# Define the MoveSet
moveset = mc.MoveSet("npt", species_list)

# Here we must specify the pressure since we are performing a
# NpT simulation. It can be provided in the custom_args dictionary
# or as a keyword argument to the "run" function.
custom_args = {
    "pressure": pressure * u.bar,
}

# Run a simulation with at 300 K with 10000 MC moves
mc.run(
    system=system,
    moveset=moveset,
    run_type="equilibration",
    run_length=simlength,
    temperature=temperature * u.K,
    **custom_args,
)

thermo = ThermoProps(f"npt.out.prp")
density = thermo.prop("Mass_Density")
steps = thermo.prop("MC_STEP")
plt.plot(steps, density, label="Density")
plt.title("NPT TraPPE-UA Ethanol @ 300 K")
plt.xlabel("MC STEPS")
plt.ylabel("Density (kg/m$^3$)")
plt.show()
