import mbuild
import foyer
import mosdef_cassandra as mc
import unyt as u
import numpy as np
import os
from mosdef_cassandra.utils.tempdir import temporary_cd
from mosdef_cassandra.analysis import ThermoProps
import matplotlib.pyplot as plt
from scipy.stats import linregress

temperature = 308.0 * u.K

methane = mbuild.Compound(name='_CH4')

# Load force field
trappe = foyer.forcefields.load_TRAPPE_UA()

# Use foyer to apply force field
methane_typed = trappe.apply(methane)

custom_args = {
    "charge_style" : "none",
    "vdw_cutoff" : 14.0 * u.angstrom,
    "prop_freq" : 10,
}


mus_adsorbate = np.arange(-46, -25, 3) * u.kJ/u.mol

for mu_adsorbate in mus_adsorbate:
    dirname = f'pure_mu_{mu_adsorbate:.1f}'.replace(" ", "_").replace("/", "-")
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    else:
        pass
    with temporary_cd(dirname):
        species_list = [methane_typed]
        if mu_adsorbate < -34:
            boxl = 20. # nm
        else:
            boxl = 5. # nm
        box_list = [mbuild.Box([boxl,boxl,boxl])]
        system = mc.System(box_list, species_list)
        moveset = mc.MoveSet('gcmc', species_list)

        mc.run(
            system=system,
            moveset=moveset,
            run_type="equil",
            run_length=100000,
            temperature=temperature,
            chemical_potentials = [mu_adsorbate],
            **custom_args
        )

pressures = []
for mu_adsorbate in mus_adsorbate:
    dirname = f'pure_mu_{mu_adsorbate:.1f}'.replace(" ", "_").replace("/", "-")
    thermo = ThermoProps(dirname + "/gcmc.out.prp")
    pressures.append(np.mean(thermo.prop("Pressure", start=30000)))
    plt.plot(thermo.prop("MC_STEP"), thermo.prop("Pressure").to("MPa"))
plt.title("Pressure equilibration")
plt.xlabel("MC Step")
plt.ylabel("Pressure (MPa)")
plt.show()

plt.title("Pressure equilibration")
plt.xlabel("MC Step")
plt.ylabel("Pressure (MPa)")
plt.plot(mus_adsorbate, pressures, 'go-')
plt.xlabel("Chemical potential (kJ/mol)")
plt.ylabel("Pressure [bar]")
plt.yscale('log')
slope, intercept, r_value, p_value, stderr = linregress(np.log(pressures).flatten(),y=mus_adsorbate.flatten())
plt.show()

pressures = [
    6000   ,
    22100  ,
    49180  ,
    121800 ,
    316800 ,
    839700 ,
    2243000,
    6000000
] * u.Pa

mus = (slope * np.log(pressures.in_units(u.bar)) + intercept) * u.kJ/u.mol
for (mu, pressure) in zip(mus, pressures):
    print(f"We will run at mu = {mu:0.2f} to simulate {pressure:0.0f}")
