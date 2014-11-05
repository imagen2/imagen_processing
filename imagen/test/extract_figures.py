#######
# Browse imagen database and store statistics to file
######


"""
python /opt/nsap/imagen/test/extract_figures.py /volatile/test.txt imagen2
"""

# General imports
import sys
import getopt
import os
import time
import logging

# Define logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# Cubicweb imports
from cubes.rql_download.fuse.fuse_mount import get_cw_connection


# Help to generate the command line
def usage():
    sys.stderr.write("Usage: {0} output_file localisation db_name\n\n".format(
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
if len(args) < 2:
    sys.stderr.write("{0}: missing arguments\n".format(script_name))
    sys.stderr.write("Try {0} --help for more information.\n".format(
        script_name))
    sys.exit(2)
elif len(args) > 2:
    sys.stderr.write("{0}: : too many arguments\n".format(script_name))
    sys.stderr.write("Try {0} --help for more information.\n".format(
        script_name))
    sys.exit(2)

# Get cmdline options
project_name = args[0]
file_path = sys.argv[1]
instance_name = sys.argv[2]

# Connection
cw_connection = get_cw_connection(instance_name)
session = cw_connection.session

# Get all subjects
rset = session.execute("Any I WHERE S is Subject, S identifier I")


####### Auxiliary functions

def add_subject(column, center):
    """ Add 1 to the amount of subject for this column (timepoint) and this
    center
    """
    if center in column:
        column[center] += 1
    else:
        column[center] = 1


# init struct
bl_dict = {}
fu2_dict = {}
for cnt, esubject in enumerate(rset):
    
    # Status message
    logger.info("{0}/{1} - {2}".format(cnt, len(rset), esubject[0]))
    
    # Get BL timepoint
    rql_BL = ("Any A WHERE A is Assessment,"
              "A timepoint 'BL',"
              "S concerned_by A, S identifier '{0}'".format(esubject[0]))
    rset_BL = session.execute(rql_BL)
    if len(rset_BL) > 0:
        #Get center
        rql_BL_2 = ("Any N WHERE C is Center,"
                    "C name N,"
                    "C holds A,"
                    "A eid '{0}'".format(rset_BL[0][0]))
        rset_BL_2 = session.execute(rql_BL_2)
        # Fill structure
	if len(rset_BL_2) > 0:
        	add_subject(bl_dict, rset_BL_2[0][0])
	else:
		logger.warning("BL genetic only subject '{0}'".format(esubject[0]))
    else:
        logger.warning("No BL assessment for subject '{0}'".format(esubject[0]))

    # Get FU2 timepoints
    rql_FU2 = ("Any A WHERE A is Assessment,"
               "A timepoint 'FU2',"
               "S concerned_by A, S identifier '{0}'".format(esubject[0]))
    rset_FU2 = session.execute(rql_FU2)
    if len(rset_FU2) > 0:
        #Get center
        rql_FU2_2 = ("Any N WHERE C is Center,"
                     "C name N,"
                     "C holds A,"
                     "A eid '{0}'".format(rset_FU2[0][0]))
        rset_FU2_2 = session.execute(rql_FU2_2)
        # Fill structure
        add_subject(fu2_dict, rset_FU2_2[0][0])
    else:
        logger.warning("No FU2 assessment for subject '{0}'".format(esubject[0]))

# Write dictionaries into a file
# first time ?
if not os.path.isfile(file_path):
    _file = open(file_path, 'w')
    _file.close()

_file = open(file_path, 'a')
line = "{0}-{1} ".format(time.strftime("%x"), time.strftime("%X"))
for center in bl_dict:
    if center in fu2_dict:
        line += "{0}:{1},{2}.".format(center, bl_dict[center], fu2_dict[center])
    else:
        line += "{0}:{1},{2}.".format(center, bl_dict[center], 0)

# Just in case a centre is in FU2 and not in BL
for centre in fu2_dict:
    if centre not in bl_dict:
        line += "{0}:{1},{2}.".format(centre, 0, fu2_dict[centre])
_file.write("{0}\n".format(line))

# Close everything
_file.close()
cw_connection.shutdown()
