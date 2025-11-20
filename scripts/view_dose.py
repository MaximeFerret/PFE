import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np
import sys

# --------------------------------------------------
# Load dose
# --------------------------------------------------
dose_path = sys.argv[1]  # e.g. data/PANCREAS/PANCREAS_0001/dose_output.mhd
print("➡️ Loading:", dose_path)

dose = sitk.ReadImage(dose_path)
dose_np = sitk.GetArrayFromImage(dose)  # z, y, x
print("Dose shape:", dose_np.shape)

# normalisation simple (optionnelle)
dose_norm = dose_np / np.max(dose_np)

# extract slices
mid_z = dose_norm[dose_norm.shape[0] // 2, :, :]
mid_y = dose_norm[:, dose_norm.shape[1] // 2, :]
mid_x = dose_norm[:, :, dose_norm.shape[2] // 2]

# --------------------------------------------------
# Plot
# --------------------------------------------------
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

axs[0].imshow(mid_z, cmap="inferno")
axs[0].set_title("Axial slice")

axs[1].imshow(mid_y, cmap="inferno")
axs[1].set_title("Coronal slice")

axs[2].imshow(mid_x, cmap="inferno")
axs[2].set_title("Sagittal slice")

for ax in axs:
    ax.axis("off")

plt.tight_layout()
plt.show()
