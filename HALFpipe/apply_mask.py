#!/usr/bin/env python

import sys

import nibabel as nib
import numpy as np
from nilearn.image import new_img_like

a = sys.argv[1]
b = sys.argv[2]
c = sys.argv[3]

image = nib.nifti1.load(a)

seg_image = nib.nifti1.load(b)
seg = np.asanyarray(seg_image.dataobj)
seg[seg == 24] = 0

data = np.asanyarray(image.dataobj)
data[seg == 0] = 0

image = new_img_like(image, data, affine=image.affine, copy_header=True)
nib.save(image, c)
