import mbuild
import foyer
import mosdef_cassandra as mc
import unyt as u
import numpy as np
import pandas as pd
import subprocess
from io import StringIO

#########################################
# We will conduct the following protocol:
# 0. Setup system 
# 1. NVT at 400 K
# 2. NVT at 151 K
# 3. NpT at 151 K
# 4. GEMC at 151 K
#########################################

##########################
# Step 0. Setup the system
##########################

liq_mols = 350
vap_mols = 150
temperature = 400.0 * u.K
simlength = 10000
boxl = 3.0

# Use mbuild to create a coarse-grained CH4 bead
methane = mbuild.Compound(name="_CH4")

# Create two empty mbuild.Box
# (vapor = larger, liquid = smaller)
liquid_box = mbuild.Box(lengths=[boxl, boxl, boxl])
vapor_box = mbuild.Box(lengths=[4.0, 4.0, 4.0])

# Load force field
trappe = foyer.forcefields.load_TRAPPE_UA()

# Use foyer to apply force field
typed_methane = trappe.apply(methane)

######################
# Step 1. NVT at 400 K
######################

# Define the System
nvt_system = mc.System([liquid_box], [typed_methane], mols_to_add=[[liq_mols]])
# Define the MoveSet
nvt_moveset = mc.MoveSet("nvt", [typed_methane])

# Run a simulation at 300 K for 10000 MC moves
mc.run(
    system=nvt_system,
    moveset=nvt_moveset,
    run_type="equilibration",
    run_length=simlength,
    temperature=temperature,
    charge_style="none",
)

######################
# Step 2. NVT at 171 K
######################

temperature = 171.0 * u.K

cmd = [
    "tail",
    "-n",
    str(liq_mols + 2),
    "nvt.out.xyz",
]

# Save final liquid box xyz file
xyz = subprocess.check_output(cmd).decode("utf-8")

with open("nvt2.initial.xyz", mode="w") as f:
    f.write(xyz)

liquid_box = mbuild.formats.xyz.read_xyz("nvt2.initial.xyz")

liquid_box.box = mbuild.Box(lengths=[boxl, boxl, boxl], angles=[90., 90., 90.])

#liq_box.periodicity = [True, True, True]

box_list = [liquid_box]

species_list = [typed_methane]

mols_in_boxes = [[liq_mols]]

nvt2_system = mc.System(box_list, species_list, mols_in_boxes=mols_in_boxes)

# Run a simulation at 300 K for 10000 MC moves
mc.run(
    system=nvt2_system,
    run_name="nvt2",
    moveset=nvt_moveset,
    run_type="equilibration",
    run_length=simlength,
    temperature=temperature,
    charge_style="none",
)

######################
# Step 2. NVT at 171 K
######################

temperature = 175.0 * u.K
pressure = 2830 * u.kilopascal

cmd = [
    "tail",
    "-n",
    str(liq_mols + 2),
    "nvt2.out.xyz",
]

# Save final liquid box xyz file
xyz = subprocess.check_output(cmd).decode("utf-8")

with open("npt.initial.xyz", mode="w") as f:
    f.write(xyz)

liquid_box = mbuild.formats.xyz.read_xyz("npt.initial.xyz")

liquid_box.box = mbuild.Box(lengths=[boxl, boxl, boxl], angles=[90., 90., 90.])

#liq_box.periodicity = [True, True, True]

box_list = [liquid_box]

species_list = [typed_methane]

mols_in_boxes = [[liq_mols]]

npt_system = mc.System(box_list, species_list, mols_in_boxes=mols_in_boxes)

npt_moveset = mc.MoveSet("npt", species_list)

# Edit the volume move probability to be more reasonable
orig_prob_volume = npt_moveset.prob_volume
new_prob_volume = 1.0 / liq_mols
npt_moveset.prob_volume = new_prob_volume

npt_moveset.prob_translate = (
    npt_moveset.prob_translate + orig_prob_volume - new_prob_volume
)


# Run a simulation at 300 K for 10000 MC moves
mc.run(
    system=npt_system,
    moveset=npt_moveset,
    run_type="equilibration",
    run_length=simlength,
    temperature=temperature,
    pressure=pressure,
    charge_style="none",
)

##################
# 4. GEMC at 175 K
##################

cmd = [
    "tail",
    "-n",
    str(liq_mols + 2),
    "npt.out.xyz",
]

# Save final liquid box xyz file
xyz = subprocess.check_output(cmd).decode("utf-8")
with open("gemc.initial.xyz", "w") as f:
    f.write(xyz)

# Save final box dims
box_data = []
with open("npt.out.H") as f:
    for line in f:
        box_data.append(line.strip().split())

boxl = float(box_data[-6][0]) / 10.0  # nm

liquid_box = mbuild.formats.xyz.read_xyz("gemc.initial.xyz")

liquid_box.box = mbuild.Box(lengths=[boxl, boxl, boxl], angles=[90., 90., 90.])

#liq_box.periodicity = [True, True, True]

specific_volume = u.kb * temperature / pressure
vap_volume = (specific_volume * vap_mols * u.Na.to("1/mol")).to("angstrom**3")
boxl_vap = vap_volume ** (1.0/3.0)

vap_box = mbuild.Box(lengths=[boxl_vap, boxl_vap, boxl_vap], angles=[90., 90., 90.])

box_list = [liquid_box, vap_box]

species_list = [typed_methane]

mols_in_boxes = [[liq_mols], [0]]

mols_to_add = [[0], [vap_mols]]

gemc_system = mc.System(box_list, species_list, mols_in_boxes=mols_in_boxes, mols_to_add=mols_to_add)

# Create a new moves object
gemc_moveset = mc.MoveSet("gemc", species_list)

# Edit the volume and swap move probability to be more reasonable
orig_prob_volume = gemc_moveset.prob_volume
orig_prob_swap = gemc_moveset.prob_swap
new_prob_volume = 1.0 / (vap_mols + liq_mols)
new_prob_swap = 4.0 / 0.05 / (vap_mols + liq_mols)
gemc_moveset.prob_volume = new_prob_volume
gemc_moveset.prob_swap = new_prob_swap

gemc_moveset.prob_translate = (
    gemc_moveset.prob_translate + orig_prob_volume - new_prob_volume
)
gemc_moveset.prob_translate = (
        gemc_moveset.prob_translate + orig_prob_swap - new_prob_swap
    )

# Define thermo output props
thermo_props = [
    "energy_total",
    "pressure",
    "volume",
    "nmols",
    "mass_density",
    "enthalpy",
]

# Define custom args

custom_args = {}
custom_args["properties"] = thermo_props
custom_args["charge_style"] = "none"

# Move into the job dir and start doing things

mc.run(
    system=gemc_system,
    moveset=gemc_moveset,
    run_type="equilibration",
    run_length=simlength,
    temperature=temperature,
    **custom_args
)




## Create box and species list
#box_list = [liquid_box, vapor_box]
#species_list = [typed_methane]
#
#mols_to_add = [[350], [100]]
#
#system = mc.System(box_list, species_list, mols_to_add=mols_to_add)
#moveset = mc.MoveSet("gemc", species_list)
#
#moveset.prob_volume = 0.010
#moveset.prob_swap = 0.11
#
#thermo_props = [
#    "energy_total",
#    "energy_intervdw",
#    "pressure",
#    "volume",
#    "nmols",
#    "mass_density",
#]
#
#custom_args = {
#    "run_name": "equil",
#    "charge_style": "none",
#    "rcut_min": 2.0 * u.angstrom,
#    "vdw_cutoff": 14.0 * u.angstrom,
#    "units": "sweeps",
#    "steps_per_sweep": 450,
#    "coord_freq": 50,
#    "prop_freq": 10,
#    "properties": thermo_props,
#}
#
#mc.run(
#    system=system,
#    moveset=moveset,
#    run_type="equilibration",
#    run_length=250,
#    temperature=151.0 * u.K,
#    **custom_args,
#)
#
## Update run_name and restart_name
#custom_args["run_name"] = "prod"
#custom_args["restart_name"] = "equil"
#
#mc.restart(
#    system=system,
#    moveset=moveset,
#    run_type="production",
#    run_length=750,
#    temperature=151.0 * u.K,
#    **custom_args,
#)