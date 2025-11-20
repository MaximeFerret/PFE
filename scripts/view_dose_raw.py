import numpy as np
import matplotlib.pyplot as plt
import sys

# --------------------------------------------------
# ARGS
# --------------------------------------------------
raw_path = sys.argv[1]  # e.g. dose_output_edep.raw
mhd_path = raw_path.replace(".raw", ".mhd")

print("➡️ RAW file:", raw_path)
print("➡️ Reading metadata from:", mhd_path)

# --------------------------------------------------
# Parse .mhd header
# --------------------------------------------------
dims = None
dtype = None

with open(mhd_path, "r") as f:
    for line in f:
        if "DimSize" in line:
            dims = list(map(int, line.split("=")[1].split()))
        if "ElementType" in line:
            t = line.split("=")[1].strip()
            if t == "MET_FLOAT":
                dtype = np.float32
            elif t == "MET_DOUBLE":
                dtype = np.float64
            elif t == "MET_SHORT":
                dtype = np.int16
            elif t == "MET_USHORT":
                dtype = np.uint16

print("Dimensions:", dims)
print("Dtype:", dtype)

# --------------------------------------------------
# Load RAW manually
# --------------------------------------------------
arr = np.fromfile(raw_path, dtype=dtype)
arr = arr.reshape(dims[::-1])   # (z, y, x)
print("Loaded array:", arr.shape)

# Normalisation
arr_norm = arr / np.max(arr)

# Middle slices
mid_z = arr_norm[arr_norm.shape[0]//2]
mid_y = arr_norm[:, arr_norm.shape[1]//2]
mid_x = arr_norm[:, :, arr_norm.shape[2]//2]

# --------------------------------------------------
# Plot
# --------------------------------------------------
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

axs[0].imshow(mid_z, cmap="inferno")
axs[0].set_title("Axial")

axs[1].imshow(mid_y, cmap="inferno")
axs[1].set_title("Coronal")

axs[2].imshow(mid_x, cmap="inferno")
axs[2].set_title("Sagittal")

for ax in axs:
    ax.axis("off")

plt.tight_layout()
plt.savefig("dose_preview.png", dpi=600)
print("✔ Image saved: dose_preview.png")
