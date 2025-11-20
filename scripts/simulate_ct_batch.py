import subprocess
import sys
from pathlib import Path
import numpy as np

# -----------------------
# Config utilisateur
# -----------------------
if len(sys.argv) < 2:
    print("Usage: python3 simulate_ct_batch.py <case_path>")
    sys.exit(1)

case_path = Path(sys.argv[1])
n_angles = 90  # nombre de positions sur 360°

# Vérifie que le script pour un angle existe
simulate_one_angle_script = Path(__file__).parent / "simulate_one_angle.py"
if not simulate_one_angle_script.exists():
    print(f"Erreur : {simulate_one_angle_script} n'existe pas !")
    sys.exit(1)

angles = np.linspace(0, 360, n_angles, endpoint=False)

# -----------------------
# Lancer chaque angle dans un subprocess
# -----------------------
for i, a in enumerate(angles):
    print(f"Launching angle {a:.1f}° (part {i})")
    result = subprocess.run([
        "python3",
        str(simulate_one_angle_script),
        str(case_path),
        str(a),
        str(i)
    ])
    if result.returncode != 0:
        print(f"Erreur lors de l'exécution de l'angle {a:.1f}°")
        sys.exit(1)

print("Toutes les simulations par angles sont terminées.")
