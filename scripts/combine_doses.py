import sys
from pathlib import Path
import SimpleITK as sitk
import numpy as np
import os

# -----------------------
# Config utilisateur
# -----------------------
if len(sys.argv) < 2:
    print("Usage: python3 combine_doses.py <case_path> [n_angles]")
    sys.exit(1)

case_path = Path(sys.argv[1])
out_dir = case_path

# Nombre d’angles utilisés pour générer les doses partielles
n_angles = int(sys.argv[2]) if len(sys.argv) > 2 else 90

# -----------------------
# Lire la première dose pour référence
# -----------------------
first_file = out_dir / "dose_part_0_edep.mhd"
if not first_file.exists():
    print(f"Erreur : {first_file} n’existe pas !")
    sys.exit(1)

ref_img = sitk.ReadImage(str(first_file))
ct_spacing = ref_img.GetSpacing()
ct_size = ref_img.GetSize()

acc = sitk.GetArrayFromImage(ref_img).astype(np.float64)  # z,y,x

# -----------------------
# Additionner toutes les doses partielles
# -----------------------
for i in range(1, n_angles):
    dose_file = out_dir / f"dose_part_{i}_edep.mhd"
    if not dose_file.exists():
        print(f"Warning: {dose_file} manquant, skipping")
        continue

    img_i = sitk.ReadImage(str(dose_file))
    arr_i = sitk.GetArrayFromImage(img_i).astype(np.float64)
    acc += arr_i

    # Optionnel : supprimer les fichiers partiels pour économiser de l’espace
    # os.remove(str(dose_file))
    # os.remove(str(dose_file).replace(".mhd", ".raw"))

# -----------------------
# Écrire le résultat combiné
# -----------------------
combined = sitk.GetImageFromArray(acc.astype(np.float32))
# SimpleITK attend (x,y,z)
combined.SetSpacing((ct_spacing[2], ct_spacing[1], ct_spacing[0]))

# Copier l’origine du CT
ct_file = case_path / "ct_2mm" / f"{case_path.name}.mhd"
ct_sitk = sitk.ReadImage(str(ct_file))
combined.SetOrigin(ct_sitk.GetOrigin())

out_total = out_dir / "dose_total_CT.mhd"
sitk.WriteImage(combined, str(out_total))
print(f"Saved combined dose: {out_total}")
