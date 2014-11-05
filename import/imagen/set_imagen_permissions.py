#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Cmd line example:
# >>> python set_imagen_permissions.py imagen admin alpine

# System import
import os
import sys
import getopt

# CubicWeb import
from cubicweb import cwconfig
from cubicweb.dbapi import in_memory_repo_cnx

# Imagen import
from imagen_permissions import ImagenPerms

# Help to generate the command line
def usage():
    sys.stderr.write("Usage: {0} db_name login password \n\n".format(
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
if len(args) < 3:
    sys.stderr.write("{0}: missing arguments\n".format(script_name))
    sys.stderr.write("Try {0} --help for more information.\n".format(
        script_name))
    sys.exit(2)
elif len(args) > 3:
    sys.stderr.write("{0}: : too many arguments\n".format(script_name))
    sys.stderr.write("Try {0} --help for more information.\n".format(
        script_name))
    sys.exit(2)

# CW authentification
db_name = args[0]
login = args[1]
password = args[2]

# Create cw store (need to be executed in a cubicweb shell)
config = cwconfig.instance_configuration(db_name)
repo, cnx = in_memory_repo_cnx(config, login=login, password=password)
session = repo._get_session(cnx.sessionid)

# Start the procedure
manager = ImagenPerms(session)
manager.set_permissions()
manager.cleanup()



