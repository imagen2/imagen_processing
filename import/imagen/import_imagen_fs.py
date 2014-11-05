#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Cmd line example:
# >>> python import_imagen_fs.py /neurospin/imagen imagen admin alpine

# System import
import os
import sys
import getopt
import datetime
import logging

# CubicWeb import
from cubicweb import cwconfig
from cubicweb.dbapi import in_memory_repo_cnx

# Bioresource import
from imagen_fs import FsConverter
from imagen_fs_parser import eval_fs_path

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

# Help to generate the command line
def usage():
    sys.stderr.write("Usage: {0} path_to_the_data "
                     "db_name login password \n\n".format(
                         script_name))


# Get the script name
script_name = os.path.basename(sys.argv[0])

# Parse command line arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "h:", ["help"])
except getopt.GetoptError:
    usage()
    sys.exit(2)

# If the help option is passed return the usage recommandations
for o, a in opts:
    if o in ["-h", "--help"]:
        usage()
        sys.exit()

# Check input arguments
if len(args) < 4:
    sys.stderr.write("{0}: missing arguments\n".format(script_name))
    sys.stderr.write("Try {0} --help for more information.\n".format(
        script_name))
    sys.exit(2)
elif len(args) > 4:
    sys.stderr.write("{0}: : too many arguments\n".format(script_name))
    sys.stderr.write("Try {0} --help for more information.\n".format(
        script_name))
    sys.exit(2)
if not os.path.isdir(args[0]):
    sys.stderr.write("{0}: : a directory argument is expected\n".format(
        script_name))

# Set logging level
logging.basicConfig(level=logging.DEBUG)

# Get the path to the data
processed_root = os.path.join(args[0], "FU2", "processed_raw_tmp", "processed")
psytools_root = os.path.join(args[0], "RAW", "PSC2", "psytools")
dawba_root = os.path.join(args[0], "RAW", "PSC2", "dawba")
nifti, psytools, dawba = eval_fs_path(processed_root, psytools_root, dawba_root)

# CW authentification
db_name = args[1]
login = args[2]
password = args[3]

# Create cw store (need to be executed in a cubicweb shell)
config = cwconfig.instance_configuration(db_name)
repo, cnx = in_memory_repo_cnx(config, login=login, password=password)
session = repo._get_session(cnx.sessionid)

# Create an object to import the meta data to the db
db_importer = FsConverter(session,
                            massive_importation=False,
                            inline_relations_in_schema=True)

# Start the insertion
# This step is long: start a timer
start_time = datetime.datetime.now()
nb_of_data_to_treat = len(nifti)
for cnt, nifti in enumerate(nifti.iteritems()):
    patient_name, patient_scans = nifti
    rset = session.execute("Any N Where S is Subject, S code_in_study '{0}', "
                           "S concerned_by A, X holds A, X name N".format(patient_name))
    patient_structure = {
        'Device': {
            'model': 'unknown',
            'name': 'unknown',
            'manufacturer': 'unknown'}, 
        'Study': {
            'data_filepath': 'unknown',
            'name': 'IMAGEN'}, 
        'Center': {
            'city': 'unknown',
            'identifier': '-1',
            'name': 'unknown'},
        'Subject': {
            'code_in_study': patient_name,
            'gender': 'unknown',
            'identifier': 'IMAGEN_{0}'.format(patient_name),
            'handedness': 'unknown'}
    }
    if rset.rowcount > 0:
        patient_structure["Center"]["name"] = rset[0][0]
        patient_structure["Center"]["city"] = rset[0][0]
        patient_structure["Center"]["identifier"] = str(center_map[rset[0][0]])
    patient_questionnaires = []
    if patient_name in dawba:
        patient_questionnaires.extend(dawba[patient_name])
    if patient_name in psytools:
        patient_questionnaires.extend(psytools[patient_name])
    ratio = float(cnt + 1) / float(nb_of_data_to_treat)
    db_importer._progress_bar(
        ratio, title="Processed NIFTI '{0}'".format(patient_name))
    db_importer.parse(patient_structure, patient_questionnaires, patient_scans)
    db_importer.import_in_db()

# Stop the timer
now_time = datetime.datetime.now()
delta_time = now_time - start_time
print "\nDone in {0} seconds.".format(delta_time)

# Cleanup the cache
db_importer.cleanup()
