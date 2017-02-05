import nibabel as nib
TH = '/neurospin/imagen/processed/spmstatsintra/000001441076/SessionA/EPI_faces/swea/con_0006.nii.gz'
CAPS = '/neurospin/tmp/frouin/capsul/ft1level/out/BL000001441076/7-SpmImageNiiEncoding/con_0017_angry_-_control.nii.gz'

th = nib.load(TH)
caps = nib.load(CAPS)
d = (caps.get_data() - th.get_data()) / th.get_data()

di = nib.Nifti1Image(d, affine=caps.get_affine(), header=caps.get_header())
nib.save(di, 'difCAPS_TH000001441076.nii.gz')


TH = '/neurospin/imagen/processed/spmstatsintra/000078410552/SessionA/EPI_faces/swea/con_0006.nii.gz'
CAPS = '/neurospin/tmp/frouin/capsul/ft1level/out/BL000078410552/7-SpmImageNiiEncoding/con_0017_angry_-_control.nii.gz'
th = nib.load(TH)
caps = nib.load(CAPS)
d = (caps.get_data() - th.get_data()) / th.get_data()

di = nib.Nifti1Image(d, affine=caps.get_affine(), header=caps.get_header())
nib.save(di, 'difCAPS_TH000078410552.nii.gz')
