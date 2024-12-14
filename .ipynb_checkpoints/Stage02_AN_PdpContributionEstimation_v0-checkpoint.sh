#!/bin/sh
#PJM -L rscgrp=a-batch
#PJM -L node=1
#PJM -L elapse=24:00:00
#PJM -j


# Load your conda setup script (adjust the path as needed).
# Typically: source ~/miniconda3/etc/profile.d/conda.sh
# or for an Anaconda installation: source ~/anaconda3/etc/profile.d/conda.sh
source /home/pj24001881/ku40001335/miniconda3/etc/profile.d/conda.sh

# Activate the rapids environment
conda activate ML

# Run your Python script
jupyter nbconvert --to notebook --execute /home/pj24001881/ku40001335/Greenness_NighttimeLight_WB/PyCode_v241111/Stage02_AN_PdpContributionEstimation_v0.ipynb --output /home/pj24001881/ku40001335/Greenness_NighttimeLight_WB/PyCode_v241111/Stage02_AN_PdpContributionEstimation_v0_Execute.ipynb
