# System import
import os
import sys
import getopt

# CubicWeb import
from cubicweb import cwconfig
from cubicweb.dbapi import in_memory_repo_cnx

# Bioresource import
from genetic_measures import GenomicMeasures

""" python genetics_import.py /neurospin/imagen/dataRepos/BLFU1/genetics/dna/processed imagen admin alpine
"""


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

# CW authentification
genetics_folder = args[0]
db_name = args[1]
login = args[2]
password = args[3]

# Create cw store (need to be executed in a cubicweb shell)
config = cwconfig.instance_configuration(db_name)
repo, cnx = in_memory_repo_cnx(config, login=login, password=password)
session = repo._get_session(cnx.sessionid)

# create importer
genetics_importer = GenomicMeasures(project_name=db_name, session=session)

# parse filesystem
genetics_importer.parse_data(genetics_folder)

# import data
genetics_importer.import_genomic_measure()
