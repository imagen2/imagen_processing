#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Cmd line example:
# >>> python import_imagen_xnat.py /neurospin/imagen/export/xml-2014-04-08 2 imagen admin alpine

# System import
import os
import sys
import getopt
import datetime

# CubicWeb import
from cubicweb import cwconfig
from cubicweb.dbapi import in_memory_repo_cnx

# Bioresource import
from imagen_xnat import XnatConverter


# Help to generate the command line
def usage():
    sys.stderr.write("Usage: {0} path_to_the_data nb_of_data_to_treat "
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
if len(args) < 5:
    sys.stderr.write("{0}: missing arguments\n".format(script_name))
    sys.stderr.write("Try {0} --help for more information.\n".format(
        script_name))
    sys.exit(2)
elif len(args) > 5:
    sys.stderr.write("{0}: : too many arguments\n".format(script_name))
    sys.stderr.write("Try {0} --help for more information.\n".format(
        script_name))
    sys.exit(2)
if not os.path.isdir(args[0]):
    sys.stderr.write("{0}: : a directory argument is expected\n".format(
        script_name))

# Get the path to the data
xml_files = [os.path.abspath(os.path.join(args[0], fname))
             for fname in os.listdir(args[0]) 
             if fname.endswith(".xml")]
nb_of_data_to_treat = int(args[1])
if nb_of_data_to_treat == 0:
    nb_of_data_to_treat = len(xml_files)

# CW authentification
db_name = args[2]
login = args[3]
password = args[4]

# Create cw store (need to be executed in a cubicweb shell)
config = cwconfig.instance_configuration(db_name)
repo, cnx = in_memory_repo_cnx(config, login=login, password=password)
session = repo._get_session(cnx.sessionid)

# Create an object to import the meta data to the db
db_importer = XnatConverter(session,
                            massive_importation=False,
                            inline_relations_in_schema=True)

# Start the insertion
# This step is long: start a timer
start_time = datetime.datetime.now()
for cnt, xnat_file in enumerate(xml_files[:nb_of_data_to_treat]):
    ratio = float(cnt + 1) / float(nb_of_data_to_treat)
    db_importer._progress_bar(ratio, title=os.path.basename(xnat_file))
    db_importer.parse(xnat_file)
    db_importer.import_in_db()
# Stop the timer
now_time = datetime.datetime.now()
delta_time = now_time - start_time
print "\nDone in {0} seconds.".format(delta_time)

# Cleanup the cache
db_importer.cleanup()
