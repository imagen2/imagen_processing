---
title: "Standard Operating Procedure for NODDI images"
author: "Herve Lemaitre"
date: "2025-03-11"
output:
  html_document:
    keep_md: true
  
---

# 1. NODDI data

The IMAGEN Neurite Orientation Dispersion and Density Imaging (NODDI) MRI images were only obtained at follow-up 3 (20 years-old) on 3 Tesla scanners (Siemens and General Electric). The noddi images were acquired using two Echo Planar imaging sequences with opposite phase encoding directions (66 oblique-axial slices; Multi-band Acceleration Factor = 3; echo time = 99 ms; repetition time = 3500 ms; 128x128 matrix; field of view 256x256 mm; voxel size 2.0 x 2.0 x 2.0 mm):  
- A >> P phase encoding with 4 b-value=0  
- P >> A phase encoding, multi shells with 4 b-value=0, 64 b-value=700 and 128 b-value=2000  

# 2. Preprocessing

## 2.1. Cross-sectional preprocessing

Diffusion  data  preprocessing  was performed using tools provided by the MRtrix3 software package http://mrtrix.org (Tournier et al., 2019), including, for some preprocessing step, scripts interfacing with the external package FSL FMRIB Software Library (FSL) https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/. Diffusion images were denoised (Veraart et al., 2016), corrected for Gibbs ringing artefacts (Kellner et al., 2016), corrected for susceptibility induced distortions using topup (Andersson et al., 2003), corrected for eddy current-induced distortions and subject movements (Andersson and Sotiropoulos, 2016) using outlier replacement (Andersson et al., 2016) and a linear second level model. Then, a B1 field inhomogeneity correction was performed using the N4 algorithm as provided in ANTs (Turtison et al., 2010). 
The diffusion tensor model was fitted using a weighted least-squares estimator (Veraart et al., 2016) before to extract derivative diffusion metrics (FA, MD, AD and RD). Microstructure imaging was also performed using Accelerated Microstructure Imaging via Convex Optimization (AMICO, Daducci et al., 2015) to estimate parameters such as Free Water Fraction (FWE), Neurite Density Index (NDI) and Orientation Dispersion Index (ODI).


## 2.2. DTI integration  

Following methodological recommendations on diffusion tensor image registration (Wang et al., 2017) and on tract-based spatial statistic (Bach et al., 2014), we used a tensor-based registration with DTI-TK http://dti-tk.sourceforge.net/pmwiki/pmwiki.php (Zhang et al., 2006) to align all individuals into a common space. 
The multiple time-point DTI images were processing within an unbiased longitudinal framework using tensor-based registration (Keihaninejad et al., 2013). A first step created a within-subject template based on the multiple time point images per subject. Then a second step created a group-wise atlas based on the within-subject templates. At the end of the registration procedure, each participant’s DTI data were normalized to the MNI standard space using the IIT human brain tensor template (Zhang et al., 2018). 

In this framework, NODDI images underwent registration to the corresponding DTI images through an affine transformation and were then spatially normalized to the MNI standard space using the DTI transformations previously estimated.

## 2.3 TBSS integration 

Voxel-wise statistical inference of the NODDI parameters was carried out using the TBSS procedure (Smith et al., 2006). Each participant’s aligned FA, MD, AD, RD, FWF, NDI and ODI data were projected onto the IMAGEN skeleton to minimize any residual misalignment of tracts.

# 3. Quality controls

QC variables are stored in the spreadsheet ["imagen_noddi_qcreport.csv"](https://github.com/imagen2/imagen_processing/blob/master/tbss_noddi/imagen_noddi_qcreport.csv). diffimg are subjects with diffusion images. qc_cross_global and qc_long_global are the main qc variables for the cross-sectional (3.1) and registration (3.2) QCs. RUE indicates selected, while FALSE signifies non-selected.

## 3.1  Cross-sectional QC

The eddy qc tools (QUAD, SQUAD) were applied at the single subject and study wise level exporting -1- outliers-related, -2- volume to volume motion and -3- signal to noise ratio (SNR) QC metrics. An automatic QC procedure was performed on the number of volumes (qc_vol), the tensor computation (qc_tensor), the size of the brain mask (qc_mask), the average SNR of the b0 volumes (qc_snrb0), and the total % of outlier slices (qc_outlier) using an univariate inter quartile range approach and an multivariate outlier approach (mvoutier R package).

## 3.2  Registration QC

Diffusion images underwent visual quality control procedures in order to discard images with defective spatial normalization (qc_warpvisual). 

# 4. Outputs

## 4.1 Skeleton images

Images of FA, MD, AD, RD, FWF, NDI and ODI  skeleton images are stored under the following format:  
"XXXXXXXXXXXX_noddi_denoised_degibbsed_preprocessed_biascorrected_dtitk_warpedtomni_YY_skeletonised.nii.gz"  
XXXXXXXXXXX: Subject number  
YY: Modality (i.e. fa, tr, ad, rd, fwf, ndi, odi)  

## 4.2 Skeleton derivative measures

Mean FA, MD, AD, RD, FWF, NDI and ODI measures were extracted from the whole skeleton and from the 48 white matter tract labels of the ICBM-DTI-81 white-matter labels atlas (Hua et al., 2008), and stored under the following format:  
"XXXXXXXXXXXX_noddi_denoised_degibbsed_preprocessed_biascorrected_dtitk_warpedtomni_YY_skeletonised.txt"  
XXXXXXXXXXX: Subject number  
YY: Modality (i.e. fa, tr, ad, rd, fwf, ndi, odi)  

## 5. Other databases

For IMAGEN sister databases (e.g. STRATIFY), NODDI images followed the same work flow except they were registered cross-sectionnally to the IMAGEN template and projected to the IMAGEN skeleton.  

## 6. Releases

**2.1** images are within fsl standard space.  

# 7. References

Andersson, J.L.R., Graham, M.S., Zsoldos, E., Sotiropoulos, S.N., 2016. Incorporating outlier detection and replacement into a non-parametric framework for movement and distortion correction of diffusion MR images. Neuroimage 141, 556–572. https://doi.org/10.1016/j.neuroimage.2016.06.058
Andersson, J.L.R., Skare, S., Ashburner, J., 2003. How to correct susceptibility distortions in spin-echo echo-planar images: application to diffusion tensor imaging. Neuroimage 20, 870–888. https://doi.org/10.1016/S1053-8119(03)00336-7
Andersson, J.L.R., Sotiropoulos, S.N., 2016. An integrated approach to correction for off-resonance effects and subject movement in diffusion MR imaging. Neuroimage 125, 1063–1078. https://doi.org/10.1016/j.neuroimage.2015.10.019
Bach, M., Laun, F.B., Leemans, A., Tax, C.M.W., Biessels, G.J., Stieltjes, B., Maier-Hein, K.H., 2014. Methodological considerations on tract-based spatial statistics (TBSS). Neuroimage 100, 358–369. https://doi.org/10.1016/j.neuroimage.2014.06.021
Daducci, A., Canales-Rodríguez, E.J., Zhang, H., Dyrby, T.B., Alexander, D.C., Thiran, J.-P., 2015. Accelerated Microstructure Imaging via Convex Optimization (AMICO) from diffusion MRI data. Neuroimage 105, 32–44. https://doi.org/10.1016/j.neuroimage.2014.10.026
Hua, K., Zhang, J., Wakana, S., Jiang, H., Li, X., Reich, D.S., Calabresi, P.A., Pekar, J.J., van Zijl, P.C.M., Mori, S., 2008. Tract Probability Maps in Stereotaxic Spaces: Analyses of White Matter Anatomy and Tract-Specific Quantification. Neuroimage 39, 336–347. https://doi.org/10.1016/j.neuroimage.2007.07.053
Keihaninejad, S., Zhang, H., Ryan, N.S., Malone, I.B., Modat, M., Cardoso, M.J., Cash, D.M., Fox, N.C., Ourselin, S., 2013. An unbiased longitudinal analysis framework for tracking white matter changes using diffusion tensor imaging with application to Alzheimer’s disease. Neuroimage 72, 153–163. https://doi.org/10.1016/j.neuroimage.2013.01.044
Kellner, E., Dhital, B., Kiselev, V.G., Reisert, M., 2016. Gibbs-ringing artifact removal based on local subvoxel-shifts. Magn Reson Med 76, 1574–1581. https://doi.org/10.1002/mrm.26054
Smith, S.M., Jenkinson, M., Johansen-Berg, H., Rueckert, D., Nichols, T.E., Mackay, C.E., Watkins, K.E., Ciccarelli, O., Cader, M.Z., Matthews, P.M., Behrens, T.E.J., 2006. Tract-based spatial statistics: voxelwise analysis of multi-subject diffusion data. Neuroimage 31, 1487–1505. https://doi.org/10.1016/j.neuroimage.2006.02.024
Tournier, J.-D., Smith, R., Raffelt, D., Tabbara, R., Dhollander, T., Pietsch, M., Christiaens, D., Jeurissen, B., Yeh, C.-H., Connelly, A., 2019. MRtrix3: A fast, flexible and open software framework for medical image processing and visualisation. Neuroimage 202, 116137. https://doi.org/10.1016/j.neuroimage.2019.116137
Tustison, N.J., Avants, B.B., Cook, P.A., Zheng, Y., Egan, A., Yushkevich, P.A., Gee, J.C., 2010. N4ITK: Improved N3 Bias Correction. IEEE Trans Med Imaging 29, 1310–1320. https://doi.org/10.1109/TMI.2010.2046908
Veraart, J., Fieremans, E., Novikov, D.S., 2016. Diffusion MRI noise mapping using random matrix theory. Magn Reson Med 76, 1582–1593. https://doi.org/10.1002/mrm.26059
Veraart, J., Sijbers, J., Sunaert, S., Leemans, A., Jeurissen, B., 2013. Weighted linear least squares estimation of diffusion MRI parameters: strengths, limitations, and pitfalls. Neuroimage 81, 335–346. https://doi.org/10.1016/j.neuroimage.2013.05.028
Wang, Y., Shen, Y., Liu, D., Li, G., Guo, Z., Fan, Y., Niu, Y., 2017. Evaluations of diffusion tensor image registration based on fiber tractography. Biomed Eng Online 16. https://doi.org/10.1186/s12938-016-0299-2
Zhang, H., Yushkevich, P.A., Alexander, D.C., Gee, J.C., 2006. Deformable registration of diffusion tensor MR images with explicit orientation optimization. Med Image Anal 10, 764–785. https://doi.org/10.1016/j.media.2006.06.004
Zhang, S., Arfanakis, K., 2018. Evaluation of standardized and study-specific diffusion tensor imaging templates of the adult human brain: Template characteristics, spatial normalization accuracy, and detection of small inter-group FA differences. Neuroimage 172, 40–50. https://doi.org/10.1016/j.neuroimage.2018.01.046

