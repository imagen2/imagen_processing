#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

""" Script to parse cantab questionnaires data.

Usage :

'>>> python imagen_cantab_parser.py'

When an error is found on a subject, its data is discarded and the error is
put in the log file
Error log, output json results file and subjects json file are produced in the
script directory.

Please refer to https://bioproj.extra.cea.fr/redmine/projects/imagen/wiki/Cantab
and https://bioproj.extra.cea.fr/redmine/projects/imagen/wiki/Indexation_Cantab
for information about cantab indexation.
"""

# System imports
import os
import csv
import glob
import json
import logging
import datetime


# Initialised the dict for errors collection
errors = {}
# Function to store parsing errors in a dict
def store_error(original_file, error_msg):
    errors.setdefault(original_file, []).append(error_msg)

# Grab the current date and define error log and output result names
dt = str(datetime.datetime.now())
date_prefix = dt.replace(' ', '_')
logname = date_prefix + '_cantab_parser_errors.log'
output_questionnaires_name = date_prefix + '_cantab_results.json'
output_qsubjects_name = date_prefix + '_cantab_subjects.json'
script_location = os.path.realpath(__file__)
scripts_root, script_basename = os.path.split(script_location)
log_file = os.path.join(scripts_root, logname)
output_questionnaires_file = os.path.join(scripts_root, output_questionnaires_name)
output_qsubjects_file = os.path.join(scripts_root, output_qsubjects_name)

# Create a logger to error file
logging.basicConfig(filename=log_file, level=logging.DEBUG)

# Global variables and data path
qname = "cantab"
project_name = "IMAGEN"
timepoints = ['BL', 'FU2']
questionnaires_roots = {'BL': "/neurospin/imagen/BL/processed/nifti/*/"
                              "BehaviouralData/datasheet_*.csv",
                        'FU2': "/neurospin/imagen/FU2/processed/nifti/*/"
                               "BehaviouralData/datasheet_*.csv"}

# Specify the wanted columns according to the imagen documentation
selected_cols = ["RVP A'",
                 "SWM Between errors",
                 "SWM Strategy",
                 "AGN Mean correct latency (positive)",
                 "AGN Mean correct latency (negative)",
                 "AGN Mean correct latency (neutral)",
                 "AGN Total omissions (positive)",
                 "AGN Total omissions (negative)",
                 "AGN Total omissions (neutral)",
                 "CGT Delay aversion",
                 "CGT Deliberation time",
                 "CGT Overall proportion bet",
                 "CGT Quality of decision making",
                 "CGT Risk adjustment",
                 "CGT Risk taking"]

# Initialize the final results structure
questionnaires = {}

# Initialize temporary result structure
questionnaires_tmp = {}

# Total numbers of csv by timepoint
total_csv_number = {}

# Go through all timepoints
for timepoint in timepoints:

    questionnaires_tmp[timepoint] = {}

    datasheet_csv_files_path = glob.glob(questionnaires_roots[timepoint])
    # Total number of csv found
    total_csv_number[timepoint] = len(datasheet_csv_files_path)

    # Go through all datasheet csv
    for file_path in datasheet_csv_files_path:

        folders = file_path.split(os.sep)
        # Get the real subject ID from the parent folder name
        subject_id = folders[-3]
        # Check if ID is valid
        if subject_id.isdigit():

            file_name = folders[-1]
            # Check if csv file name is valid
            if file_name == ("datasheet_" + subject_id + ".csv"):
                # Open csv
                with open(file_path, 'rb') as f:
                    rows = [row for row in csv.reader(f)]
                    # Check if the number of rows is 2
                    if len(rows) == 2:
                        row_subject_id = rows[1][0]
                        # Check if folder name and row ID correspond
                        if subject_id == row_subject_id:

                            subject_age = rows[1][1]
                            # Check if subject age is valid
                            if subject_age.isdigit():

                                if 0 < int(subject_age) < 120:
                                    # Check that the subject has not been treated yet
                                    if subject_id not in \
                                            questionnaires_tmp[timepoint]:

                                        headers = rows[0]
                                        # Check if there are not duplicated questions in csv
                                        if len(headers) > len(set(headers)):
                                            store_error(file_path,
                                                        "One or more duplicated "
                                                        "questions")
                                        # Check that the wanted questions are in csv
                                        if set(selected_cols).issubset(set(headers)):

                                            selected_cols_nb = []
                                            for index, header in enumerate(headers):
                                                if header in selected_cols:
                                                    selected_cols_nb.append(index)

                                            answers = rows[1]

                                            not_empty = 0
                                            for answer in answers:
                                                if len(answer) > 0:
                                                    not_empty += 1

                                            # Check that answer row is not empty
                                            if not_empty:

                                                questionnaires_tmp[timepoint][subject_id] = {}

                                                for index, answer in \
                                                        enumerate(answers):

                                                    # Get only the wanted questions
                                                    if index in selected_cols_nb:
                                                        # Refactor the question
                                                        # according to xnat guidelines
                                                        question = headers[index]\
                                                            .lower()\
                                                            .replace('\'', '')\
                                                            .replace('(', '')\
                                                            .replace(')', '')\
                                                            .replace(' ', '_')
                                                        question = u"{0}".format(question)

                                                        questionnaires_tmp[timepoint][subject_id][question] = u"{0}".format(answer)

                                                questionnaires_tmp[timepoint][subject_id][u"age"] = u"{0}".format(subject_age)

                                            else:
                                                store_error(file_path,
                                                            "Empty answers row")
                                        else:
                                            store_error(file_path,
                                                        "Some required "
                                                        "columns are missing")
                                    else:
                                        store_error(file_path, "Subject has already"
                                                               " been treated")
                                else:
                                    store_error(file_path, "Unexpected subject age "
                                                           "(not between 0 and 120)")
                            else:
                                store_error(file_path, "Subject age is not a digit")
                        else:
                            store_error(file_path, "Parent folder name do not "
                                                   "match csv name on Subject ID")
                    else:
                        store_error(file_path, "The number of rows is not 2")
            else:
                store_error(file_path, "CSV name is not valid")
        else:
            store_error(file_path, "Parent folder is not a digit")

# Initialize subject container
qsubjects = {}

# Put results in the final structure to be compliant with insertion scripts
for timepoint, subjects_data in questionnaires_tmp.iteritems():

    # Initialize subjects set for this timepoint
    qsubjects_tmp = set()

    for subject_id, subject_questions_answers in subjects_data.iteritems():

        subject_age = subject_questions_answers[u"age"]
        del subject_questions_answers[u"age"]

        # Define assessment ID
        assessment_id = u"{0}_{1}_{2}_{3}".format(project_name, timepoint,
                                                  qname, subject_id)
        # Create assessment structure
        assessment_struct = {
            "identifier": assessment_id,
            "age_of_subject": subject_age,
            "timepoint": unicode(timepoint)
        }

        # Build the subject questionnaires structure for this timepoint
        subj_questionnaires = {
            "Questionnaires": {},
            "Assessment": assessment_struct
        }

        # Fill the questionnaire structure
        subj_questionnaires["Questionnaires"][qname] = subject_questions_answers

        # Add this questionnaire to the patien data
        questionnaires.setdefault(subject_id, []).append(subj_questionnaires)

        # Add subject to subjects set
        qsubjects_tmp.add(subject_id)

    qsubjects[timepoint] = qsubjects_tmp

for timepoint in timepoints:
    logging.info(" Timepoint : {0} : {1} csv read, {2} were valid."
                 .format(timepoint, total_csv_number[timepoint],
                         len(qsubjects[timepoint])))

# Write errors to file
logging.info("********************** ERRORS **********************")
for origin_file, file_errors in errors.iteritems():
    logging.warning(" {0} : {1}".format(origin_file, json.dumps(file_errors)))

# Write questionnaires to output file
with open(output_questionnaires_file, 'w') as f:
    json.dump(questionnaires, f)

# Write subjects to output files
all_subjects = set()
for timepoint in timepoints:
    all_subjects = all_subjects.union(qsubjects[timepoint])
with open(output_qsubjects_file, 'w') as f:
    json.dump(list(all_subjects), f)

# Visual integrity check
print json.dumps(questionnaires, indent=4)