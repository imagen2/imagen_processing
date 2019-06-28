Structural MRI data: preprocessing with FreeSurfer
==================================================

Segmentation of structural MRI data was performed with FreeSurfer 5.3.0.

1. We ran FreeSurfer command ``recon-all -clean -subjid ... -all`` on every subject.
2. We extracted the usual FreeSurfer stats table using shell script ``stats2table.sh``.
3. We extracted Euler's number using shell script ``eno2table.py``.
