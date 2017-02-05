########################################################################
# Short documentation 
# on onset/contrast generation to build the spm batch file
########################################################################

# These Python scripts are extracted from the general pipelines in NeuroSpin


Contents: sst.py and helper sst_generate_onsets.py
          example/ss_000055417875.csv is an actual behavioural file from BL
          

Syntax:
python sst.py --in ss_000055417875.csv --out contrasts.m


This script generates the onset/contrast part of the batch file (the 
complete batch file job_spmstatsintra_EPIstopsignal_000055417875.m that
was used for the base line is given here)

The first 73 lines are common between constrasts.m and job_XXX.m.
Indeed, the rest of the script models other variables like movement and so on.

