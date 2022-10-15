#!/usr/bin/env python
# coding: utf-8

# https://github.com/mosdef-hub/mbuild/issues/966
import mbuild
import foyer

import warnings
warnings.filterwarnings("ignore")

ethanol_unparametrized = mbuild.load("CCO", smiles=True)
ethanol_unparametrized.name = "ETO"

box = mbuild.Box(3 * [4.0])

filled_box = mbuild.fill_box(compound=ethanol_unparametrized, n_compounds=200, box=box)

ff = foyer.Forcefield(name="oplsaa")
filled_box_parmed = filled_box.to_parmed(infer_residues=True)
filled_box_parmed_parametrized = ff.apply(filled_box_parmed) #parmed.Structure

mbuild.formats.lammpsdata.write_lammpsdata(
   filled_box_parmed_parametrized, 
   "ethanol.data",
   atom_style="full",
   unit_style="real",
   use_rb_torsions=True,
)
