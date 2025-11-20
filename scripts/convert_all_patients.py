import os
from ct_to_gate import convert_ct_to_gate

root = "./data/Pancreas_2mm_v2"
destination = "./gate_input/"
hu_file = "./gate_config/huToMaterial.xml"

if __name__ == "__main__":
    for i in range(1, 83):
        if i in [25, 70]:
            continue
        
        folder = f"PANCREAS_{i:04d}"
        input_mhd = f"{root}/{folder}/ct_2mm/{folder}.mhd"
        
        if not os.path.exists(input_mhd):
            print("❌ Introuvable", input_mhd)
            continue
        
        output_dir = f"{destination}/{folder}"
        convert_ct_to_gate(input_mhd, output_dir, hu_file)