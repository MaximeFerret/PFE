# PFE
Compression des réseaux de neurones convolutifs pour les applications en temps réel de la simulation de Monte Carlo en radiothérapie


sudo apt install python3.11 python3.11-venv


python3.11 -m venv gateenv
source gateenv/bin/activate
pip install --upgrade pip
pip install opengate


opengate_info
opengate_tests

python3 ./scripts/simulate_pancreas.py ./data/Pancreas_2mm_v2/PANCREAS_0001/

python3 ./scripts/simulate_ct_batch.py ./data/Pancreas_2mm_v2/PANCREAS_0001/

python3 ./scripts/combine_doses.py ./data/Pancreas_2mm_v2/PANCREAS_0001/ 90
