import nibabel as nib
import numpy


TH = '/neurospin/imagen/processed/spmstatsintra/000012029891/SessionA/EPI_faces/swea/con_0001.nii.gz'
# 'angry 1'
CAPS = '/volatile/rc244162/capsul/ft1level/out/BL000012029891/6-EstimateContrast/con_0001.hdr'

th = nib.load(TH)
caps = nib.load(CAPS)
a1 = caps.get_data()
a2 = th.get_data()
a1[numpy.isnan(a1)] = 0
a2[numpy.isnan(a2)] = 0
print numpy.abs(a1).max()
print numpy.abs(a2).max()
d = numpy.abs((a1 - a2))
print d.min()
print d.max()

di = nib.Nifti1Image(d, affine=caps.get_affine(), header=caps.get_header())
nib.save(di, '/volatile/rc244162/diff.nii.gz')



# TH='/neurospin/imagen/processed/spmstatsintra/000078410552/SessionA/EPI_faces/swea/con_0006.nii.gz'
# CAPS='/neurospin/tmp/frouin/capsul/ft1level/out/BL000078410552/7-SpmImageNiiEncoding/con_0017_angry_-_control.nii.gz'
# th = nib.load(TH)
# caps = nib.load(CAPS)
# d = (caps.get_data() - th.get_data())/th.get_data()
#
# di = nib.Nifti1Image(d, affine=caps.get_affine(), header=caps.get_header())
# nib.save(di,'difCAPS_TH000078410552.nii.gz')
