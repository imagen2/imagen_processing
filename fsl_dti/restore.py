#!/usr/bin/python

# Using the RESTORE algorithm for robust tensor fitting
# http://nipy.org/dipy/examples_built/restore_dti.html
# 
# 09/17/2015 H. Lemaitre (herve.lemaitre@u-psud.fr).
# Usage: restore.py rawfile dtifile dtibval dtibvec output
#
# rawfile = diffusion weighted image non masked
# dtifile = diffusion weighted masked
# dtibval = bval file
# dtibvec = bvec file
# output  = output name
#

# arguments
import sys
rawfile=str(sys.argv[1])
dtifile=str(sys.argv[2])
dtibval=str(sys.argv[3])
dtibvec=str(sys.argv[4])
output=str(sys.argv[5])

# imports
import numpy as np
import nibabel as nib
import dipy.reconst.dti as dti
import dipy.denoise.noise_estimate as ne
import dipy.io as io
import dipy.core.gradients as cg

# load dti data
raw=nib.load(rawfile)
dataraw=raw.get_data()
img = nib.load(dtifile)
data = img.get_data()

# load bvec and bvals
bvals, bvecs = io.read_bvals_bvecs(dtibval, dtibvec)
gtab = cg.gradient_table(bvals, bvecs)

# noise estimation from the b=0
sigma = ne.estimate_sigma(dataraw[:,:,:,bvals==0])
sigmamean=np.mean(sigma)

# tensor computation using restore
tenmodel=dti.TensorModel(gtab,fit_method='RESTORE', sigma=sigmamean)
tenfit = tenmodel.fit(data)

# Derivated measures
from dipy.reconst.dti import fractional_anisotropy, mean_diffusivity, radial_diffusivity, axial_diffusivity,mode
FA = fractional_anisotropy(tenfit.evals)
MD = mean_diffusivity(tenfit.evals)
AD = axial_diffusivity(tenfit.evals)
RD = radial_diffusivity(tenfit.evals)
MO = mode(tenfit.evecs)

tenfit.evals[np.isnan(tenfit.evals)] = 0
evals1_img = nib.Nifti1Image(tenfit.evals[:,:,:,0].astype(np.float32), img.get_affine())
nib.save(evals1_img, output+'_restore_L1.nii.gz')
evals2_img = nib.Nifti1Image(tenfit.evals[:,:,:,1].astype(np.float32), img.get_affine())
nib.save(evals2_img, output+'_restore_L2.nii.gz')
evals3_img = nib.Nifti1Image(tenfit.evals[:,:,:,2].astype(np.float32), img.get_affine())
nib.save(evals3_img, output+'_restore_L3.nii.gz')

tenfit.evecs[np.isnan(tenfit.evecs)] = 0
evecs_img1 = nib.Nifti1Image(tenfit.evecs[:,:,:,:,0].astype(np.float32), img.get_affine())
nib.save(evecs_img1, output+'_restore_V1.nii.gz')
evecs_img2 = nib.Nifti1Image(tenfit.evecs[:,:,:,:,1].astype(np.float32), img.get_affine())
nib.save(evecs_img2, output+'_restore_V2.nii.gz')
evecs_img3 = nib.Nifti1Image(tenfit.evecs[:,:,:,:,2].astype(np.float32), img.get_affine())
nib.save(evecs_img3, output+'_restore_V3.nii.gz')

FA[np.isnan(FA)] = 0
fa_img = nib.Nifti1Image(FA.astype(np.float32), img.get_affine())
nib.save(fa_img, output+'_restore_FA.nii.gz')

MD[np.isnan(MD)] = 0
md_img = nib.Nifti1Image(MD.astype(np.float32), img.get_affine())
nib.save(md_img, output+'_restore_MD.nii.gz')

RD[np.isnan(RD)] = 0
rd_img = nib.Nifti1Image(RD.astype(np.float32), img.get_affine())
nib.save(rd_img, output+'_restore_RD.nii.gz')

MO[np.isnan(MO)] = 0
mo_img = nib.Nifti1Image(MO.astype(np.float32), img.get_affine())
nib.save(mo_img, output+'_restore_MO.nii.gz')









