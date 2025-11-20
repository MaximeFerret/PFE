import sys
from pathlib import Path
import math
import os
import SimpleITK as sitk
import opengate as gate

# -----------------------
# Récupérer les arguments
# -----------------------
if len(sys.argv) < 4:
    print("Usage: python3 simulate_one_angle.py <case_path> <angle_deg> <part_index>")
    sys.exit(1)

case_path = Path(sys.argv[1])
angle_deg = float(sys.argv[2])
part_index = int(sys.argv[3])

ct_path = case_path / "ct_2mm" / f"{case_path.name}.mhd"
out_dir = case_path
os.makedirs(out_dir, exist_ok=True)

# -----------------------
# Paramètres de simulation
# -----------------------
n_per_angle = int(2e5)
src_radius_mm = 500.0
u = gate.g4_units

# Taille et spacing du CT
img = sitk.ReadImage(str(ct_path))
ct_size = list(img.GetSize())[::-1]
ct_spacing = list(img.GetSpacing())[::-1]

# -----------------------
# Fonction run_angle (une seule instance)
# -----------------------
sim = gate.Simulation()
sim.output_dir = str(out_dir)
sim.world.size = [2*u.m, 2*u.m, 2*u.m]

# Charger le CT
ct = sim.add_volume("ImageVolume", "CT")
ct.image = str(ct_path)
ct.voxel_materials = [
    [-10000, -500, "G4_AIR"],
    [-500, 300, "G4_WATER"],
    [300, 3000, "G4_BONE_COMPACT_ICRU"]
]

# Source
src = sim.add_source("GenericSource", "ct_source")
src.particle = "gamma"
try:
    spec = gate.get_default("spect/CT_120kVp.spectrum")
    src.energy.type = "spectrum"
    src.energy.spectrum_file = spec
except Exception:
    print("Warning: default CT spectrum not found, using mono 60 keV fallback")
    src.energy.mono = 60 * gate.g4_units.keV

# Position de la source
theta = math.radians(angle_deg)
x = src_radius_mm * math.cos(theta)
y = src_radius_mm * math.sin(theta)
z = 0.0

src.position.type = "point"
src.position.translation = [x * u.mm, y * u.mm, z * u.mm]

# Orientation vers le centre
src.direction.type = "focused"
src.direction.point = [0.0, 0.0, 0.0]
src.direction.sigma_angle = 0.0 * u.rad

# Nombre de primaires
src.n = n_per_angle

# Actor dose
dose = sim.add_actor("DoseActor", f"dose_part_{part_index}")
dose.output_filename = f"dose_part_{part_index}.mhd"
dose.write_to_disk = True
dose.size = ct_size
dose.spacing = ct_spacing

print(f"Running angle {angle_deg:.1f}° -> pos ({x:.1f},{y:.1f}) mm, primaries={src.n}")
sim.run()
print(f"Finished angle {angle_deg:.1f}° (part {part_index})")
