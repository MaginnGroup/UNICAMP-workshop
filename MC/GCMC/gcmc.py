import mbuild
import foyer
import mosdef_cassandra as mc
import unyt as u
import numpy as np
import matplotlib.pyplot as plt
from mosdef_cassandra.analysis import ThermoProps

from warnings import filterwarnings
filterwarnings('ignore', category=UserWarning)

chemical_potential = -27.64 * (u.kJ / u.mol)

n_unitcells = 12

lattice = mbuild.lattice.load_cif("MFI_SI.cif")

compound_dict = {
    "Si4+": mbuild.Compound(name="Si"),
    "O2-": mbuild.Compound(name="O"),
}

mfi = lattice.populate(compound_dict, 2, 2, 3)

#Create a coarse-grained methane
methane = mbuild.Compound(name="_CH4")

# Load forcefields
trappe_zeo = foyer.Forcefield("trappe_zeo.xml")
trappe = foyer.forcefields.load_TRAPPE_UA()

# Use foyer to apply forcefields
mfi_ff = trappe_zeo.apply(mfi)
methane_ff = trappe.apply(methane)

# Create box and species list
box_list = [mfi]
species_list = [mfi_ff, methane_ff]

# Since we have an occupied box we need to specify
# the number of each species present in the intial config
mols_in_boxes = [[1, 0]]

system = mc.System(box_list, species_list, mols_in_boxes=mols_in_boxes)
moveset = mc.MoveSet("gcmc", species_list)

default_args = {
    "chemical_potentials": ["none", chemical_potential],
    "rcut_min": 0.5 * u.angstrom,
    "vdw_cutoff": 14.0 * u.angstrom,
    "charge_cutoff": 14.0 * u.angstrom,
    "coord_freq": 1000,
    "prop_freq": 1000,
}

# Combine default/custom args and override default
mc.run(
    system=system,
    moveset=moveset,
    run_type="equilibration",
    run_length=100000,
    temperature=308.0 * u.K,
    **default_args,
)

loading = []
thermo = ThermoProps("./gcmc.out.prp")
plt.plot(thermo.prop("MC_STEP"), thermo.prop("Nmols_2") / n_unitcells, label="Simulations")
nmols_uc = thermo.prop("Nmols_2", start=30000) / n_unitcells
plt.axhline(y=np.mean(nmols_uc), color='r', linestyle='-', label='Mean')
plt.title(f"GCMC TraPPE Methane @ $\mu$ = {chemical_potential}, \n Mean = {np.round(np.mean(nmols_uc).value, 2)} molecules")
plt.xlabel("MC Step")
plt.ylabel("Molecules / uc")
plt.legend(loc=4)
plt.show()
