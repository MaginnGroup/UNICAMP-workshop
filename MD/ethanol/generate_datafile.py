#!/usr/bin/env python

##############################################################
# This script uses MoSDeF to construct a LAMMPS datafile
# of 200 ethanol molecules in a 4x4x4 nm box using the OPLS-AA
# force field. To run, simply type
# > python generate_datafile.py
##############################################################

# Load in mbuild and foyer tools from MoSDeF
import mbuild
import foyer

# Suppress warnings - we know everything here is OK but
# in general you don't want to do this if you are doing
# new things
import warnings
warnings.filterwarnings("ignore")

# Tell mbuild to make an ethanol molecule using SMILES
ethanol_unparametrized = mbuild.load("CCO", smiles=True)

# Name this so that the atom naming works for LAMMPS
ethanol_unparametrized.name = "ETO"

# Define the simulation box as a x,y,z cube 4 nm on a side
box = mbuild.Box(3 * [4.0])

# Fill the box using mbuild with 200 unparameterized ethanol molecules
filled_box = mbuild.fill_box(compound=ethanol_unparametrized, n_compounds=200, box=box)

# Load the OPLS-AA force field parameters to ff using foyer
ff = foyer.Forcefield(name="oplsaa")

# Convert a mbuild compound into a parmed structure
filled_box_parmed = filled_box.to_parmed(infer_residues=True)

# Assign OPLS-AA force field to the unparameterized system
filled_box_parmed_parametrized = ff.apply(filled_box_parmed) #parmed.Structure

# Write the LAMMPS data file using real units
mbuild.formats.lammpsdata.write_lammpsdata(
   filled_box_parmed_parametrized, 
   "ethanol.data",
   atom_style="full",
   unit_style="real",
   use_rb_torsions=True,
)
