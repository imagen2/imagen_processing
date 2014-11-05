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
import copy
from lxml import etree
import logging
import sys

# Parser import
from imagen_xnat_parser import (build_scan, eval_xml_path, build_questionnaire)
from imagen_xnat_parser import xnat_patient_structure as xnat_patient_structure_ref
from imagen_xnat_parser import xnat_scan_structure as xnat_scan_structure_ref
from imagen_xnat_parser import xnat_questionnaire_structure as xnat_questionnaire_structure_ref


def progress_bar(ratio, title="", bar_length=40):
    """ Method to generate a progress bar.

    Parameters
    ----------
    ratio: float (mandatory 0<ratio<1)
        float describing the current processing status.
    title: str (optional)
        a title to identify the progress bar.
    bar_length: int (optional)
        the length of the bar that will be ploted.
    """
    progress = int(ratio * 100.)
    block = int(round(bar_length * ratio))
    text = "\r{2} in Progress: [{0}] {1}%".format(
        "=" * block + " " * (bar_length - block), progress, title)
    sys.stdout.write(text)
    sys.stdout.flush()


# Get the path to the data
data_path = "/neurospin/imagen/export/xml-2014-04-08/"
xml_files = [os.path.abspath(os.path.join(data_path, fname))
             for fname in os.listdir(data_path) 
             if fname.endswith(".xml")]

# List to store file with not expected organization
parsing_errors = []

# Parsing
nb_files = float(len(xml_files))
for cnt, xml_file in enumerate(xml_files):
    # Print status
    progress_bar(
        float(cnt) / nb_files,
        title="Processing {0}: {1}...".format(cnt, os.path.basename(xml_file)))

    try:
        # Load the xml file
        tree = etree.parse(xml_file)
        xml_root = tree.getroot()
        nsmap = xml_root.nsmap

        # Parse the xml file
        xnat_patient_structure = copy.deepcopy(xnat_patient_structure_ref)
        xnat_questionnaire_structure = copy.deepcopy(
            xnat_questionnaire_structure_ref)
        xnat_scan_structure = copy.deepcopy(xnat_scan_structure_ref)
        eval_xml_path(xnat_patient_structure, xml_root, nsmap, True)
        eval_xml_path(xnat_questionnaire_structure, xml_root, nsmap, False)
        eval_xml_path(xnat_scan_structure, xml_root, nsmap, False)

        # Hack the code in study field to get the psc1 code
        cis = xnat_patient_structure["Subject"]["code_in_study"]
        xnat_patient_structure["Subject"]["code_in_study"] = cis.replace("IMAGEN_", "")

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

    except:
        parsing_errors.append(xml_file)
        logging.error("Error {0}: {1}.\n{2}".format(cnt, xml_file, sys.exc_info()[1]))

print "Errors summary: {0}".format(len(parsing_errors))
print parsing_errors
        


