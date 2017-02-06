Resting-state fMRI data: preprocessing with FSL, ANTS, ArtRepair
================================================================

Preprocessing of resting-state data was performed with routines from FMRIB’s
Software Library (FSL v5.0.9) and Advanced Normalization Tools (ANTs v1.9.2).

1. Motion correction was carried out, applying a rigid body registration of
   each volume to the middle volume (FSL MCFLIRT).
2. Non-brain tissue was removed (FSL BET).
3. [Optional: Spatial smoothing was applied using a 4mm FWHM Gaussian kernel].
4. Independent component analysis (FSL MELODIC) was run for each data set.
   Artifact components were identified using an automatic classification
   algorithm, and subsequently regressed from the data (ICA-AROMA v0.3;
   Pruim et al., 2015).
5. The resulting cleaned data set was detrended (up to a third degree
   polynomial).
6. Coregistration to a high-resolution T1 image (FSL FLIRT using the BBR
   algorithm), and normalization to 2mm isotropic MNI standard space (ANTs)
   was carried out.
7. Lastly, preprocessed and normalized resting-state data sets were resliced
   to 3mm isotropic voxels.
