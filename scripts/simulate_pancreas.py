import opengate as gate
from pathlib import Path
import sys
import SimpleITK as sitk

# --------------------------------------------------
# Input argument
# --------------------------------------------------
case_path = Path(sys.argv[1])
ct_path = case_path / "ct_2mm" / f"{case_path.name}.mhd"

print(f"➡️ Running MC on: {case_path}")

# Units
u = gate.g4_units

# --------------------------------------------------
# Read CT metadata using SimpleITK (compatible everywhere)
# --------------------------------------------------
img = sitk.ReadImage(str(ct_path))
ct_size = list(img.GetSize())[::-1]        # SITK gives (x,y,z) but Gate wants (z,y,x)
ct_spacing = list(img.GetSpacing())[::-1]  # same

print(f"   Loaded CT {ct_path}")
print(f"   Size: {ct_size}, Spacing: {ct_spacing}")

# --------------------------------------------------
# Simulation
# --------------------------------------------------
sim = gate.Simulation()

# World
sim.world.size = [1 * u.m, 1 * u.m, 1 * u.m]

# --------------------------------------------------
# Load CT inside Gate
# --------------------------------------------------
ct = sim.add_volume("ImageVolume", "CT")
ct.image = str(ct_path)
ct.voxel_materials = [
    [-10000, -500, "G4_AIR"],
    [-500, 300, "G4_WATER"],
    [300, 3000, "G4_BONE_COMPACT_ICRU"]
]

# --------------------------------------------------
# Photon source (6 MeV)
# --------------------------------------------------
src = sim.add_source("GenericSource", "photon_source")
src.particle = "gamma"
src.energy.mono = 6 * u.MeV
src.position.type = "point"
src.position.translation = [0, 0, -200 * u.mm]
src.direction.type = "momentum"
src.direction.momentum = [0, 0, 1]   # tire vers le haut
src.n = 1e5    # sinon Gate simulera 0 particules !

# --------------------------------------------------
# Dose Actor
# --------------------------------------------------
sim.output_dir = str(case_path)   # dossier où les sorties seront écrites

dose = sim.add_actor("DoseActor", "dose")
dose.output_filename = "dose_output.mhd"   # nom du fichier dans output_dir
dose.write_to_disk = True                 # obligatoire
dose.size = ct_size
dose.spacing = ct_spacing


# --------------------------------------------------
# Run
# --------------------------------------------------
sim.run()

print(f"✔️ Simulation done for {case_path.name}")
