#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2011-2015 CEA
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

"""
Script to run the SPM preprocessing on one fMRI data of the Imagen project.
Meant to be usable with Hopla.

Call example with random subject id and in/out paths:

python imagen_spm_preprocessing.py \
-f /neurospin/imagen/BL/processed/nifti/000000106871/SessionA/EPI_faces/000000106871s004a001.nii.gz  \
-i 000000106871 \
-p EPI_faces \
-o /tmp/IMAGEN_TEST_PREPROC \
-r 2.2 \
-e 40 \
-d 40 39 38 37 36 35 34 33 32 31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 \
-t /neurospin/imagen/workspace/fmri/scripts/ImagenEPI200_3mm.nii \
-c spm \
-n fmri \
-s /neurospin/imagen/workspace/spm/spm12-iteration6 \
-g /etc/fsl/4.1/fsl.sh

"""

import os
import tempfile
import shutil
import argparse

# CAPSUL import
from capsul.study_config import StudyConfig
from capsul.api import get_process_instance

from mmutils.adapters.io import gzip_file

###############################################################################

def create_tmp_dir(rootdir, prefix="tmp_spmpreproc_"):
    """
    Create a tmp dir in rootdir.
    """
    tmp_dir = tempfile.mkdtemp(dir=rootdir, prefix=prefix)
    return tmp_dir


def is_file(filepath):
    """ Type for argparse - check file existence.
    """
    if not os.path.isfile(filepath):
        raise argparse.ArgumentError("File does not exist: %s" % filepath)
    return filepath


def get_cmd_line_args():
    """
    Create a command line argument parser, run it and return a dict mapping
    <argument name> -> <argument value>.
    """
    usage = ("%(prog)s -f <funcfile> -i <subject id> -p <paradigm> "
             "-o <outdir> -s <spm bin>")
    parser = argparse.ArgumentParser(prog="python spm_preprocessing.py",
                                     usage=usage)

    parser.add_argument("-f", "--funcfile",
                        required=True,
                        type=is_file,
                        metavar="<funcfile>",
                        help="Path to fMRI Nifti.")
    parser.add_argument("-i", "--sid",
                        required=True,
                        metavar="<subject id>")
    parser.add_argument("-p", "--paradigm",
                        required=True,
                        metavar="<paradigm>")
    parser.add_argument("-o", "--outdir",
                        required=True,
                        metavar="<outdir>")
    parser.add_argument("-r", "--repetition-time",
                        type=float,
                        required=True,
                        metavar="<repetition time>")
    parser.add_argument("-e", "--ref-slice",
                        type=int,
                        required=True,
                        metavar="<ref slice>")
    parser.add_argument("-d", "--slice-order",
                        type=int,
                        nargs="+",
                        required=True,
                        metavar="<slice order>")
    parser.add_argument("-t", "--template",
                        type=is_file,
                        required=True,
                        metavar="<path template>")
    parser.add_argument("-c", "--timings-corr-algo",
                        default="spm",
                        metavar="<timings corr algo>")
    parser.add_argument("-n", "--normalization",
                        default="fmri",
                        metavar="<normalization>")
    parser.add_argument("-s", "--spm-bin",
                        type=is_file,
                        metavar="<spm bin>")
    parser.add_argument("-g", "--fsl-config",
                        type=is_file,
                        metavar="<fsl config>")
    args = parser.parse_args()
    kwargs = vars(args)

    return kwargs


def run_spm_preprocessing(funcfile, outdir, repetition_time, ref_slice,
                          slice_order, template, timings_corr_algo,
                          normalization, spm_bin, fsl_config,
                          enable_display=False):
    """
    """
    print "Study_config init..."
    study_config = StudyConfig(
        modules=["MatlabConfig", "SPMConfig", "FSLConfig", "NipypeConfig"],
        use_smart_caching=False,
        fsl_config=fsl_config,
        use_fsl=True,
        use_matlab=False,
        use_spm=True,
        spm_exec=spm_bin,
        spm_standalone=True,
        use_nipype=True,
        output_directory=outdir,
        )
    print "    ... done."

    # Processing definition: create the <clinfmri.preproc.FmriPreproc> that
    # define the different step of the processings.
    pipeline = get_process_instance("clinfmri.preproc.converted_fmri_preproc.xml")

    # It is possible to display the pipeline.
    if enable_display:
        import sys
        from PySide import QtGui
        from capsul.qt_gui.widgets import PipelineDevelopperView

        app = QtGui.QApplication(sys.argv)
        view = PipelineDevelopperView(pipeline)
        view.show()
        app.exec_()

    # Now to parametrize the pipeline pipeline.
    pipeline.fmri_file = funcfile
    pipeline.realign_register_to_mean = True
    pipeline.select_slicer = timings_corr_algo
    pipeline.select_normalization = normalization
    pipeline.force_repetition_time = repetition_time
    pipeline.force_slice_orders = slice_order
    pipeline.realign_wrap = [0, 1, 0]
    pipeline.realign_write_wrap = [0, 1, 0]
    pipeline.ref_slice = ref_slice
    if template is not None:
        pipeline.template_file = template

    # The pipeline is now ready to be executed.
    study_config.run(pipeline, executer_qc_nodes=False, verbose=1)


def reorganize_preproc_files(outdir, sid, proto, image_basename, tmp_capsul,
                             overwrite=False):
    """
    Perform the tree reorganization
    """
    #describe reorganization
    processing_struct = {
        "1-BET": [
            "{}_brain_mask.nii.gz",
            "{}_brain.nii.gz"],
        "5-SliceTiming": [
            "au{}.nii",
            "pyscript_slicetiming.m"],
        "6-Realign": [
            "rp_au{}.txt",
            "rau{}.nii",
            "pyscript_realign.m",
            "meanau{}.nii",
            "au{}.mat"],
        "8-Normalize": [
            "wmeanau{}.nii",
            "pyscript_normalize.m",
            "meanau{}_sn.mat"],
        "9-Normalize": [
            "wau{}.nii",
            ["pyscript_normalize.m", "pyscript_apply_normalize.m"]],
        "10-Smooth": [
            "pyscript_smooth.m",
            "swau{}.nii"]
    }

    # clean target entry
    gzdestpath = os.path.join(outdir, sid, proto)
    if os.path.exists(gzdestpath):
        if overwrite:
            shutil.rmtree(gzdestpath)
        else:
            raise Exception("Directory already exists: %s" % gzdestpath)

    os.makedirs(gzdestpath)

    # loop on items
    for step_name, step_fnames in processing_struct.items():
        for base in step_fnames:
            if type(base) == list:
                basename = base[0]
                rename = base[1]
            else:
                basename = base
                rename = base
            basename = basename.format(image_basename)
            rename = rename.format(image_basename)
            srcpath = os.path.join(tmp_capsul, step_name, basename)
            if srcpath.endswith(".nii"):
                gzip_file(srcpath, prefix="", output_directory=gzdestpath)
                print "****gzip ", srcpath, gzdestpath
            else:
                destpath = os.path.join(gzdestpath, rename)
                print "****mv ", srcpath, destpath
                if os.path.exists(srcpath):
                    shutil.move(srcpath, destpath)
    print "rm ", tmp_capsul
    shutil.rmtree(tmp_capsul)


###############################################################################
# SCRIPT STARTS HERE

# Get command line arguments
kwargs = get_cmd_line_args()

# Take out the keys that run_spm_preprocessing() does not need
subject_id = kwargs.pop("sid")
paradigm = kwargs.pop("paradigm")
outdir = kwargs.pop("outdir")

# Create a temporary dir where to run capsul
if not os.path.isdir(outdir):
    os.mkdir(outdir)
tmp_capsul = create_tmp_dir(outdir)

# Run the preprocessing in the temporary dir
run_spm_preprocessing(outdir=tmp_capsul, **kwargs)

# Reorganize data
image_name = os.path.basename(kwargs["funcfile"]).split(".")[0]
reorganize_preproc_files(outdir, subject_id, paradigm, image_name, tmp_capsul)
