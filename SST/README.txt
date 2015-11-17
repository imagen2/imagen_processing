# Short documentaion 
# on onset/contrast generation to build the spm batch file
########################################################################

# This python script are extracted from the general pipelines in NS


Content : sst.py and helper (generate_onsets.py)
          ss_000055417875.csv is an actual behavioural file from BL
          

Syntax 
python sst.py --in  ss_000055417875.csv --out contrasts.m


This script generates the onset/contrast part of the batch file (the 
complete batch file job_spmstatsintra_EPIstopsignal_000055417875.m that
was used for the base line is given here)


the first 73 lines are common between constrasts.m and job_XXX.m. Indeed, the rest of the script models other variableslike movment and so on...

