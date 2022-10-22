import mbuild
import foyer
import mosdef_cassandra as mc
from mosdef_cassandra.analysis import ThermoProps
import unyt as u
import matplotlib.pyplot as plt

# We'll filter out warnings. This is to improve the
# clarity of this tutorial. Please refrain to do this
# if you are not completely sure what these mean.

from warnings import filterwarnings
filterwarnings('ignore', category=UserWarning)

temperature = 400.0
pressure = 5.39
boxl = 3.0
nmols = 200
simlength = 3000000

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

# Run a simulation with at 400 K with 3E6 MC moves

# Damped shifted force for fast electrostatics

mc.run(
    system=system,
    moveset=moveset,
    charge_style="dsf",
    dsf_damping=0.2,
    run_type="equilibration",
    run_length=simlength,
    temperature=temperature * u.K,
    **custom_args,
)

# Ewald summation

#mc.run(
#    system=system,
#    moveset=moveset,
#    run_type="equilibration",
#    run_length=simlength,
#    temperature=temperature * u.K,
#    **custom_args,
#)
