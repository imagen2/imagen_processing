#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import subprocess
import os
import multiprocessing
import itertools


# We need to insert common data apriori in order to run this procedure

# Global parameters
data_path = "/neurospin/imagen/export/"
db_name = "imagen"
login = "admin"
password = "alpine"


def job(iteration, db_name, login, password):
    """ The core job.
    """
    cmd = ["python", "import_imagen_xnat_multi.py",
           os.path.join(data_path, "xml_2014_04_08_part{0}.txt".format(iteration +1)),
           db_name, login, password]
    print iteration, ": ", cmd
    subprocess.check_call(cmd)    


def _job(params):
	"""Convert `f([1,2])` to `f(1,2)` call.
    """
	job(*params)


# Create a group of CPUs to run on
pool = multiprocessing.Pool()
params = [a for a in itertools.izip(range(6),
                itertools.repeat(db_name),itertools.repeat(login),
                itertools.repeat(password))]
pool.map(_job, params)




