#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
from lxml import etree
import re
import hashlib
import os
import logging

# Xnat Imagen import
from xnat_config import (XNAT_PSYTOOL_TAGS_QUESTIONNAIRE, XNAT_TAGS_SKIPPED,
    XNAT_DAWBA_TAGS_QUESTIONNAIRE, XNAT_BEHAVIOURAL_TAGS_QUESTIONNAIRE,
    XNAT_RAW_FMRI_SCAN, XNAT_SPM_FMRI_SCAN, XNAT_FSL_SCAN,
    XNAT_RAW_ANATOMICAL_SCAN, XNAT_RAW_DIFFUSION_SCAN,
    XNAT_MISC_TAGS_QUESTIONNAIRE, XNAT_SPM_FMRI_SCAN_RESOURCE,
    XNAT_FREESURFER_SCAN, XNAT_QR_TAGS_QUESTIONNAIRE)

# Questionnaire entity
questionnaire_struct = {
    "test_version": "version",
    "language": "language"
}

# QuestionnaireRun entity
questionnairerun_struct = {
    "user_code_ident": "user_ident",
    "iteration": "iteration",
    "completed": "completed"
}

# Center entity
center_struct = {
    "identifier": [(
        "//xnat:experiment[@xsi:type='imagen:imagenSubjectVariablesData']"
        "/@ImagingCentreID")],
    "city": [(
        "//xnat:experiment[@xsi:type='imagen:imagenSubjectVariablesData']"
        "/@ImagingCentreCity")],
    "name": [(
        "//xnat:experiment[@xsi:type='imagen:imagenSubjectVariablesData']"
        "/@ImagingCentreCity")],
}

# Device entity
device_struct = {
    "name": ["//xnat:scanner"],
    "manufacturer": ["//xnat:scanner/@manufacturer"],
    "model": ["//xnat:scanner/@model"]
}

# Subject entity
subject_struct = {
    "identifier": ["//xnat:Subject/@ID"],
    "gender": ["xnat:demographics/xnat:gender"],
    "handedness": ["xnat:demographics/xnat:handedness"],
    "code_in_study": ["//xnat:Subject/@label"],
}

# Study entity
study_struct = {
    "name": ["//xnat:Subject/@project"],
    "data_filepath": ["unknown"],
}

# Assessment entity
assessment_struct = {
    "identifier": ["//xnat:Subject/@project"],
    "age_of_subject": ["unknown"],
}

# Parse the exported xnat xml to get patient informations
xnat_patient_structure = {
    "Center": center_struct,
    "Subject": subject_struct,
    "Device": device_struct,
    "Study": study_struct,
    "Assessment": assessment_struct,
}

# Parse the exported xnat xml to get scan informations
xnat_scan_structure = {
    "Scan": {
        "raw_fmri": [(raw_fmri[0], raw_fmri[1], 
        #"raw_fmri": [(raw_fmri[1], 
                      "//xnat:assessor[@xsi:type='{0}']".format(behavioural) 
                      if behavioural is not None else None)
                      for behavioural, raw_fmri in XNAT_RAW_FMRI_SCAN.iteritems()],
        #"spm": ([(spm_fmri, "None") for spm_fmri in XNAT_SPM_FMRI_SCAN] + 
        #        [(spm_fmri,) for spm_fmri in XNAT_SPM_FMRI_SCAN_RESOURCE]),
        #"fsl": [(fsl_data, "None") for fsl_data in XNAT_FSL_SCAN], 
        "anatomical": [(anatomical_data[0], anatomical_data[1], "None")
        #"anatomical": [(anatomical_data[1], "None")
                       for anatomical_data in XNAT_RAW_ANATOMICAL_SCAN],
        "diffusion": [(diffusion_data[0], diffusion_data[1], "None")
        #"diffusion": [(diffusion_data[1], "None")
                       for diffusion_data in XNAT_RAW_DIFFUSION_SCAN],
        #"freesurfer": [(fs_data[0], fs_data[1]) for fs_data in XNAT_FREESURFER_SCAN],
    }
}

# Parse the exported xnat xml to get questionnaire informations
xnat_questionnaire_structure = {
    "Questionnaire": {
        "psytools": ["//xnat:experiment[@xsi:type='{0}']".format(name)
                    for name in XNAT_PSYTOOL_TAGS_QUESTIONNAIRE],
        "dawba": ["//xnat:experiment[@xsi:type='{0}']".format(name)
                  for name in XNAT_DAWBA_TAGS_QUESTIONNAIRE],
        "behavioural": ["//xnat:experiment[@xsi:type='{0}']".format(name)
                        for name in XNAT_BEHAVIOURAL_TAGS_QUESTIONNAIRE],
        "misc": ["//xnat:experiment[@xsi:type='{0}']".format(name)
                 for name in XNAT_MISC_TAGS_QUESTIONNAIRE],  
        "qr": ["//xnat:experiment[@xsi:type='{0}']".format(name)
                 for name in XNAT_QR_TAGS_QUESTIONNAIRE], 
    }
}

# Some Global Varibles
image_exts = (".nii", ".nii.gz")
search_data_struct = {
    "resources": "resource",
    "out": "file",
}
_ILLEGAL_CHARACTERS = u'\\/:*?"<>|. \t\r\n\0'
_CLEANUP_TABLE = dict((ord(char), u'_') for char in _ILLEGAL_CHARACTERS)


###############################################################################
#   Questionnaire parser
###############################################################################

def build_questionnaire(questionnaire_xml_element, nsmap=None):
    """ Method to construct the questionnaire (questions - answers) from
    an IMAGEN experiment element.

    Parameters
    ----------
    questionnaire_xml_element: lxml.etree._Element (mandatory)
        structure that contains the imagen questionnaire informations.
    nsmap: dict (optional)
        namespace where to execute the xml command

    Returns
    -------
    cw_questionnaire: dict
        a dictionary with six keys (Questionnaire - QuestionnaireRun -
        Question - OpenAnswer - ExternalResource - Assessment) that
        contains the entity parameter decriptions
    """
    # Create a copy of the structure to fill
    cw_questionnaire_struct = {}
    cw_questionnairerun_struct = {}
    cw_questionnaire = {
        "Questionnaire": None,
        "QuestionnaireRun": None,
        "Question": [],
        "OpenAnswer": [],
        "ExternalResource": [],
        "Assessment": None
    }

    # Get the subject ID
    qid = questionnaire_xml_element.find(
        "xnat:subject_ID", namespaces=nsmap).text

    # Go through the xml element to get the required questionnaire
    # informations
    qidentifier = questionnaire_xml_element.get("ID")
    # Find the timepoint (BL or FU1)
    qtimepoint = "BL"
    if "fu" in qidentifier.lower():
        qtimepoint = "FU1"
    # Split identifier
    m = qidentifier.replace(qid.replace("IMAGEN_", ""), "_")
    s = [x.lower() for x in m.split("_") if x]
    qtype = s[0]
    qname = "_".join(s)

    # Add all questions attached directly to this node,
    # Skip some tags to get the question - answer items only.
    for tag, value in questionnaire_xml_element.items():
        if tag not in XNAT_TAGS_SKIPPED:
            cw_questionnaire["Question"].append({
                "text": tag, 
                "identifier": _md5_sum(qname + tag)
            })
            cw_questionnaire["OpenAnswer"].append({
                "identifier": _md5_sum(qname + tag + qid),
                "value": value or " ",
                "text": tag
            })                

    # Get through the xml structure
    sub_elements = questionnaire_xml_element.getchildren()
    qage = None
    # Get multiple serie tag
    serie_tags = []
    for sub_element in sub_elements:
        small_tag = sub_element.tag.split("}")[1]

        # Fill some informations required to create the Questionnaire - 
        # QuestionnaireRun entities
        if small_tag in questionnaire_struct:
            cw_questionnaire_struct[questionnaire_struct[small_tag]] = sub_element.text
        if small_tag in questionnairerun_struct:
            cw_questionnairerun_struct[questionnairerun_struct[small_tag]] = sub_element.text

        # Special case for age parameter
        if (qage is None and 
            small_tag in ["processed_age_for_test", "age_for_test"]):
            qage = sub_element.text

        # Special case for subject id
        #if small_tag=="subject_ID":
        #    qid = sub_element.text

        # Skip some tags to get the question - answer items
        if small_tag not in XNAT_TAGS_SKIPPED:
            # For Qr need to hack serie name
            unique_small_tag = small_tag
            if small_tag == "Serie":
                unique_small_tag = sub_element.get("name")
            if not unique_small_tag in serie_tags:
                cw_questionnaire["Question"].append({
                    "text": unique_small_tag, 
                    "identifier": _md5_sum(qname + unique_small_tag)
                })
                cw_questionnaire["OpenAnswer"].append({
                    "identifier": _md5_sum(qname + unique_small_tag + qid),               
                    "value": sub_element.text or " ",
                    "text": unique_small_tag
                })
                serie_tags.append(unique_small_tag)

        # If an external resource found create the corresponding cw structure
        if small_tag == "resources":
            cw_questionnaire["ExternalResource"] = build_external_resources(
                sub_element)
                     
    # Fill the entity parmaters structures
    cw_questionnaire_struct["type"] = qtype
    cw_questionnaire_struct["name"] = qname
    cw_questionnaire_struct["identifier"] = _md5_sum(qname)
    cw_questionnairerun_struct["identifier"] = _md5_sum(qidentifier)
    if "user_ident" not in cw_questionnairerun_struct:
        cw_questionnairerun_struct["user_ident"] = "unknown"

    # Store the results
    cw_questionnaire["Assessment"] = {
        "identifier": qid,
        "age_of_subject": qage or "0",
        "timepoint": qtimepoint,
    }
    cw_questionnaire["Questionnaire"] = cw_questionnaire_struct
    cw_questionnaire["QuestionnaireRun"] = cw_questionnairerun_struct

    return cw_questionnaire

def build_external_resources(resources_xml_element):
    """ Method to construct a set of external resources from
    an IMAGEN resources xml element.

    Parameters
    ----------
    resources_xml_element: lxml.etree._Element (mandatory)
        structure that contains the imagen resource informations.

    Returns
    -------
    cw_external_resources: list of dict
        a list of dictionaries with two keys (name - filepath)
        that contains the ExternalResource entities parameters.
    """
    # Create the output
    cw_external_resources = []

    # Get through the xml structure
    sub_elements = resources_xml_element.getchildren()
    for sub_element in sub_elements:
        # Search for resource element
        small_tag = sub_element.tag.split("}")[1]
        if small_tag == "resource":
            # Create a new ExternalResource cw element
            if sub_element.get("URI", None) is not None:
                cw_external_resources.append({
                    "name": sub_element.get("label"),
                    "filepath": sub_element.get("URI").replace(
                        "/data/xnat_private/archive/IMAGEN/arc001/",
                        "/neurospin/imagen/")
                })

    return cw_external_resources


###############################################################################
#   Scan parser
###############################################################################

def build_scan(scan_xml_elements, nsmap=None):
    """ Method to construct the scan (scan - external resource - score value)
    from an IMAGEN scan element.

    Parameters
    ----------
    scan_xml_elements: list of lxml.etree._Element (mandatory)
        list of structures that contain the imagen scan informations.
        The first item may contains sequence information as spacing.
        If the last item is not None, it is considered as an external resource
        of all the other elements
    nsmap: dict (optional)
        namespace where to execute the xml command

    Returns
    -------
    cw_scan: list dict
        a list of dictionaries with four keys (Scan - ExternalResource -
        *Data - ScoreValue) that contains the entity parameter decriptions
    """
    # Create the output
    cw_scan = {
        "Scan": [],
        "ExternalResource": [],
        "Assessment": [],
        "ScoreValue": [],
    }

    # Create a parameter to store the scan type
    cw_scan_type = None

    # Go through the list of xml element to get the required scan
    # informations
    for cnt, selement in enumerate(scan_xml_elements[:-1]):

        # Check if an element was found in the xml XNAT file
        if selement is not None:

            # Create en scan type struct
            scan_type_struct = {
               "type": u"unknown",
               "voxel_res_x": 0,
               "voxel_res_y": 0,
               "voxel_res_z": 0,
               "fov_x": 0,
               "fov_y": 0,
               "tr": 0,
               "te": 0,
            }

            # Create scan struct
            scan_struct = {
                "identifier": u"unknown",
                "type": u"unknown",
                "label": u"unknown",
                "filepath": u"unknown",
                "format": u"unknown",
                "valid": u"unknown",
            }

            # Store iamges and resources
            images = []
            resources = []
    
            # First get the type element
            scan_struct["type"] = (selement.get("type") or 
                selement.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
            if scan_struct["type"] == "EPI_short_MID":
                scan_struct["type"] = "EPI_mid"

            # Get through child elements
            sub_elements = selement.getchildren()
            for sub_element in sub_elements:

                # Remove comment field
                if not isinstance(sub_element, etree._Comment):

                    # Search for scan elements
                    small_tag = sub_element.tag.split("}")[1]
                    if small_tag == "quality":
                        scan_struct["valid"] = sub_element.text
                    elif small_tag == "file":
                        images.append(sub_element.get("URI"))
                        scan_struct["filepath"] = sub_element.get("URI").replace(
                            "/data/xnat_private/archive/IMAGEN/arc001/",
                            "/neurospin/imagen/")
                        scan_struct["label"] = cleanup(sub_element.get("content", u"unknown"))
                        scan_struct["format"] = sub_element.get("format")
                    elif small_tag == "image_session_ID":
                        scan_struct["identifier"] = _md5_sum(
                            sub_element.text)
                    # Try to get files
                    elif small_tag in ("resources", "out"):

                        # Get files from items
                        file_element = sub_element.findall(
                            "xnat:{0}".format(search_data_struct[small_tag]),
                            namespaces=nsmap)
                        paths = [resource.get("URI")
                            for resource in file_element]
                        
                        # Sort files by type
                        images.extend([path for path in paths 
                            if path.endswith(image_exts)])
                        resources.extend([path for path in paths 
                            if not path.endswith(image_exts)])
                    # Try to get scan type from the first element
                    elif (small_tag == "parameters" and cnt == 0):
                        sub_parameters = sub_element.getchildren()
                        # Get the scan type
                        if "EPI" in scan_struct["type"]:
                            scan_type_struct["type"] = "FMRIData"
                        elif "DTI" in scan_struct["type"]:
                            scan_type_struct["type"] = "DMRIData"
                        else:
                            scan_type_struct["type"] = "MRIData"
                        # Find all sequence informations
                        for sub_parameter in sub_parameters:
                            intern_small_tag = sub_parameter.tag.split("}")[1]
                            if intern_small_tag == "voxelRes":
                               scan_type_struct["voxel_res_x"] = sub_parameter.get("x")
                               scan_type_struct["voxel_res_y"] = sub_parameter.get("y")
                               scan_type_struct["voxel_res_z"] = sub_parameter.get("z")
                            elif intern_small_tag == "fov":
                               scan_type_struct["fov_x"] = sub_parameter.get("x")
                               scan_type_struct["fov_y"] = sub_parameter.get("y")
                            elif intern_small_tag == "tr":
                               scan_type_struct["tr"] = sub_parameter.text
                            elif intern_small_tag == "te":
                               scan_type_struct["te"] = sub_parameter.text
                            # Store the result
                            cw_scan_type = scan_type_struct
                    # Create a processing flag
                    elif cnt == 0:
                        cw_scan_type = {
                            "type": "PROCESSINGData",
                        }

            # Check if a valid scan has been found
            images = [x for x in set(images) if x]
            resources = [x for x in set(resources) if x]

            # No image found
            if len(images) == 0:
                logging.error("No image found, force to skip xml element")

            # Normal case
            elif len(images) == 1:

                # Set the scan if necessary
                if scan_struct["filepath"] == "unknown":
                    scan_struct["filepath"] = images[0].replace(
                        "/data/xnat_private/archive/IMAGEN/arc001/",
                        "/neurospin/imagen/")
                    scan_struct["label"] = cleanup(scan_struct["type"])
                    if os.path.splitext(images[0])[1] == ".gz":
                        scan_struct["format"] = "NIFTI COMPRESSED"
                    else:
                        scan_struct["format"] = "NIFTI"
                    scan_struct["description"] = selement.get("dc")
                    scan_struct["position_acquisition"] = (
                        selement.get("number") or u"-1")                           
                    scan_struct["identifier"] = _md5_sum(
                        selement.get("ID"))

                # Set the external resources
                for resource in resources:
                    external_resource_struct = {
                        "name": (os.path.splitext(resource)[1][1:].upper()),  # + 
                                 # "_" + selement.get("ID")),
                        "filepath": resource.replace(
                            "/data/xnat_private/archive/IMAGEN/arc001/",
                            "/neurospin/imagen/"),
                    }
                    # Store cw external_resource
                    cw_scan["ExternalResource"].append(
                        external_resource_struct)

            # Error, more than one image found in resource
            else:
                raise Exception(
                    "More than one have been found in the resource "
                    "element {1}, got {0}".format(
                    len(images), scan_struct["type"]))       

            # Store cw scan
            cw_scan["Scan"].append((scan_struct, cw_scan_type))

            # Create an assessment
            session_id = (
                selement.findall("xnat:image_session_ID", namespaces=nsmap) +
                selement.findall("xnat:imageSession_ID", namespaces=nsmap))[0].text
            cw_scan["Assessment"].append({
                "identifier": session_id,  # scan_struct["label"],
                "age_of_subject": "0",
                "timepoint": "BL",
            })

    # Check if an external resource has been specified (used to set the
    # behavioural fmri informations, freesurfer file and freesurfer score
    # values)
    selements = scan_xml_elements[-1]
    if selements is not None:

        # Go through all resource items
        for cnt, selement in enumerate(selements):

            # Build struct (do not parse the file as it was done in xnat)
            xnat_out_element = selement.findall(
                "xnat:out/xnat:file", namespaces=nsmap)
            xnat_out_element.extend(
                selement.findall("xnat:resources/xnat:resource", namespaces=nsmap))
            for resource in xnat_out_element:
                external_resource_struct = {
                     "name": selement.get("ID"),
                     "filepath": resource.get("URI").replace(
                        "/data/xnat_private/archive/IMAGEN/arc001/",
                        "/neurospin/imagen/"),
                }
                # Store cw external_resource
                cw_scan["ExternalResource"].append(external_resource_struct)

                # Create an assessment if only behavioural data has been set
                if len(cw_scan["Assessment"]) == 0:
                    cw_scan["Assessment"].append({
                        "identifier": cleanup(
                            selement.get(
                            "{http://www.w3.org/2001/XMLSchema-instance}type")),
                        "age_of_subject": "0",
                        "timepoint": "BL",
                    })

            # Extract Freesurfer Score values
            xnat_out_element = selement.findall(
                "fs:measures/fs:volumetric/fs:regions/fs:region",
                namespaces=nsmap)
            xnat_out_element.extend(selement.findall(
                "fs:measures/fs:surface/fs:hemisphere/fs:regions/fs:region",
                namespaces=nsmap))
            for score in xnat_out_element:
                score_struct = {}
                measure = score.getparent().getparent()
                # Construct score name
                hemisphere = measure.get("name")
                if hemisphere is not None:
                    score_struct["text"] = "fs_surface_{0}".format(hemisphere)
                else:
                    score_struct["text"] = "fs_volumetric"
                # Get global scores
                for item in measure.getchildren():
                    # Remove comment field and regions
                    if (not isinstance(item, etree._Comment) and 
                            "regions" not in repr(item)):
                        local_score_struct = {
                            "text": (score_struct["text"] + "_" +
                                     repr(item).split("}")[1].split()[0]),
                            "value": item.text,
                        }
                        cw_scan["ScoreValue"].append(local_score_struct)
                # Get sub scores
                for item in score.getchildren():
                    # Remove comment field
                    if not isinstance(item, etree._Comment):
                        local_score_struct = {
                            "text": (score_struct["text"] + "_" + score.get("name") +
                                     repr(item).split("}")[1].split()[0]),
                            "value": item.text,
                        }
                        cw_scan["ScoreValue"].append(local_score_struct)

            # Hugly trick to change Freesurfer identifier
            dtype = selement.get(
                "{http://www.w3.org/2001/XMLSchema-instance}type")
            if dtype == "fs:fsData":
                version = selement.find("fs:version", namespaces=nsmap).text
                dtype =  cleanup(dtype + "_" + version)
                cw_scan["Assessment"][0]["identifier"] = dtype
                cw_scan["Scan"][0][0]["type"] = dtype
     
    return cw_scan


###############################################################################
#   Parser Tools
###############################################################################

def eval_xml_path(struct_to_eval, xml_root, nsmap, keep_first_element_only=False):
        """ Find the requested information in the xml file
        """
        # Go through the entity types
        for entity_name, entity_params in struct_to_eval.iteritems():
            # Go through the entity parameters
            for param_name, xml_paths in entity_params.iteritems():
                # Go through the xml paths
                for cnt, xml_path in enumerate(xml_paths):
                    # Get the xml value(s)
                    if isinstance(xml_path, tuple):
                        param_value = []
                        for path in xml_path[:-1]:
                            param_value.extend(
                                xml_root.xpath(path, namespaces=nsmap))
                        resource = xml_root.xpath(xml_path[-1], namespaces=nsmap) or None
                        param_value.append(resource)
                    else:
                        param_value = xml_root.xpath(xml_path, namespaces=nsmap)
                    # Check if we are only interested by the first occurence
                    if keep_first_element_only:
                        # If we have at least on value store this value
                        if len(param_value) > 0:
                            param_value = param_value[0]
                            if isinstance(param_value, str):
                                entity_params[param_name] = param_value
                            else:
                                entity_params[param_name] = param_value.text
                        # Otherwise return None
                        else:
                            entity_params[param_name] = "unknown"
                    # Otherwise return the xml value
                    else:
                        xml_paths[cnt] = param_value
    

def _md5_sum(name):
    """ Create a md5 sum of a name

    Parameters
    ----------
    name: str (mandatory)
        a string that will be hash.

    Returns
    -------
    md5: str
        the md5 sum of the input name.
    """
    m = hashlib.md5()
    m.update(name)
    return m.hexdigest()


def cleanup(attribute):
    """ Get rid of illegal characters.

    Parameters
    ----------
    attribute  : unicode
        Decoded string.

    Returns
    -------
    unicode
        String with illegal characters replaced.

    """
    return attribute.decode('latin_1').translate(_CLEANUP_TABLE).upper()


###############################################################################
#   Main
###############################################################################

if __name__ == "__main__":

    # Load the xml file
    xml_file = "/home/ag239446/tmp/IMAGEN_000000001274.xml"
    tree = etree.parse(xml_file)
    xml_root = tree.getroot()
    nsmap = xml_root.nsmap

    # Eval the xml strucutre
    eval_xml_path(xnat_patient_structure, xml_root, nsmap, True)
    eval_xml_path(xnat_questionnaire_structure, xml_root, nsmap, False)
    eval_xml_path(xnat_scan_structure, xml_root, nsmap, False)

    # Organize the parsed data to be compliant with the cw organization
    # Do questionnaire
    patient_questionnaires = []
    for qname, qtypes in xnat_questionnaire_structure.iteritems():
        for qtype, qelements in qtypes.iteritems():
            for qelement in qelements:
                if len(qelement) == 1:
                    patient_questionnaires.append(
                        build_questionnaire(qelement[0], nsmap))

    # Do scan
    patient_scans = []
    for sname, stypes in xnat_scan_structure.iteritems():
        for stype, selements in stypes.iteritems():
            for selement in selements:
                patient_scans.append(build_scan(selement, nsmap))

    print "\n\nPatient:::::\n", xnat_patient_structure
    print "\n\nQuestionnaire:::::\n", patient_questionnaires[0].keys()
    print "\n\nSCAN:::::\n", patient_scans[0].keys()

    print stop

    # Do scan
    patient_scans = []
    for sname, stypes in xnat_scan_structure.iteritems():
        print "\n\n******", sname
        for stype, selements in stypes.iteritems():
            print "\n->", stype
            for selement in selements:
                patient_scans.append(build_scan(selement, nsmap))
            for key, item in patient_scans[-1].iteritems():
                print "\n+", key, ": ", item

   
