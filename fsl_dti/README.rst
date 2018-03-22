DTI data: preprocessing with FSL
================================================================

imagen_diffsl v.5 09/04/2015 
H. Lemaitre (herve.lemaitre@u-psud.fr)
P. Frere    (pabezivin@gmail.com)

Preprocess Imagen dti data for:
1. Linear registration with eddy current correction and bvec rotation
2. B0 mapping correction if possible
3. Brain extraction
4. Tensor computation with weighted least squares and RESTORE (optional)
