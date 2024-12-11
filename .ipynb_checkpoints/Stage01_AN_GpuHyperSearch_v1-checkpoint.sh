#!/bin/sh
#PJM -L rscgrp=b-batch
#PJM -L rscgrp=b-batch
#PJM -L gpu=1
#PJM -j
#PJM -N my_rapids_job
#PJM -o my_rapids_job.out
#PJM -e my_rapids_job.err

# Load your conda setup script (adjust the path as needed).
# Typically: source ~/miniconda3/etc/profile.d/conda.sh
# or for an Anaconda installation: source ~/anaconda3/etc/profile.d/conda.sh
source /home/pj24001881/ku40001335/miniconda3/etc/profile.d/conda.sh

# Activate the rapids environment
conda activate rapids-24.10

# Run your Python script
python3 /home/pj24001881/ku40001335/Greenness_NighttimeLight_WB/PyCode_v241111/Stage01_AN_GpuHyperSearch_v1.py
