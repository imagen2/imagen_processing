#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


###############################################################################
#           Special xml tags
###############################################################################

XSI = '{http://www.w3.org/2001/XMLSchema-instance}'

XNAT_TAGS_SUBJECT_INFOS = (
    'CANTAB',
    'CHILDHA',
    'CHILDRA',
    'Drugs',
    'Export',
    'Adolescent',
    'FMRI',
    'Series',
    'Guardian',
    'Medications',
    'PARENTRA',
    'PARENTSA',
    'Test'
)

XNAT_TAGS_SKIPPED = (
    'iteration',
    'language',
    'user_code_ident',
    'completed',
    'valid',
    'test_version',
    'trials',
    'imageSession_ID',
    'base_scan_type',
    'subject_ID',
    'ID',
    'project',
    'label',
    'type',
    '%stype' % XSI,
    'xsi:stype',
    'Task_type',
    'ratedate',
    'ratername',
    'relations',
    'age_for_test',
    'processed_age_for_test',
    'resources',
)

###############################################################################
#           Questionnaire xml tags
###############################################################################

XNAT_DAWBA_TAGS_QUESTIONNAIRE = (
    'dawba:clinicalRateData',
    'dawba:clinicalRate_fuData',
    'dawba:computerData',
    'dawba:computer_fuData',
    'dawba:youthData',
    'dawba:youth_fuData',
    'dawba:parent1Data',
    'dawba:parent1_fuData',
)

XNAT_PSYTOOL_TAGS_QUESTIONNAIRE = (
    'psytool:adsr_child_fuData',
    'psytool:audit_childData',
    'psytool:audit_child_fuData',
    'psytool:audit_parentData',
    'psytool:audit_parent_fuData',
    'psytool:audit_interview_fuData',
    'psytool:consent_fuData',
    'psytool:csi_child_fuData',
    'psytool:fbbhks_parent_fuData',
    'psytool:fu_reliabilityData',
    'psytool:fu_reliability_additionalData',
    'psytool:gateway_fu_parentData',
    'psytool:espad_childData',
    'psytool:espad_child_fuData',
    'psytool:espad_parentData',
    'psytool:espad_parent_fuData',
    'psytool:espad_interview_fuData',
    'psytool:ctsData',
    'psytool:iri_child_fuData',
    'psytool:kirbyData',
    'psytool:kirby_fuData',
    'psytool:srs_parent_fuData',
    'psytool:stutt_parent_fuData',
    'psytool:leqData',
    'psytool:leq_fuData',
    'psytool:pbqData',
    'psytool:pdsData',
    'psytool:pds_fuData',
    'psytool:niData',
    'psytool:mast_parentData',
    'psytool:mast_parent_fuData',
    'psytool:neoffi_childData',
    'psytool:neoffi_child_fuData',
    'psytool:neoffi_parentData',
    'psytool:neoffi_parent_fuData',
    'psytool:pegboardData',
    'psytool:surpsData',
    'psytool:surps_fuData',
    'psytool:surps_parentData',
    'psytool:surps_parent_fuData',
    'psytool:tci_childData',
    'psytool:tci_child_fuData',
    'psytool:tci_parentData',
    'psytool:tci_parent_fuData',
    'psytool:tlfbData',
    'psytool:wiscData',
    'psytool:pbq_fuData',
    'psytool:genData',
    'psytool:srcData',
    'psytool:identData',
    'psytool:dotprobeData',
    'psytool:palp_v2Data',
)

XNAT_BEHAVIOURAL_TAGS_QUESTIONNAIRE = (
    'behavioural:cantabTestsData',
)

XNAT_MISC_TAGS_QUESTIONNAIRE = (
    'imagen:imagenSubjectVariablesData',
    'imagen:recruitmentInfosData',
)

XNAT_QR_TAGS_QUESTIONNAIRE = (
    "imagen:qualityReportData",
)

###############################################################################
#           Scan xml tags
###############################################################################

XNAT_RAW_ANATOMICAL_SCAN = (
    ("//xnat:scan[@xsi:type='xnat:mrScanData' and @type='ADNI_MPRAGE']",
     "//xnat:assessor[@xsi:type='imagen:niftiScanData' and @type='ADNI_MPRAGE']"),
    ("//xnat:scan[@xsi:type='xnat:mrScanData' and @type='short_MPRAGE']",
     "//xnat:assessor[@xsi:type='imagen:niftiScanData' and @type='short_MPRAGE']"),
    ("//xnat:scan[@xsi:type='xnat:mrScanData' and @type='FLAIR']",
     "//xnat:assessor[@xsi:type='imagen:niftiScanData' and @type='FLAIR']"),
    ("//xnat:scan[@xsi:type='xnat:mrScanData' and @type='T2']",
     "//xnat:assessor[@xsi:type='imagen:niftiScanData' and @type='T2']"),
#    ("//xnat:scan[@xsi:type='xnat:mrScanData' and @type='B0_Map_Optional']",
#     "//xnat:assessor[@xsi:type='imagen:niftiScanData' and @type='B0_Map_Optional']"),
)

XNAT_RAW_DIFFUSION_SCAN = (
    ("//xnat:scan[@xsi:type='xnat:mrScanData' and @type='DTI']",
     "//xnat:assessor[@xsi:type='imagen:niftiScanData' and @type='DTI']"),
)

XNAT_RAW_FMRI_SCAN = {
    'behavioural:face_taskData': [
        "//xnat:scan[@xsi:type='xnat:mrScanData' and @type='EPI_faces']",
        "//xnat:assessor[@xsi:type='imagen:niftiScanData' and @type='EPI_faces']" 
    ],     
    'behavioural:recognition_taskData': [
        "//xnat:scan[@xsi:type='xnat:mrScanData' and @type='EPI_rest']",
        "//xnat:assessor[@xsi:type='imagen:niftiScanData' and @type='EPI_rest']" 
    ],       
    'behavioural:stop_signal_taskData': [
        "//xnat:scan[@xsi:type='xnat:mrScanData' and @type='EPI_stop_signal']",
        "//xnat:assessor[@xsi:type='imagen:niftiScanData' and @type='EPI_stop_signal']" 
    ],    
    'behavioural:mid_taskData': [
        "//xnat:scan[@xsi:type='xnat:mrScanData' and @type='EPI_short_MID']",
        "//xnat:assessor[@xsi:type='imagen:niftiScanData' and @type='EPI_short_MID']" 
    ],            
    'behavioural:gcaData': [
        "//xnat:scan[@xsi:type='xnat:mrScanData' and @type='EPI_global']",
        "//xnat:assessor[@xsi:type='imagen:niftiScanData' and @type='EPI_global']" 
    ],                 
    'behavioural:rps_taskData': [
        "//xnat:scan[@xsi:type='xnat:mrScanData' and @type='EPI_short_reward']",
        "//xnat:assessor[@xsi:type='imagen:niftiScanData' and @type='EPI_short_reward']" 
    ],            
}

XNAT_SPM_FMRI_SCAN = (
    "//xnat:assessor[@xsi:type='spm:betaData']",
    "//xnat:assessor[@xsi:type='spm:beta_meanData']", 
    "//xnat:assessor[@xsi:type='spm:beta_mean_mvtroiData']", 
    "//xnat:assessor[@xsi:type='spm:conData']", 
    "//xnat:assessor[@xsi:type='spm:con_mvtroiData']", 
    "//xnat:assessor[@xsi:type='spm:essData']", 

    "//xnat:assessor[@xsi:type='spm:mmprageData']",
    "//xnat:assessor[@xsi:type='spm:wmmprageData']",
    "//xnat:assessor[@xsi:type='spm:y_mprageData']",  
    "//xnat:assessor[@xsi:type='spm:mwcData']", 
    "//xnat:assessor[@xsi:type='spm:resmsData']",
    "//xnat:assessor[@xsi:type='spm:meanaData']",

    "//xnat:assessor[@xsi:type='spm:rpvData']", 
    "//xnat:assessor[@xsi:type='spm:spmfData']", 
    "//xnat:assessor[@xsi:type='spm:spmtData']", 

    "//xnat:assessor[@xsi:type='spm:wcData']", 
    "//xnat:assessor[@xsi:type='spm:weaData']", 
    "//xnat:assessor[@xsi:type='spm:cData']",
    "//xnat:assessor[@xsi:type='spm:maskData']",
)

XNAT_SPM_FMRI_SCAN_RESOURCE = {
    "//xnat:assessor[@xsi:type='spm:meana_matData']",
    "//xnat:assessor[@xsi:type='spm:statsintra_mat_Data']",
    "//xnat:assessor[@xsi:type='spm:rpl_aData']", 
    "//xnat:assessor[@xsi:type='spm:rp_txtData']", 
    "//xnat:assessor[@xsi:type='spm:job_statsintraData']", 
}

XNAT_FSL_SCAN = (
    "//xnat:assessor[@xsi:type='fsl:eccData']",
    "//xnat:assessor[@xsi:type='fsl:brainData' and @dc='0']",
    "//xnat:assessor[@xsi:type='fsl:brainData' and @dc='1']",
    "//xnat:assessor[@xsi:type='fsl:dcData']",
    "//xnat:assessor[@xsi:type='fsl:maskData' and @dc='0']",
    "//xnat:assessor[@xsi:type='fsl:maskData' and @dc='1']",
    "//xnat:assessor[@xsi:type='fsl:FAData' and @dc='0']",
    "//xnat:assessor[@xsi:type='fsl:FAData' and @dc='1']",
    "//xnat:assessor[@xsi:type='fsl:LData' and @dc='0']",
    "//xnat:assessor[@xsi:type='fsl:LData' and @dc='1']",
    "//xnat:assessor[@xsi:type='fsl:MDData' and @dc='0']",
    "//xnat:assessor[@xsi:type='fsl:MDData' and @dc='1']",
    "//xnat:assessor[@xsi:type='fsl:MOData' and @dc='0']",
    "//xnat:assessor[@xsi:type='fsl:MOData' and @dc='1']",
    "//xnat:assessor[@xsi:type='fsl:RDData' and @dc='0']",
    "//xnat:assessor[@xsi:type='fsl:RDData' and @dc='1']",
    "//xnat:assessor[@xsi:type='fsl:S0Data' and @dc='0']",
    "//xnat:assessor[@xsi:type='fsl:S0Data' and @dc='1']",
    "//xnat:assessor[@xsi:type='fsl:TFData' and @dc='0']",
    "//xnat:assessor[@xsi:type='fsl:TFData' and @dc='1']",
    "//xnat:assessor[@xsi:type='fsl:VData' and @dc='0' and @number='1']",
    "//xnat:assessor[@xsi:type='fsl:VData' and @dc='1' and @number='1']",
    "//xnat:assessor[@xsi:type='fsl:VData' and @dc='0' and @number='2']",
    "//xnat:assessor[@xsi:type='fsl:VData' and @dc='1' and @number='2']",
    "//xnat:assessor[@xsi:type='fsl:VData' and @dc='0' and @number='3']",
    "//xnat:assessor[@xsi:type='fsl:VData' and @dc='1' and @number='3']",
)

XNAT_FREESURFER_SCAN = (
    ("//xnat:assessor[@xsi:type='imagen:niftiScanData' and @type='ADNI_MPRAGE']",
     "//xnat:assessor[@xsi:type='fs:fsData']"),
)


###############################################################################
#           Misc xml tags
###############################################################################

XNAT_TAGS_SUBJECT_ADDITIONAL_INFOS = (
    'custom:cyclePhaseInfoData',
    'custom:sommeilData',
    'custom:bdnfData',
    'custom:oxyData'
)

XNAT_TAGS_GENERIC_ASSESSMENT_RESOURCES_ONLY = (
    'imagen:rawPackageData'
)

XNAT_TAGS_NEUROIMAGING = (
    'xnat:mrSessionData'
)

XNAT_TAG_GENOMICS_SCORES = (
    'custom:per1_methylationData',
    'custom:oxtrGeneExpressionData',
    'custom:per2Data',
    'custom:per1_no13Data'
)


