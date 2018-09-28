=======
DTI data: preprocessing with FSL
=======
-----------------
Goal:
-----------------
The imagen_diffsl script preprocesses all dti data from the eight IMAGEN centers (http://www.imagen-europe.com). 

-----------------
Configuration:
-----------------

Imagen_diffsl needs FSL>=5.09 to be installed on your system and properly set up (http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation).
If the option RESTORE is set to yes, you need the restore.py script, and python>=2.7 and dipy>=0.8 installed.

-----------------
Preprocessing steps:
-----------------
The pipeline consists in the following steps:

1. Linear registration with eddy current correction and bvec rotation using the first volume of the dti data as reference.
2. B0 mapping correction if possible using magnitude and phase images from the fieldmap acquisition. The correction direction is defined automatically (default is y).
3. Brain extraction
4. Tensor computation with weighted least squares and RESTORE (optional, http://www.ncbi.nlm.nih.gov/pubmed/15844157).

The script takes into account the own characteristics of each imaging center considering the scanner type, the diffusion-weigthed and the B0 fieldmap sequences.

-----------------
Inputs:
-----------------
The general use is:

imagen_diffsl <mag> <phase> <dti> <center> <restore> <pdir>

* mag, the raw magnitude image from the fieldmap.
* phase, the raw phase image from the fieldmap.
* dti,the 4D image including the diffusion weighted images.
* center, the center id between 1 and 8.
* restore=yes or no for the optional RESTORE
* pdir, output directory for preprocessed data

All images must be in ANALYZE, NIFTI or NIFTI.GZ.

For centers concatenating fieldmaps (magnitude and phase images in a 4D image) like Nottingham and Dublin, you may replace the magnitude with NA and the phase with the 4D image:
imagen_diffsl	NA	000038429243s601a1006	000038429243s901a1009 2 yes /tmp/

For Berlin with three dti sets and without fieldmap from the GE scanner, you need to specify only the three dti images (no correction distortion is applied):
Imagen_diffsl	000021053574s006a1001	000021053574s007a1001	000021053574s008a1001	4 yes /tmp/


For Berlin with one dti set and with fieldmaps from the Siemens scanner, you need to specify 41 instead of 4 for the center id:
imagen_diffsl	000014178831s006a1001	000014178831s007a2001	0000014178831s016a1001	41 yes /tmp/

-----------------
Outputs:
-----------------

The script creates one folder per subject with inside:

======================================= =======================================================================================
file            Description
======================================= =======================================================================================
subject_mag                             the raw magnitude image
subject_phase 	                        the raw phase image
subject_phase_w	                        the wrapped phase ima
subject_phase_uw			                  the unwrapped phase image
subject_phase_rads			                the rad/sec phase image
subject_dti_ecc.unwarp/		              folder for the distortion correction
subject_dti			                        the raw dti data
subject_dti.bval			                  the b values
subject_dti.bvec			                  the gradient directions
subject_dti_ecc			                    the eddy current corrected dti data
subject_dti_ecc.bvec		                the bvec table corrected for rotation
subject_dti_ecc_mask		                the brain mask after eddy current correction
subject_dti_ecc_brain		                the brain extracted and eddy current corrected dti data
subject_dti_ecc_brain_*                 the diffusion measures from the tensor estimation with wls
subject_dti_ecc_brain_restore_*         and RESTORE
subject_dti_ecc_dc			                the eddy current and distortion corrected dti data
subject_dti_ecc_dc_mask		              the mask after eddy current and distortion correction
subject_dti_ecc_dc_brain		            the brain extracted and distortion corrected dti data
subject_dti_ecc_dc_brain_*		          the diffusion measures from the tensor estimation after distortion correction with wls
subject_dti_ecc_dc_brain_restore*       and RESTORE
subject_dtit.slices				              mean value per axial slices and diffusion-weighted volumes
subject_dti_ecc.log				              transformation matrix during the affine registration
subject_dti_ecc.rotation			          total angle rotation in radians and flag for 2 and 5 degrees
subject_dti_ecc_dc.log			            cost values after distortion correction (smaller is better)
subject_dti_ecc_brain_tf.log			      summary of the wls tensor fitting after eddy current correction
subject_dti_ecc_brain_restore_tf.log    summary of the restore tensor fitting after eddy current correction
subject_dti_ecc_dc_brain_tf.log		      summary of the wls tensor fitting after distortion correction
subject_dti_ecc_dc_brain_restore_tf.log summary of the restore tensor fitting after distortion correction
======================================= =======================================================================================

*: _V1 - 1st eigenvector; _V2 - 2nd eigenvector; _V3 - 3rd eigenvector; _L1 - 1st eigenvalue; _L2 - 2nd eigenvalue; _L3 - 3rd eigenvalue; _RD – radial diffusivity
_MD - mean diffusivity; _FA - fractional anisotropy; _MO - mode of the anisotropy (oblate ~ -1; isotropic ~ 0; prolate ~ 1); _S0 - raw T2 signal with no diffusion weighting

-----------------
Automatic QC:
-----------------
Several automatic QC steps can be performed on these output files:

1. Volumes and slices

QCing the number of volumes and slices.

* File: subject_dtit.slices
* Flag: if # of volumes != 36 or # of slices != 60

2. Slice-dropout

QCing slice by slice for divergent values indicating a signal dropout.

* File: subject_dtit.slices
* Flag: if # > 1

3. Head motion

QCing volume by volume for head rotation based on the matrix used for the spatial registration.

* File: subject_dti_ecc.rotation
* Flag: if # > 1

4. B0 mapping correction

QCing the distortion correction by looking at the cost measure of the spatial registration before and after correction.

* Files: subject_dti_ecc_dc.log
* Flag: if the cost measure is bigger after correction than without correction 

5. Tensor computation

QCing the tensor computation by using a k-means clustering on the global FA, MD, L1, L2, L3 and MO values.

* Files: subject_dti_ecc_brain_tf.log
* Flag: if not in the two main clusters.

-----------------
Data availability:
-----------------
The preprocessed data can be found in the Imagen database (https://imagen2.cea.fr) under “Processed Data”.

-----------------
Contact:
-----------------
Herve Lemaitre (herve.lemaitre@u-psud.fr).

