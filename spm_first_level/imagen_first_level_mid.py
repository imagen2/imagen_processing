#! /usr/bin/env python

# Copyright (c) 2015-2016 CEA
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software. You can use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty and the software's author, the holder of the
# economic rights, and the successive licensors have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading, using, modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean that it is complicated to manipulate, and that also
# therefore means that it is reserved for developers and experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and, more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# Imports
import os
import glob
import tarfile
import numpy as np
import shutil
import argparse
import gzip

# CAPSUL import
from capsul.study_config import StudyConfig
from capsul.api import get_process_instance

# Mmutils import
from mmutils.adapters.io import gzip_file


# Command line
def is_directory(dirarg):
    """ Type for argparse - checks that directory exists.
    """
    if not os.path.isdir(dirarg):
        raise argparse.ArgumentError(
            "The directory '{0}' does not exist!".format(dirarg))
    return dirarg

def is_file(filearg):
    """ Type for argparse - checks that output file exists.
    """
    if not os.path.isfile(filearg):
        raise argparse.ArgumentError(
            "The file '{0}' does not exist!".format(filearg))
    return filearg


# transcoding table: from behavioural files to onset interpretation
# rfom BT's code
transcoding_table = {
    "anticip_hit_largewin": ('BIG_WIN', 'SUCCESS'),
    "anticip_hit_smallwin": ('SMALL_WIN', 'SUCCESS'),
    "anticip_hit_nowin": ('NO_WIN', 'SUCCESS'),
    "anticip_missed_largewin": ('BIG_WIN', 'FAILURE'),
    "anticip_missed_smallwin": ('SMALL_WIN', 'FAILURE'),
    "anticip_missed_nowin": ('NO_WIN', 'FAILURE'),
    # "anticip_noresp": special case handled differently
    "feedback_hit_largewin": ('BIG_WIN', 'SUCCESS'),
    "feedback_hit_smallwin": ('SMALL_WIN', 'SUCCESS'),
    "feedback_hit_nowin": ('NO_WIN', 'SUCCESS'),
    "feedback_missed_largewin": ('BIG_WIN', 'FAILURE'),
    "feedback_missed_smallwin": ('SMALL_WIN', 'FAILURE'),
    "feedback_missed_nowin": ('NO_WIN', 'FAILURE'),
    # "feedback_noresp": as previous, handled differently
    }


def csv_to_onset(data_onsets_name, formats, outfile, timepoint):
    """
    step1: read csv and generate proper list of dictionary
    step2: interpret csv information to generate onset
    """

    print data_onsets_name

    def format_element(a, _format):
        """
        format csv content
        """
        if len(a) == 0:
            return ""
        if _format == "float":
            return float(a.replace('"', ''))/1000.
        elif _format == "string":
            return str(a)
        elif _format == 'integer':
            return int(a)

    with open(data_onsets_name, 'r') as _file:
        lines = _file.readlines()

    # first line is useless
    # second line contains headers
    temp = lines[1].split("\t")
    headers = []
    for item in temp[:-1]:
        headers.append(item.replace(" ", "_").lower())

    # initialize csv information container
    csv_content = []

    # parse csv
    for line in lines[2:]:
        temp = {}
        line = line.replace('"', '')
        if len(line) < 50:
            continue
        for item, _format, header in zip(line.split("\t")[:-1],
                                         formats,
                                         headers):
            temp[header] = format_element(item, _format)
        csv_content.append(temp)

    onset_header = ["Conditions", "Onsets", "Durations"]

    onset_content = [
        "anticip_hit_largewin",
        "anticip_hit_smallwin",
        "anticip_hit_nowin",
        "anticip_missed_largewin",
        "anticip_missed_smallwin",
        "anticip_missed_nowin",
        "anticip_noresp",
        "feedback_noresp",
        "feedback_hit_largewin",
        "feedback_hit_smallwin",
        "feedback_hit_nowin",
        "feedback_missed_largewin",
        "feedback_missed_smallwin",
        "feedback_missed_nowin",
        "pressleft",
        "pressright",
        ]

    not_found = onset_content[:]

    # 1) process restart : time sequence decrease suddenly
    ref = -1.
    ocsv_content = csv_content[:]
    for i, line in enumerate(csv_content):
        st = line['trial_start_time_(onset)']
        if float(st) < ref:
            ocsv_content = csv_content[i:]
            print "\n\tWARNING: reset detected condition in stimulis !"
        ref = float(st)
    csv_content = ocsv_content[:]
    print " - INFO : behavior file contains {} lines".format(len(csv_content))

    # 2) generate onset lines and set durations
    lines = []
    for line_content in csv_content:
        if line_content["response_made_by_subject"] == "NO RESPONSE":
            lines.append("anticip_noresp;{0};4.0".format(
                line_content["anticipation_phase_start_time"]))
            if "anticip_noresp" in not_found:
                not_found.remove("anticip_noresp")
            lines.append("feedback_noresp;{0};1.45".format(
                line_content["feedback_phase_start_time"]))
            if "feedback_noresp" in not_found:
                not_found.remove("feedback_noresp")
            continue

        elif "left" in line_content["response_made_by_subject"].lower():
            lines.append("pressleft;{0};0.0".format(
                line_content["response_time"]))
            if "pressleft" in not_found:
                not_found.remove("pressleft")
        elif "right" in line_content["response_made_by_subject"].lower():
            lines.append("pressright;{0};0.0".format(
                line_content["response_time"]))
            if "pressright" in not_found:
                not_found.remove("pressright")

        for element, conditions in transcoding_table.iteritems():
            if conditions == (line_content["trial_category"],
                              line_content["outcome"]):
                if "feedback" in element:
                    lines.append(
                        "{0};{1};1.45".format(
                            element,
                            line_content["feedback_phase_start_time"]))
                    if element in not_found:
                        not_found.remove(element)
                else:
                    lines.append(
                        "{0};{1};4.0".format(
                            element,
                            line_content["anticipation_phase_start_time"]))
                    if element in not_found:
                        not_found.remove(element)

    # 3) exclusion criteria on behavioral data for BL and FU2
    # not implemented

    # process not_found conditions
    if len(not_found) > 0:
        for element in not_found:
            lines.append("{0};nan;nan".format(element))

    # write onset file
    with open(outfile, 'w') as _file:
        _file.write(";".join(onset_header))
        _file.write("\n")
        for line in lines:
            _file.write("{0}\n".format(line))

    return onset_content, not_found


def generate_onsets(behav_file, timepoint, out_dir):
    """Convert the csv in onset format
    Update the path names from csv to onset
    Update the path with value None if the csv file is void

    Return:
    =======
        log : string
        outfile : String. Path to the corresponding onset.txt files
        missing_names : list of strings. Degenerated regressors
    """

    converters = ["integer",
                  "string",
                  "float",
                  "float",
                  "string",
                  "float",
                  "float",
                  "float",
                  'integer',
                  "string",
                  "float",
                  "float",
                  "string",
                  'integer',
                  "float",
                  "float",
                  "float"]

    outfile = os.path.join(out_dir, "onset.txt")
    namelist, missing_names = csv_to_onset(behav_file, converters, outfile,
                                           timepoint)

    if len(missing_names) > 0:
        log = "- INFO This session do not display these regressors: ", missing_names
    else:
        log = ''
    return log, outfile, missing_names


def set_pipeline_contrasts(timepoint):
    """
    set pipeline contrasts: different from one subject to another IF a
    regressor is missing
    """
    if (timepoint == "FU2") or (timepoint == "BL"):
        #[('Realign1', 'T', ['Realign1'], [1.0]), ()...]
        # 6 +(3up+3down) = 12  mvt regressors AND 3+6 = 9 compCorr regressors
        shadow_contrastsT_RP = [("Realign{0}".format(i), "T",
                        ['Realign{0}'.format(i), ],
                        [1., ]
                        ) for i in range(1, 13)]
        shadow_contrastsT_Comp = [("Realign{0}".format(i), "T",
                        ['Realign{0}'.format(i), ],
                        [1., ]
                        ) for i in range(13, 22)]

        # Specify the contrats list
        contrastsT =  [
            ("anticip_missed_nowin", "T", ['anticip_missed_nowin'],
             [1.]),
            ("anticip_hit_smallwin", "T", ['anticip_hit_smallwin'],
             [1.]),
            ("anticip_hit_nowin", "T", ['anticip_hit_nowin'],
             [1.]),
            ("anticip_missed_largewin", "T", ['anticip_missed_largewin', ],
             [1.]),
            ("anticip_missed_smallwin", "T", ['anticip_missed_smallwin', ],
             [1.]),
            ("feedback_hit_nowin", "T", ['feedback_hit_nowin'],
             [1.]),
            ("feedback_missed_largewin", "T", ['feedback_missed_largewin'],
             [1.]),
            ("feedback_missed_smallwin", "T", ['feedback_missed_smallwin'],
             [1.]),
            ("feedback_missed_nowin", "T", ['feedback_missed_nowin'],
             [1.]),
            ("pressleft", "T", ['pressleft'],
             [1.]),
            ("pressright", "T", ['pressright'],
             [1.]),
            # contrast as defined from BT's script
            ("anticip", "T", ['anticip_hit_largewin',
                              'anticip_hit_smallwin',
                              'anticip_hit_nowin',
                              'anticip_missed_largewin',
                              'anticip_missed_smallwin',
                              'anticip_missed_nowin'],
             [1./6, 1./6, 1./6, 1./6, 1./6, 1./6]),
            ("anticip_hit", "T", ['anticip_hit_largewin',
                                  'anticip_hit_smallwin',
                                  'anticip_hit_nowin'],
             [1./3, 1./3, 1./3]),
            ("anticip_missed", "T", ['anticip_missed_largewin',
                                     'anticip_missed_smallwin',
                                     'anticip_missed_nowin'],
             [1./3, 1./3, 1./3]),
            ("anticip_noresp", "T", ['anticip_noresp'],
             [1.]),
            # 'anticip_hit' - 'anticip_missed'
            ("anticip_hit - missed", "T", ['anticip_hit_largewin',
                                         'anticip_hit_smallwin',
                                         'anticip_hit_nowin',
                                         'anticip_missed_largewin',
                                         'anticip_missed_smallwin',
                                         'anticip_missed_nowin'],
             [1./3, 1./3, 1./3, -1./3, -1./3, -1./3]),
            # 'anticip_missed' - 'anticip_hit'
            ("anticip_missed - hit", "T", ['anticip_hit_largewin',
                                         'anticip_hit_smallwin',
                                         'anticip_hit_nowin',
                                         'anticip_missed_largewin',
                                         'anticip_missed_smallwin',
                                         'anticip_missed_nowin'],
             [-1./3, -1./3, -1./3, 1./3, 1./3, 1./3]),
            # 'anticip_hit' - 'anticip_noresp'
            ("anticip_hit - noresp", "T", ['anticip_hit_largewin',
                                         'anticip_hit_smallwin',
                                         'anticip_hit_nowin',
                                         'anticip_noresp'],
             [1./3, 1./3, 1./3, -3./3]),
            # 'anticip_noresp' - 'anticip_hit'
            ("anticip_noresp - hit", "T", ['anticip_hit_largewin',
                                         'anticip_hit_smallwin',
                                         'anticip_hit_nowin',
                                         'anticip_noresp'],
             [-1./3, -1./3, -1./3, 3./3]),
            ("anticip_hit_largewin - smallwin", "T", ['anticip_hit_largewin',
                                                      'anticip_hit_smallwin'],
             [1., -1.]),
            ("anticip_hit_largewin - nowin", "T", ['anticip_hit_largewin',
                                                   'anticip_hit_nowin'],
             [1., -1.]),
            ("anticip_hit_smallwin - nowin", "T", ['anticip_hit_smallwin',
                                                   'anticip_hit_nowin'],
             [1., -1.]),
            ("anticip_missed_largewin - smallwin", "T",
             ['anticip_missed_largewin',
              'anticip_missed_smallwin'],
             [1., -1.]),
            ("anticip_missed_largewin - nowin", "T",
             ['anticip_missed_largewin',
              'anticip_missed_nowin'],
             [1., -1.]),
            ("anticip_missed_smallwin - nowin", "T",
             ['anticip_missed_smallwin',
              'anticip_missed_nowin'],
             [1., -1.]),
            ("anticip - anticip_noresp", "T", ['anticip_hit_largewin',
                                               'anticip_hit_smallwin',
                                               'anticip_hit_nowin',
                                               'anticip_missed_largewin',
                                               'anticip_missed_smallwin',
                                               'anticip_missed_nowin',
                                               'anticip_noresp'],
             [1./6, 1./6, 1./6, 1./6, 1./6, 1./6, -6./6]),
            ("feedback", "T", ['feedback_hit_largewin',
                               'feedback_hit_smallwin',
                               'feedback_hit_nowin',
                               'feedback_missed_largewin',
                               'feedback_missed_smallwin',
                               'feedback_missed_nowin'],
             [1./6, 1./6, 1./6, 1./6, 1./6, 1./6]),
            ("feedback_hit", "T", ['feedback_hit_largewin',
                                   'feedback_hit_smallwin',
                                   'feedback_hit_nowin'],
             [1./3, 1./3, 1./3]),
            ("feedback_missed", "T", ['feedback_missed_largewin',
                                      'feedback_missed_smallwin',
                                      'feedback_missed_nowin'],
             [1./3, 1./3, 1./3]),
            ("feedback_hit-missed", "T", ['feedback_hit_largewin',
                                          'feedback_hit_smallwin',
                                          'feedback_hit_nowin',
                                          'feedback_missed_largewin',
                                          'feedback_missed_smallwin',
                                          'feedback_missed_nowin'],
             [1./3, 1./3, 1./3, -1./3, -1./3, -1./3]),
            ("feedback_missed-hit", "T", ['feedback_hit_largewin',
                                          'feedback_hit_smallwin',
                                          'feedback_hit_nowin',
                                          'feedback_missed_largewin',
                                          'feedback_missed_smallwin',
                                          'feedback_missed_nowin'],
             [-1./3, -1./3, -1./3, 1./3, 1./3, 1./3]),
            ("feedback_hit_largewin - smallwin", "T",
             ['feedback_hit_largewin',
              'feedback_hit_smallwin'],
             [1., -1.]),
            ("feedback_hit_largewin - nowin", "T",
             ['feedback_hit_largewin',
              'feedback_hit_nowin'],
             [1., -1.]),
            ("feedback_hit_smallwin - nowin", "T",
             ['feedback_hit_smallwin',
              'feedback_hit_nowin'],
             [1., -1.]),
            ("feedback_missed_largewin - smallwin", "T",
             ['feedback_missed_largewin',
              'feedback_missed_smallwin'],
             [1., -1.]),
            ("feedback_missed_largewin - nowin", "T",
             ['feedback_missed_largewin',
              'feedback_missed_nowin'],
             [1., -1.]),
            ("feedback_missed_smallwin - nowin", "T",
             ['feedback_missed_smallwin',
              'feedback_missed_nowin'],
             [1., -1.]),

            ("press L + R", "T",
             ['pressleft',
              'pressright'],
             [1., 1.]),
            ("press L - R", "T",
             ['pressleft',
              'pressright'],
             [1., -1.]),
            ("press R - L", "T",
             ['pressleft',
              'pressright'],
             [-1., 1.]),

            ("anticip_hit_somewin - nowin", "T",
             ['anticip_hit_largewin',
              'anticip_hit_smallwin',
              'anticip_hit_nowin'],
             [1./2, 1./2, -2./2]),
            ("anticip_missed_somewin - nowin", "T",
             ['anticip_missed_largewin',
              'anticip_missed_smallwin',
              'anticip_missed_nowin'],
             [1./2, 1./2, -2./2]),
            ("feedback_hit_somewin - nowin", "T",
             ['feedback_hit_largewin',
              'feedback_hit_smallwin',
              'feedback_hit_nowin'],
             [1./2, 1./2, -2./2]),
            ("feedback_missed_somewin - nowin", "T",
             ['feedback_missed_largewin',
              'feedback_missed_smallwin',
              'feedback_missed_nowin'],
             [1./2, 1./2, -2./2]),

            ("feedback_somewin_hit - missed", "T",
             ['feedback_hit_largewin',
              'feedback_hit_smallwin',
              'feedback_missed_largewin',
              'feedback_missed_smallwin'],
             [1./2, 1./2, -1./2, -1./2]),
            ("feedback_somewin_missed - win", "T",
             ['feedback_hit_largewin',
              'feedback_hit_smallwin',
              'feedback_missed_largewin',
              'feedback_missed_smallwin'],
             [-1./2, -1./2, 1./2, 1./2]),

            ("feedback_somewin - nowin", "T",
             ['feedback_hit_largewin',
              'feedback_hit_smallwin',
              'feedback_hit_nowin',
              'feedback_missed_largewin',
              'feedback_missed_smallwin',
              'feedback_missed_nowin'],
             [1./4, 1./4, -2./4, 1./4, 1./4, -2./4]),

            ("anticip_hit_largewin", "T",
             ['anticip_hit_largewin'],
             [1.]),
            ("- anticip_hit_largewin", "T",
             ['anticip_hit_largewin'],
             [-1.]),
            ("feedback_hit_largewin", "T",
             ['feedback_hit_largewin'],
             [1.]),
            ("- feedback_hit_largewin", "T",
             ['feedback_hit_largewin'],
             [-1.]),
            ("anticip_hit_largewin - feedback_hit_largewin", "T",
             ['anticip_hit_largewin',
              'feedback_hit_largewin'],
             [1., -1.]),
            ("feedback_hit_largewin - anticip_hit_largewin", "T",
             ['anticip_hit_largewin',
              'feedback_hit_largewin'],
             [-1., 1.]),
            ("anticip_hit_nowin - feedback_hit_nowin", "T",
             ['anticip_hit_nowin',
              'feedback_hit_nowin'],
             [1., -1.]),
            ("feedback_hit_nowin - anticip_hit_nowin", "T",
             ['anticip_hit_nowin',
              'feedback_hit_nowin'],
             [-1., 1.]),
        ] + shadow_contrastsT_RP + shadow_contrastsT_Comp
        # F contrasts
        contrastF_EI = [
            ("Effect of interest", "F",
             [
              ("anticip_hit_largewin", "T", ['anticip_hit_largewin'],
               [1]),
              ("anticip_hit_smallwin", "T", ['anticip_hit_smallwin'],
               [1]),
              ("anticip_hit_nowin", "T", ['anticip_hit_nowin'],
               [1]),
              ("anticip_missed_largewin", "T", ['anticip_missed_largewin', ],
               [1]),
              ("anticip_missed_smallwin", "T", ['anticip_missed_smallwin', ],
               [1]),
              ("anticip_missed_nowin", "T", ['anticip_missed_nowin', ],
               [1]),
              ("anticip_noresp", "T", ['anticip_noresp', ],
               [1]),
              ("feedback_hit_largewin", "T", ['feedback_hit_largewin'],
               [1]),
              ("feedback_hit_smallwin", "T", ['feedback_hit_smallwin'],
               [1]),
              ("feedback_hit_nowin", "T", ['feedback_hit_nowin'],
               [1]),
              ("feedback_missed_largewin", "T", ['feedback_missed_largewin'],
               [1]),
              ("feedback_missed_smallwin", "T", ['feedback_missed_smallwin'],
               [1]),
              ("feedback_missed_nowin", "T", ['feedback_missed_nowin'],
               [1]),
              ("feedback_noresp", "T", ['feedback_noresp'],
               [1]),
              ("pressleft", "T", ['pressleft'],
               [1]),
              ("pressright", "T", ['pressright'],
               [1])
             ]
             ),
            ("Anticip_hit_GainEffect", "F",
             [
              ("anticip_hit_largewin - smallwin", "T",
               ['anticip_hit_largewin',
                'anticip_hit_smallwin'],
               [1., -1.]),
              ("anticip_hit_smallwin - nowin", "T",
               ['anticip_hit_smallwin',
                'anticip_hit_nowin'],
               [1., -1.])
             ]),
            ("Anticip_missed_GainEffect", "F",
             [
              ("anticip_missed_largewin - smallwin", "T",
               ['anticip_missed_largewin',
                'anticip_missed_smallwin'],
               [1., -1.]),
              ("anticip_missed_smallwin - nowin", "T",
               ['anticip_missed_smallwin',
                'anticip_missed_nowin'],
               [1., -1.])]),
            ("Feedback_hit_GainEffect", "F",
             [("feedback_hit_largewin - smallwin", "T",
               ['feedback_hit_largewin',
                'feedback_hit_smallwin'],
               [1., -1.]),
              ("feedback_hit_smallwin - nowin", "T",
               ['feedback_hit_smallwin',
                'feedback_hit_nowin'],
               [1., -1.])]),
            ("Feedback_hit_GainEffect", "F",
             [
              ("feedback_missed_largewin - smallwin", "T",
               ['feedback_missed_largewin',
                'feedback_missed_smallwin'],
               [1., -1.]),
              ("feedback_missed_smallwin - nowin", "T",
               ['feedback_missed_smallwin',
                'feedback_missed_nowin'],
               [1., -1.])])
             ]

        contrastF_RP = shadow_contrastsT_RP
        contrastF_Comp = shadow_contrastsT_Comp
        constrastsF = contrastF_EI + [
                        ['Effects of rp', 'F', contrastF_RP],
                        ['Effects of compcorr', 'F', contrastF_Comp],
                      ]
        # All  type of contrasts are gathered
        contrasts = contrastsT + constrastsF
        return contrasts

def fix_pipeline_contrasts(ref_contrasts, missing_names):
    """
    Start from the reference contrast a patch it.
    In fact wil keep BThyreau+JBPoline strategy not C Moessnang
    """
    # clenup structure if a regressor is missing (an expected outcome did
    # not occur during the session)
    # recursive cleaner
    def contrast_check(contrast, missing):
        """
        check if the contrast require the missing one (or is the missing one)
        """
        if contrast[1] == "T":
            if contrast[0] in missing:
                return True
            for item in contrast[2]:
                if item in missing:
                    return True
        elif contrast[1] == "F":
            for reg in contrast[2]:
                if contrast_check(reg, missing):
                    return True
        return False

    # generate the subject-contrasts
    contrasts_stripped = ref_contrasts

    for missing in missing_names:
        tempo = []
        if len(missing) > 0:
            for cont_element in contrasts_stripped:
                if contrast_check(cont_element, missing):
                    continue
                tempo.append(cont_element)
        contrasts_stripped = tempo

    if missing_names:
        print "INFO:: Un -estimable contrasts T and F will not be computed:"
        print "missing names :", missing_names
        print set([item[0] for item in ref_contrasts]) - set([item[0] for item in contrasts_stripped])

    return contrasts_stripped


doc = """
First Level MID

python imagen_first_level_mid.py \
-s 000001441076 \
-t BL \
-i /neurospin/imagen/BL/processed/spm_preprocessing/000001441076/EPI_short_MID/swau000001441076s003a001.nii.gz \
-f /neurospin/imagen/BL/processed/freesurfer \
-n /neurospin/imagen/BL/processed/spm_new_segment/000001441076/u000001441076000001441076s006a1001_seg8.mat \
-r /neurospin/imagen/BL/processed/spm_preprocessing/000001441076/EPI_short_MID/rp_au000001441076s003a001.txt \
-b /neurospin/imagen/BL/processed/nifti/000001441076/BehaviouralData/mid_000001441076.csv \
-o /tmp/IMAGEN_TEST_MID

"""
parser = argparse.ArgumentParser(description=doc)
parser.add_argument(
    "-t", "--timepoint", dest="timepoint", type=str, required=True,
    choices=["BL", "FU2"], help="timepoint concerned by this process.")
parser.add_argument(
    "-o", "--outdir", dest="outdir", type=str, required=True,
    help="the output directory.")
parser.add_argument(
    "-f", "--fsdir", dest="fsdir", type=is_directory, required=True,
    help="the root of freesurfer directory.")
parser.add_argument(
    "-d", "--spmdir", dest="spmdir", type=is_directory,
    default="/i2bm/local/spm12",
    help="the spm directory.")
parser.add_argument(
    "-l", "--fslconfig", dest="fslconfig", type=is_file,
    default="/etc/fsl/4.1/fsl.sh",
    help="the FSL configuration file path.")
parser.add_argument(
    "-g", "--fsconfig", dest="fsconfig", type=is_file,
    default="/i2bm/local/freesurfer/SetUpFreeSurfer.sh",
    help="the Freesurfer configuration file path.")
parser.add_argument(
    "-m", "--matlabexec", dest="matlabexec", type=is_file,
    default="/neurospin/local/bin/matlab",
    help="the Matlab Executable path.")
parser.add_argument(
    "-e", "--erase", dest="erase", action="store_true",
    help="if activated, clean the subject output folder.")
parser.add_argument(
    "-s", "--sid", dest="sid", type=str, required=True,
    help="the subject identifier.")
parser.add_argument(
    "-n", "--matfile", dest="matfile", type=is_file, required=True,
    help="the spm_new_segment seg8 mat file.")
parser.add_argument(
    "-b", "--behavfile", dest="behavfile", type=is_file, required=True,
    help="the functionnal serie associated behavioral csv file (in BehavioralData folder")
parser.add_argument(
    "-r", "--rpfile", dest="rpfile", type=is_file, required=True,
    help="the realignment parameters file.")
parser.add_argument(
    "-i", "--inputvolume", dest="inputvolume", type=is_file, required=True,
    help="the 4D volume")
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true",
    help="output info.")
parser.add_argument(
    "-k", "--maskimage", dest="maskimage", type=is_file,
    default=('/neurospin/imagen/workspace/fmri/scripts/mask_dilated.nii'),
    help="the mask image.")
args = parser.parse_args()


# Create the subject output directory
if args.timepoint == "BL":
    dirname = "EPI_short_MID"
else:
    dirname = "EPI_mid"
soutdir = os.path.join(args.outdir, args.sid, dirname)
capsulwd = os.path.join(soutdir, "capsul")
if args.erase and os.path.isdir(soutdir):
    shutil.rmtree(soutdir)
if not os.path.isdir(capsulwd):
    os.makedirs(capsulwd)

# Create the study configuration
print "Study_config init..."
study_config = StudyConfig(
    modules=["MatlabConfig", "SPMConfig", "FSLConfig", "NipypeConfig"],
    use_smart_caching=False,
    use_fsl=True,
    fsl_config=args.fslconfig,
    use_matlab=True,
    matlab_exec=args.matlabexec,
    use_spm=True,
    spm_directory=args.spmdir,
    # spm_exec=args.spmbin,
    # spm_standalone=True,
    use_nipype=True,
    output_directory=capsulwd)
print "    ... done."

# Get the pipeline
pipeline = get_process_instance(
    "clinfmri.statistics.spm_first_level_pipeline.xml")

# unzip nifti file (to be destroyed after)
fmri_session_unizp = os.path.join(capsulwd,
                                  os.path.basename(
                                      args.inputvolume).replace(".gz", ""))

with gzip.open(args.inputvolume, 'rb') as f:
    file_content = f.read()
    with open(fmri_session_unizp, "wb") as _file:
        _file.write(file_content)

# generate onset
log_onset, onset_file, missing_names = generate_onsets(args.behavfile,
                                                       args.timepoint, soutdir)
if not onset_file:
    if args.verbose:
        print "{} - {}".format(args.sid, log_onset)
        print "STOP"
    # csv file invalid STOP
    exit(1)

pl_contrast = set_pipeline_contrasts(args.timepoint)
# if missing conditons fix the contrasts set

contrasts_fixed = fix_pipeline_contrasts(pl_contrast, missing_names)

# Configure the pipeline
# FreeSurfer config
pipeline.fsconfig = args.fsconfig
# Smoothing already performed in proproc IMAGEN
pipeline.smoother_switch = "no_smoothing"
# sequence information
pipeline.time_repetition = 2.2

# contrasts we have defined above
pipeline.contrasts = contrasts_fixed

# the 6 basic movement regressors are completed with wm, ventricles and
# extra mvt
# world to world transformation matrix
# number of extra noise covars to extract
pipeline.realignment_parameters = args.rpfile
pipeline.complete_regressors = "yes"
pipeline.w2w_mat_file = args.matfile
pipeline.nb_wm_covars = 3
pipeline.nb_csf_covars = 6
# erosion of anatomical masks before resampling
pipeline.erode_path_nb_wm = 3
pipeline.erode_path_nb_csf = 1

# not used in imagen
# the mask (constant reference variable)
# explicit spm_mudefault:mask= 0.05 used
pipeline.mask_image = args.maskimage

# the smoothing kernel size
pipeline.fwhm = [5, 5, 5]

# the nifti of the session to process
pipeline.fmri_sessions = [fmri_session_unizp]

# the corresponding behavioural data
pipeline.behavioral_data = [onset_file]
# spm variable names
pipeline.condition_name = "Conditions"
pipeline.onset_name = "Onsets"
pipeline.duration_name = "Durations"

# starting volume
pipeline.start = 0
# filter cutoff
pipeline.high_pass_filter_cutoff = 128
# design model parameters for hrf function
pipeline.bases = {'hrf': {'derivs': [0, 0]}}
# onset behavioural file delimiter
pipeline.delimiter = ";"
pipeline.concatenate_runs = True

# freesurfer directory
pipeline.fsdir = args.fsdir

# subject indentifier
pipeline.sid = args.sid

#
# now run pipeline
#
study_config.run(pipeline, verbose=0)
######  ?? pipeline.delimiter = ";"

# Keep only data of interest
# .m files
mfiles = glob.glob(os.path.join(capsulwd, "*", "pyscript*.m"))
for mfile in mfiles:
    shutil.copy(mfile, soutdir)
# reg file
regfile = os.path.join(capsulwd, "9-covars", "complete_reg_file.txt")
shutil.copy(regfile, os.path.join(soutdir, "rp_nuisance_extended.txt"))
# EstimateModel niftis
estimate_model_dir = os.path.join(capsulwd, "13-EstimateModel")
images = [os.path.join(estimate_model_dir, fname)
          for fname in ("mask.nii", "RPV.nii", "ResMS.nii")]
for image in images:
    gzip_file(image, prefix="", output_directory=soutdir,
              remove_original_file=False)
# betas
betas = glob.glob(os.path.join(estimate_model_dir, "beta*.nii"))
with tarfile.open(os.path.join(soutdir, "beta_files.tar.gz"), 'w:gz') as f:
    for beta in betas:
        f.add(beta, arcname=os.path.basename(beta))
# SPM.mat
spmmatfile = os.path.join(capsulwd, "14-EstimateContrast", "SPM.mat")
gzip_file(spmmatfile, prefix="", output_directory=soutdir,
          remove_original_file=False)
# nii_spmF_images_dir niftis
nii_spmF_images_dir = os.path.join(capsulwd, "15-nii_spmF_images")
nii_spmF_images_files = []
nii_spmF_images_files += [filepath for filepath in glob.glob(
    os.path.join(nii_spmF_images_dir, "con*")) if not any(
        substr in os.path.basename(filepath).lower()
        for substr in ("_faces_", "realign"))]
nii_spmF_images_files += [filepath for filepath in
                          glob.glob(os.path.join(nii_spmF_images_dir, "ess*"))]
nii_spmF_images_files += [filepath for filepath in
                          glob.glob(os.path.join(nii_spmF_images_dir, "spmT*"))
                          if "realign" not in os.path.basename(filepath).lower()]
nii_spmF_images_files += [filepath for filepath in
                          glob.glob(os.path.join(nii_spmF_images_dir, "spmF*"))]
for filepath in nii_spmF_images_files:
    shutil.copy(filepath, soutdir)
# erase capsul dear
shutil.rmtree(capsulwd)
