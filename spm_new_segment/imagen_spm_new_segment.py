#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 CEA
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
import os
import glob
import shutil
import argparse

# Mmutils import
from mmutils.adapters.io import gzip_file

# CAPSUL import
from capsul.study_config import StudyConfig
from capsul.api import get_process_instance


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

doc = """
SPM structural normalization to template.

python imagen_spm_new_segment.py \
-s 000000106871 \
-a /neurospin/imagen/BL/processed/nifti/000000106871/SessionA/ADNI_MPRAGE/000000106871s008a1001.nii.gz \
-o /tmp/IMAGEN_TEST_NEW_SEGMENT \
-e

"""
parser = argparse.ArgumentParser(description=doc)
parser.add_argument(
    "-s", "--sid", dest="sid", type=str, required=True,
    help="the subject identifier.")
parser.add_argument(
    "-a", "--t1file", dest="t1file", type=is_file, required=True,
    help="the anatomical file to be processed.")
parser.add_argument(
    "-o", "--outdir", dest="outdir", type=str, required=True,
    help="the output directory.")
parser.add_argument(
    "-c", "--spmbin", dest="spmbin", type=is_file,
    default="/neurospin/imagen/workspace/spm/spm12-iteration6",
    help="the spm standalone path.")
parser.add_argument(
    "-d", "--spmdir", dest="spmdir", type=is_directory,
    default="/i2bm/local/spm12-standalone-6472/spm12_mcr/spm12",
    help="the spm standalone directory.")
parser.add_argument(
    "-e", "--erase", dest="erase", action="store_true",
    help="if activated, clean the subject output folder.")
args = parser.parse_args()


# Create the subject output directory
soutdir = os.path.join(args.outdir, args.sid)
capsulwd = os.path.join(soutdir, "capsul")
if args.erase and os.path.isdir(soutdir):
    shutil.rmtree(soutdir)
if not os.path.isdir(capsulwd):
    os.makedirs(capsulwd)

   
# Create the study configuration
print "Study_config init..."
study_config = StudyConfig(
    modules=["MatlabConfig", "SPMConfig", "NipypeConfig"],
    use_smart_caching=False,
    use_matlab=False,
    use_spm=True,
    spm_exec=args.spmbin,
    spm_standalone=True,
    use_nipype=True,
    output_directory=capsulwd)
print "    ... done."

# Get the pipeline
pipeline = get_process_instance("clinfmri.utils.spm_new_segment_only.xml")

# Configure the pipeline
pipeline.channel_files = [args.t1file]
#to find the template TPM.nii from the standalone distrib
pipeline.spm_dir = args.spmdir

# Execute the pipeline
study_config.run(pipeline, verbose=1)

# Keep only data of interest
batch = os.path.join(capsulwd, "3-NewSegment", "pyscript_newsegment.m")
images = glob.glob(os.path.join(capsulwd, "1-ungzipfnames", "*.nii"))
images = [item for item in images
          if not os.path.basename(item).startswith(("u", "iy_"))]
mat = glob.glob(os.path.join(capsulwd, "1-ungzipfnames", "*.mat"))[0]
for path in images:
    gzip_file(path, prefix="", output_directory=soutdir,
              remove_original_file=False)
shutil.copy(mat, soutdir)
shutil.rmtree(capsulwd)

