########################################################################
# Short documentation 
# on onset/contrast generation to build the SPM batch file
########################################################################

# This python script are extracted from the general pipelines in NS


Contents: mid.py and helper mid_generate_onsets.py
          example/mid_000055417875.csv is an actual behavioural file from BL
          

Syntax 
python mid.py --in  mid_000055417875.csv --out contrasts.m


This script generates the onset/contrast part of the batch file (the 
complete batch file job_spmstatsintra_EPImid_000055417875.m that
was used for the base line is given here)

