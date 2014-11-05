#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


# System import
import os
import logging
import csv
import numpy
import copy

# Imagen import
from imagen_xnat_parser import _md5_sum

# Exclusion list
exclude_patients = [
    "000036043675", "000053120454", "000028264513", "000067052967",
    "000094998851", "000005432841", "000052774607", "000038072766",
    "000072545430", "000040623634", "000069366941"]

# Center maping
center_map = {
    "LONDON": 1,
    "NOTTINGHAM": 2,
    "DUBLIN": 3,
    "BERLIN": 4,
    "HAMBURG": 5,
    "MANNHEIM": 6,
    "PARIS": 7,
    "DRESDEN": 8
}

# Dawba maping
dawba_map = {
    "clinicalrate": [
        "dcany", "dcemot", "dcsepa", "dcspph", "dcsoph", "dcpanic", "dcagor",
        "dcptsd", "dcocd", "dcgena", "dcotanx", "dcmadep", "dcotdep",
        "dcundif", "dcmania", "dcanyso", "dcmutis", "dcdisat", "dcinhat",
        "dcothat", "dcanyhk", "dcadhdc", "dcadhdi", "dcadhdh", "dcadhdo",
        "dcanycd", "dcodd", "dccd", "dcothcd", "dcother", "dcpdd", "dctic",
        "dceat", "dcpsych", "dcstere", "dcototh", "icany", "icemot", "icsepa",
        "icspph", "icsoph", "icpanic", "icagor", "icptsd", "icocd", "icgena",
        "icotanx", "icmadep", "icotdep", "icundif", "icmania", "icanyso",
        "icmutis", "icdisat", "icreact", "icothat", "icanyhk", "ichyper",
        "icothk", "icanycd", "icodd", "iccdfam", "icunsoc", "icsoccd",
        "icothcd", "icother", "icpdd", "ictic", "iceat", "icpsych",
        "icstere", "icototh"
    ],
}


# Paradigm maping
paradigm_map = {
    "mid": ["mid", "short"],
    "rest": ["rest", "resting"],
    "ss": ["sst", "ss", "stop"],
    "ft": ["faces", "ft", "face"]
}


###############################################################################
#   Psytools parser
###############################################################################

def build_psytools(psytools_root, timepoint="FU2"):
    """ Method to construct the psytools questionnaire (questionnaire - 
    questionnaire run - question).

    Files specific to the processed time point are identified by the
    'timepoint' string in their name.

    Parameters
    ----------
    psytools_root: str (mandatory)
        the path to the psytools files
    timepoint: str (optional)
        the imagen project timepoint identifier

    Returns
    -------
    psytools: dict of list of dict
        the first dictionnaries contains the psc2 as keys and then
        a list of dictionaries with six keys (Questionnaire - QuestionnaireRun -
        Question - OpenAnswer - ExternalResource - Assessment) that
        contains the entity parameter decriptions
    """
    # Get all the processing timepoint psytools file
    psy_files = [os.path.join(psytools_root, x)
                 for x in os.listdir(psytools_root)
                 if (os.path.isfile(os.path.join(psytools_root, x)) and 
                     timepoint in x and x.endswith(".csv"))]
    
    # Go through all psytools questionnaire files
    psytools = {}
    for csv_file in psy_files:

        # Parse questionnaire in csv file
        questionnaires = build_questionnaire(csv_file, timepoint, 
                            patient_id_field="User code",
                            question_field="Trial",
                            answer_field="Trial result",
                            language_field="Language",
                            valid_field="Valid",
                            complete_field="Completed",
                            iteration_field="Iteration")
        for key, value in questionnaires.iteritems():
            if key not in psytools:
                psytools[key] = []
            psytools[key].extend(value)

    return psytools


###############################################################################
#   Dawba parser
###############################################################################

def build_dawba(dawba_root, timepoint="FU2"):
    """ Method to construct the dawba questionnaire (questionnaire - 
    questionnaire run - question).

    Files specific to the processed time point are identified by the
    'timepoint' string in their name.

    Parameters
    ----------
    dawba_root: str (mandatory)
        the path to the psytools files
    timepoint: str (optional)
        the imagen project timepoint identifier

    Returns
    -------
    dawba: dict of list of dict
        the first dictionnaries contains the psc2 as keys and then
        a list of dictionaries with six keys (Questionnaire - QuestionnaireRun -
        Question - OpenAnswer - ExternalResource - Assessment) that
        contains the entity parameter decriptions
    """
    # Get all the processing timepoint psytools file
    dawba_files = [os.path.join(dawba_root, x)
                   for x in os.listdir(dawba_root)
                   if (os.path.isfile(os.path.join(dawba_root, x)) and 
                       timepoint in x and x.endswith(".csv"))]
   
    # Go through all dawba questionnaire files
    dawba = {}
    for csv_file in dawba_files:

        # Find the center that give us the file
        center_id = "unknown"
        for center in center_map.keys():
            if center.lower() in os.path.basename(csv_file).lower():
                center_id = center_map[center]
                break
        if center_id == "unknown":
            logging.error(
                "No center identifier for dawba '{0}'".format(csv_file))

        # Open the csv file
        with open(csv_file,"rb") as open_file:

            logging.info("Processing '{0}' file...".format(csv_file))

            # Parse the file in a dict:
            # fieldnames parameter is omitted to use the values in the first row
            # of the csvfile as the fieldnames.
            reader = csv.DictReader(open_file, fieldnames=None)

            # Mutiple rows are associated with one patient questionnaire
            patient_questions = {}
            for row in reader:

                # Get patient info
                patient_id = row.pop("dawbaID")
                patient_age = row.pop("age")
                patient_gender = "male" if row.pop("gender") == 1 else "female"
        
                # Get rater info
                rater_name = row.pop("ratername")
                rate_date = row.pop("ratedate")

                # Filter the patient id that must be a digit
                if patient_id.isdigit():

                    # Go through all questionnaire
                    for qname, qfields in dawba_map.iteritems():

                        # Create the associated questions
                        questions = []
                        answers = []
                        for qfield in qfields:
                
                            # Create answer
                            answer = "unknown"
                            if qfield in row:
                                answer = row[qfield]

                            # Create question entity structure
                            questions.append({
                                "text": qfield, 
                                "identifier": _md5_sum(qname + qfield)
                            })

                            # Create answer entity structure
                            answers.append({
                                "identifier": _md5_sum(qname + qfield + patient_id),
                                "value": answer,
                                "text": qfield
                            })

                        # Create questionnaire entity structure
                        questionnaire_struct = {
                            "version": "unknown",
                            "language": "unknown",
                            "type": "dawba",
                            "name": qname,
                            "identifier": _md5_sum(qname)
                        }

                        # Create questionnaire run entity structure
                        questionnairerun_struct = {
                            "user_ident": "unknow",
                            "iteration": "1",
                            "completed": "unknow",
                            "identifier": _md5_sum(qname + patient_id),
                            "valid": "unknow"
                        }

                        # Create the assessment entity structure
                        assessment_struct = {
                            "identifier": "IMAGEN_{0}".format(patient_id),
                            "age_of_subject": patient_age,
                            "timepoint": timepoint
                        }

                        # Create the external resource entity structure
                        resource_struct = {
                            "name": qname,
                            "filepath": csv_file
                        }

                        # Create final structure
                        cw_questionnaire = {
                            "Questionnaire": questionnaire_struct,
                            "QuestionnaireRun": questionnairerun_struct,
                            "Question": questions,
                            "OpenAnswer": answers,
                            "ExternalResource": [resource_struct, ],
                            "Assessment": assessment_struct
                        }
                        if not patient_id in dawba:
                            dawba[patient_id] = []
                        dawba[patient_id].append(cw_questionnaire)

    return dawba


###############################################################################
#   Questionnaire builder
###############################################################################

def build_questionnaire(csv_file, timepoint, patient_id_field, question_field,
                        answer_field, language_field, valid_field,
                        complete_field, iteration_field):
    """ Method to construct the psytools questionnaire (questionnaire - 
    questionnaire run - question).

    Parameters
    ----------
    csv_file: str (mandatory)
        the path to the questionnaire csv file
    timepoint: str (optional)
        the imagen project timepoint identifier
    *_field: the csv column name to acces the * element.

    Returns
    -------
    questionnaires:  dict of list of dict
        the first dictionnaries contains the psc2 as keys and then
        a list of dictionaries with six keys (Questionnaire - QuestionnaireRun -
        Question - OpenAnswer - ExternalResource - Assessment) that
        contains the entity parameter decriptions
    """

    # Build the questionnaire name and type
    qname = os.path.basename(csv_file).lower().replace("-", "_").split("_")
    qtype = qname[2]
    qname = "_".join(qname[:qname.index(timepoint.lower()) + 1])

    # Open the csv file
    questionnaires = {}
    with open(csv_file,"rb") as open_file:

        logging.info("Processing '{0}' file...".format(csv_file))

        # Parse the file in a dict:
        # fieldnames parameter is omitted to use the values in the first row
        # of the csvfile as the fieldnames.
        reader = csv.DictReader(open_file, fieldnames=None)

        # Mutiple rows are associated with one patient questionnaire
        patient_questions = {}
        for cnt, row in enumerate(reader):
    
            # Get the psc2
            patient_id = row[patient_id_field].split("-")
            user_ident = patient_id[-1]
            patient_id = patient_id[0]

            # Filter the patient id that must be a digit
            if patient_id.isdigit():

                # Create question entity structure
                question_structure = {
                    "text": row[question_field], 
                    "identifier": _md5_sum(qname + row[question_field])
                }

                # Create answer entity structure
                answer_structure = {
                    "identifier": _md5_sum(
                        qname + ":" + row[question_field] + ":" + patient_id +
                        ":" + row[iteration_field] + ":" + str(cnt)),
                    "value": row[answer_field],
                    "text": row[question_field]
                }

                # Create questionnaire entity structure
                questionnaire_struct = {
                    "version": "unknown",
                    "language": row[language_field],
                    "type": qtype,
                    "name": qname,
                    "identifier": _md5_sum(qname)
                }

                # Create questionnaire run entity structure
                qr_valid = "unknow"
                if "Valid" in row:
                    qr_valid = 1 if row[valid_field] == "t" else 0
                questionnairerun_struct = {
                    "user_ident": user_ident,
                    "iteration": row[iteration_field],
                    "completed": 1 if row[complete_field] == "t" else 0,
                    "identifier": _md5_sum(qname + patient_id),
                    "valid": qr_valid
                }

                # Insert items
                patient_questions.setdefault(
                    (patient_id, row[iteration_field]), []).append(
                        [questionnaire_struct, questionnairerun_struct,
                         question_structure, answer_structure])

        # Build the final structure
        for key, structures in patient_questions.iteritems():

            # Unpack key
            subject_id, iteration = key

            # Check that all questionnaire structure are identical
            questionnaire_struct = structures[0][0]
            q_check = numpy.asarray(
                [x[0] == questionnaire_struct for x in structures]).all()
            if not q_check:
                logging.error(
                    "The questionnaire are not aligned: questionnaire {0}, "
                    "patinent {1}.".format(csv_file, subject_id))

            # Check that all questionnaire run structure are identical
            questionnairerun_struct = structures[0][1]
            qr_check = numpy.asarray(
                [x[1] == questionnairerun_struct for x in structures]).all()
            if not qr_check:
                logging.error(
                    "The questionnaire run are not aligned: questionnaire "
                    "run {0}, patinent {1}.".format(csv_file, subject_id))

            # Create the assessment entity structure
            assessment_struct = {
                "identifier": "IMAGEN_{0}".format(subject_id),
                "age_of_subject": "0",
                "timepoint": timepoint
            }

            # Create the external resource entity structure
            resource_struct = {
                "name": qname,
                "filepath": csv_file
            }

            # Create final structure
            cw_questionnaire = {
                "Questionnaire": questionnaire_struct,
                "QuestionnaireRun": questionnairerun_struct,
                "Question": [x[2] for x in structures],
                "OpenAnswer": [x[3] for x in structures],
                "ExternalResource": [resource_struct, ],
                "Assessment": assessment_struct
            }

            if subject_id not in questionnaires:
                questionnaires[subject_id] = []
            questionnaires[subject_id].append(cw_questionnaire)

    return questionnaires


###############################################################################
#   Nifti parser
###############################################################################

def build_nifti(nifti_root, timepoint="FU2",
                modalities_of_interest=["epi", ("b0", "fieldmap"), "dti",
                                        "mprage", "t2", "flair"]):
    """ Method to construct the nifti scan elements (scan - external resource)
    from the nifti root path.

    Special modalities:

        * "epi": try to find the assoiated paradigm, raise an Exception otherwise.
        * "dti": try to find the assoiated .bvecs .bvals files, raise an
          Exception otherwise.

    Parameters
    ----------
    nifti_root: str (mandatory)
        the path to the processed nifti images
    timepoint: str (optional)
        the imagen project timepoint identifier
    modalities_of_interest: list of str (optional)
        the type of modalities we are looking for

    Returns
    -------
    nifti: dict of list of dict
        the first dictionnaries contains the psc2 as keys and then
        a list of dictionaries with four keys (Scan - ExternalResource -
        *Data - Assessment - ScoreValue) that contains the entities parameter
        decriptions.
    """
    # Get all the nifti processed subjects
    subjects = [x for x in os.listdir(nifti_root) 
                  if (os.path.isdir(os.path.join(nifti_root, x)) and
                     x not in exclude_patients)]

    # Go through all subjects
    nifti = {}
    for subject in subjects:

        # Init subject item
        nifti[subject] = []

        # Get all the modality associated to the subject
        modality_root = os.path.join(nifti_root, subject, "SessionA")
        modalities = [x for x in os.listdir(modality_root)
                       if os.path.isdir(modality_root)]

        # Split folder by modality
        s_modalities = dict((x if isinstance(x, str) else x[0], [])
                            for x in modalities_of_interest)
        for modality in modalities:
            for key in s_modalities:
                if not isinstance(key, tuple):
                    key = (key, )
                for sub_key in key:
                    if (sub_key.lower() in modality.lower() and 
                        "tensorinfo" not in modality.lower()):

                        s_modalities[key[0]].append(modality)
                        break
        
        # Clean s_modalities: T2W_FLAIR
        s_modalities["t2"] = [x for x in s_modalities["t2"]
                              if "flair" not in x.lower()]

        # Construct the assessment entity structure
        assessment_struct = {
            "identifier": "IMAGEN_{0}".format(subject),
            "age_of_subject": "0",
            "timepoint": timepoint
        }

        # Construct the scan entity structure
        for modality, paths in s_modalities.iteritems():

            # Build the scans
            if modality != "mprage" or len(paths) == 1:
                scans = build_scan(modality_root, paths, subject, modality,
                                   assessment_struct)
            nifti[subject].extend(scans)

    return nifti
                 

###############################################################################
#   Scan builder
###############################################################################

def build_scan(root_path, paths, subject_id, modality, assessment_struct,
               invalid_prefix=("o", "co")):

    """ Method to construct the nifti scan elements (scan - external resource)
    of a sequence type from a root path.

    Special modalities:

        * "epi": try to find the assoiated paradigm name.

    Parameters
    ----------
    root_path: str (mandatory)
        the path to the processed nifti images
    paths: str (mandatory)
        different paths to the same modality
    subject_id: str (mandatory)
        the psc2 code in study
    modality:
        the modality type
    invalid_prefix: tuple of str (optional)
        filter potential images to remove reoriented, reoriented and cropped
        images
    assessment_struct: dict (mandatory)
        the scan related asessment structure

    Returns
    -------
    scans: list dict
        a list of dictionaries with four keys (Scan - ExternalResource -
        *Data - Assessment - ScoreValue) that contains the entities parameter
        decriptions.
    """
    # Go through all folders
    scans = []
    for cnt, path in enumerate(paths):

        # Need one valid compressed nifti per folder
        full_path = os.path.join(root_path, path)
        ims = [x for x in os.listdir(full_path)
               if (os.path.isfile(os.path.join(full_path, x)) and
                   x.endswith(".nii.gz"))]

        # Filter potential images to remove reoriented, reoriented and cropped
        # images
        if len(ims) > 1:
            ims = [x for x in ims if not x.startswith(invalid_prefix)]

        # Assert we have only one image
        second_bo = None
        if len(ims) != 1:

            # Special case for b0 when two file are found (phase + amplitude
            # are splited)
            if "b0" in modality and len(ims) == 2:
                second_bo = ims[1]
            else:
                #raise Exception("Need one scan image, got {0}. Subject {1}, "
                #                "modality {2}".format(len(ims), subject_id, path))
                logging.error("Need one scan image, got {0}. Subject {1}, "
                              "modality {2}. Keep first only. Maybe two echos in "
                              "two files?".format(len(ims), subject_id, path))

        im = ims[0]
        im_path = os.path.join(full_path, im)

        # Create the scan entity structure
        if modality == "mprage":
            modality = "adni_mprage"
        scan_struct = {
            "type": modality.upper(),
            "filepath": im_path,
            "label": modality.upper(),
            "format": "NIFTI COMPRESSED",
            "position_acquisition": cnt + 1,
            "description": cnt + 1,
            "identifier": _md5_sum("IMAGEN_{0}_{1}".format(subject_id, im_path))
        }

        # Deal with epi scan type (description is expected to be new the 'epi'
        # string)
        if modality == "epi":
            type_suffix = path.lower() #.replace("-", " ").replace("_", " ").split()
            if "epi" in type_suffix:
                if "mid" in type_suffix:
                    scan_type = "mid"
                elif "stop" in type_suffix or "sst" in type_suffix:
                    scan_type = "stop_signal"
                elif "face" in type_suffix:
                    scan_type = "faces"
                elif "rest" in type_suffix:
                    scan_type = "rest"
                else:
                    raise Exception("Unknown epi sequence '{0}'.".format(
                        type_suffix))
                scan_struct["type"] += "_" + scan_type

        # Create the scan type entity structure
        scan_type_struct = {
           "type": u"MRIData",
           "voxel_res_x": 0,
           "voxel_res_y": 0,
           "voxel_res_z": 0,
           "fov_x": 0,
           "fov_y": 0,
           "tr": 0,
           "te": 0,
        }

        # Update the scan type entity type
        if modality == "epi":
            scan_type_struct["type"] = "FMRIData"
        elif modality == "dti":
            scan_type_struct["type"] = "DMRIData"
        elif modality == "processing":
            scan_type_struct["type"] = "PROCESSINGData"

        # Try to get sequence information from the dcm dump of a valid dicom
        # file
        dcm_dump_file = os.path.join(full_path, "dcmheader.txt")
        if os.path.isfile(dcm_dump_file):
            raise NotImplementedError(
                "The dicom dump parser has not been implemented yet.")

        # Create the resource entity structure
        resources = []

        # Deal with dti images (need two external resources)
        if modality == "dti":
            # Get files in path
            files = [x for x in os.listdir(full_path)
                       if os.path.isfile(os.path.join(full_path, x))]
            # Try to find the .bvals file in the same folder
            bvals = [x for x in files if x.endswith(".bval")]
            if not bvals:
                logging.error(
                    "No bvals found: Subject {0}, modality {1}".format(
                        subject_id, path))
            resources.append({
                "name": "BVAL",
                "filepath": bvals or "unknown"
            })
            # Try to find the .bvecs file in the same folder
            bvecs = [x for x in files if x.endswith(".bvec")]
            if not bvals:
                logging.error(
                    "No bvecs found: Subject {0}, modality {1}".format(
                        subject_id, path))
            resources.append({
                "name": "BVEC",
                "filepath": bvecs or "unknown"
            })

        # Deal with epi (need one external resource)
        elif modality == "epi":

            # Buil the behavioural data path
            paradigm_path = os.path.abspath(
                os.path.join(root_path, os.pardir, "BehaviouralData"))

            # If the folder exists
            if os.path.isdir(paradigm_path):

                # Get the sequence paradigm name
                paramdigm_type = scan_struct["type"].split("_")[1]

                # Get the paradigm files available in the behavioural directory
                paradigm_files = os.listdir(paradigm_path)
                paradigm_search = dict((x.split("_")[0], x) 
                                       for x in paradigm_files)

                # Try to find the associated paradigm
                paradigm_file = None
                for key, value in paradigm_map.iteritems():
                    if (paramdigm_type in value and key in paradigm_search):
                        paradigm_file = os.path.join(
                            paradigm_path, paradigm_search[key])
                        break

                # Raise an error if no paradigm file has been found
                if paramdigm_type not in paradigm_map["rest"]:
                    if paradigm_file is None:
                        logging.error(
                            "No paradigm found: Subject {0}, modality {1}, "
                            "paradigm type {2}.".format(
                                subject_id, path, paramdigm_type))
                    resources.append({
                        "name": os.path.basename(str(paradigm_file)),
                        "filepath": paradigm_file or "unknown"
                    })

            # Otherwise raise an error
            else:
                logging.error(
                    "No 'BehaviouralData' folder found: Subject {0}, modality "
                    "{1}.".format(
                        subject_id, path))

        # Create final structure
        cw_scan = {
            "Scan": [(scan_struct, scan_type_struct)],
            "ExternalResource": resources,
            "Assessment": [assessment_struct],
            "ScoreValue": []
        }

        # Store the final result
        scans.append(cw_scan)

        # Create an additional scan if a second b0 is found
        if second_bo is not None:
            scan_struct_2 = copy.deepcopy(scan_struct)
            im_path = os.path.join(full_path, second_bo)
            scan_struct_2["filepath"] = im_path
            scan_struct_2["identifier"] = _md5_sum(
                "IMAGEN_{0}_{1}".format(subject_id, im_path))
            cw_scan = {
                "Scan": [(scan_struct_2, scan_type_struct)],
                "ExternalResource": resources,
                "Assessment": [assessment_struct],
                "ScoreValue": []
            }

            # Store the second b0 result
            scans.append(cw_scan)

    return scans    
    

###############################################################################
#   Parser Tools
###############################################################################

def eval_fs_path(processed_root, psytools_root, dawba_root, timepoint="FU2"):
        """ Find the requested information on the file system
        """
        # Load the nifti images
        nifti = build_nifti(os.path.join(processed_root, "nifti"))

        # Load the psytools questionnaires
        psytools = build_psytools(psytools_root, timepoint)

        # Load the dawba questionnaires
        dawba = build_dawba(dawba_root, timepoint)

        return nifti, psytools, dawba


if __name__ == "__main__":
    
    logging.basicConfig(filename='test/new_log_nifti.txt',level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)
    processed_root = "/neurospin/imagen/FU2/processed_raw_tmp/processed"
    psytools_root = "/neurospin/imagen/RAW/PSC2/psytools/"
    dawba_root = "/neurospin/imagen/RAW/PSC2/dawba"
    eval_fs_path(processed_root, psytools_root, dawba_root)


        
        
