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
import glob
import os
import pandas
import numpy as np
import shutil
import argparse
import gzip
import tarfile

# CAPSUL import
from capsul.study_config import StudyConfig
from capsul.api import get_process_instance

# Mmutils import
from mmutils.adapters.io import gzip_file


def generate_onsets(behav_file, timepoint, out_dir):
    """Convert the csv in onset format
    Update the path names from csv to onset
    Update the path with value None if the csv file is void
    """
    def milisec_to_sec(a):
        return float(a.replace('"', ''))/1000.

    if timepoint == "BL":
        timepoint_nb = 19
    elif timepoint == "FU2":
        timepoint_nb = 24
    else:
        raise Exception

    warn_flag = False
    log = ""
    # print "DBG> fixing ",  data_onsets_name
    data_onsets = pandas.read_csv(behav_file, skiprows=2,
                                  quoting=3,
                                  header=None,
                                  sep='\t',
                                  index_col=False,
                                  names=['Onsets', 'Conditions'],
                                  converters={0: milisec_to_sec,
                                              1: str},)

    if data_onsets.shape[0] == 0:
        log += "ERROR: no stimulis found !\n"
        return log, None

    data_onsets['Conditions'] = [(i.split('\\')[-1]).split('.')[0]
                                 for i in data_onsets[
                                     'Conditions']]
    data_onsets.insert(loc=len(data_onsets.columns),
                       column='Durations',
                       value=18)
    # check if we have 20 stimulis in BL, 25 in FU2. Cleanup
    # the file in case of reset
    ref = 0
    onsets = []
    durations = []
    conditions = []
    for index, time in enumerate(data_onsets["Onsets"]):
        if time < ref:
            log += "\n\tWARNING: reset detected condition in stimulis !"
            warn_flag = True
            onsets = [time, ]
            durations = [18, ]
            conditions = [data_onsets['Conditions'][index], ]
        else:
            onsets.append(time)
            durations.append(18)
            conditions.append(data_onsets['Conditions'][index])
        ref = time

    if len(onsets) != timepoint_nb:
        log = ("ERROR: wrong number of stimulis: {} instead "
               "of {}\n".format(len(onsets), timepoint_nb))
        return log, None

    data_onsets = pandas.DataFrame(index=np.arange(len(onsets)),
                                   columns=['Conditions',
                                            'Onsets',
                                            'Durations'])
    data_onsets["Onsets"] = onsets
    data_onsets['Conditions'] = conditions
    data_onsets['Durations'] = durations

    outfile = os.path.join(out_dir,
                           "onset.txt")
    data_onsets.to_csv(outfile, index=None, sep=';',
                       columns=['Conditions',
                                'Onsets',
                                'Durations'])

    if warn_flag:
        log = "Warning in behavioural file parsing\n"
    else:
        log = ""

    return log, outfile


def set_pipeline_contrasts(timepoint):
    if timepoint == "FU2":
        #shadow T contrast to define the Fcontrasts
        shadow_contrastsT_EI = [('control', 'T', ['control'], [1.0]),
                       ('faces_a1', 'T', ['faces_a1'], [1.0]),
                       ('faces_a2', 'T', ['faces_a2'], [1.0]),
                       ('faces_a3', 'T', ['faces_a3'], [1.0]),
                       ('faces_a4', 'T', ['faces_a4'], [1.0]),
                       ('faces_n1', 'T', ['faces_n1'], [1.0]),
                       ('faces_n2', 'T', ['faces_n2'], [1.0]),
                       ('faces_n3', 'T', ['faces_n3'], [1.0]),
                       ('faces_n4', 'T', ['faces_n4'], [1.0]),
                       ('faces_h1', 'T', ['faces_h1'], [1.0]),
                       ('faces_h2', 'T', ['faces_h2'], [1.0]),
                       ('faces_h3', 'T', ['faces_h3'], [1.0]),
                       ('faces_h5', 'T', ['faces_h5'], [1.0]),
                    ]
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
        contrastsT = [
            # already in the Effect of Interest contrast list
            #("control", "T", ['control', ], [1., ]),
            ("angry", "T",
             ['faces_a1', 'faces_a2', 'faces_a3', 'faces_a4', ],
             [.25, .25, .25, .25, ]),
            ("neutral", "T",
             ['faces_n1', 'faces_n2', 'faces_n3', 'faces_n4', ],
             [.25, .25, .25, .25, ]),
            ("happy", "T",
             ['faces_h1', 'faces_h2', 'faces_h3', 'faces_h5', ],
             [.25, .25, .25, .25, ]),
            ("control - neutral", "T",
             ['faces_n1', 'faces_n2', 'faces_n3', 'faces_n4', 'control'],
             [-.25, -.25, -.25, -.25, 1.]),
            ("neutral - control", "T",
             ['faces_n1', 'faces_n2', 'faces_n3', 'faces_n4', 'control'],
             [.25, .25, .25, .25, -1.]),
            ("control - angry", "T",
             ['faces_a1', 'faces_a2', 'faces_a3', 'faces_a4', 'control'],
             [-.25, -.25, -.25, -.25, 1.]),
            ("angry - control", "T",
             ['faces_a1', 'faces_a2', 'faces_a3', 'faces_a4', 'control'],
             [.25, .25, .25, .25, -1.]),
            ("control - happy", "T",
             ['faces_h1', 'faces_h2', 'faces_h3', 'faces_h5', 'control'],
             [-.25, -.25, -.25, -.25, 1.]),
            ("happy - control", "T",
             ['faces_h1', 'faces_h2', 'faces_h3', 'faces_h5', 'control'],
             [.25, .25, .25, .25, -1.]),
            ("angry - neutral", "T",
             ['faces_a1', 'faces_a2', 'faces_a3', 'faces_a4', 'faces_n1',
              'faces_n2', 'faces_n3', 'faces_n4'],
             [.25, .25, .25, .25, -.25, -.25, -.25, -.25, ]),
            ("neutral - angry", "T",
             ['faces_a1', 'faces_a2', 'faces_a3', 'faces_a4', 'faces_n1',
              'faces_n2', 'faces_n3', 'faces_n4'],
             [-.25, -.25, -.25, -.25, .25, .25, .25, .25, ]),
            ("happy - neutral", "T",
             ['faces_h1', 'faces_h2', 'faces_h3', 'faces_h5', 'faces_n1',
              'faces_n2', 'faces_n3', 'faces_n4'],
             [.25, .25, .25, .25, -.25, -.25, -.25, -.25, ]),
            ("neutral - happy", "T",
             ['faces_h1', 'faces_h2', 'faces_h3', 'faces_h5', 'faces_n1',
              'faces_n2', 'faces_n3', 'faces_n4'],
             [-.25, -.25, -.25, -.25, .25, .25, .25, .25, ]),
            ("angry+neutral - control", "T",
             ['faces_a1', 'faces_a2', 'faces_a3', 'faces_a4', 'faces_n1',
              'faces_n2', 'faces_n3', 'faces_n4', 'control'],
             [.125, .125, .125, .125, .125, .125, .125, .125, -1.]),
            ("control - angry+neutral", "T",
             ['faces_a1', 'faces_a2', 'faces_a3', 'faces_a4', 'faces_n1',
              'faces_n2', 'faces_n3', 'faces_n4', 'control'],
             [-.125, -.125, -.125, -.125, -.125, -.125, -.125, -.125, 1.]),
            ] + shadow_contrastsT_EI + shadow_contrastsT_RP + shadow_contrastsT_Comp


        # renamming for the sake of readibility
        # contrastsF contains the list of individual F contrast's
        contrastF_EI = shadow_contrastsT_EI
        contrastF_RP = shadow_contrastsT_RP
        contrastF_Comp = shadow_contrastsT_Comp
        constrastsF = [
                        ['Effects of interest', 'F', contrastF_EI],
                        ['Effects of rp', 'F', contrastF_RP],
                        ['Effects of compcorr', 'F', contrastF_Comp],
                    ]

        # All  type of contrasts are gathered
        contrasts = contrastsT + constrastsF
        return contrasts

    elif timepoint == "BL":
        #shadow T contrast to define the Fcontrasts
        shadow_contrastsT_EI = [('control', 'T', ['control'], [1.0]),
                       ('faces_a1', 'T', ['faces_a1'], [1.0]),
                       ('faces_a2', 'T', ['faces_a2'], [1.0]),
                       ('faces_a3', 'T', ['faces_a3'], [1.0]),
                       ('faces_a4', 'T', ['faces_a4'], [1.0]),
                       ('faces_a5', 'T', ['faces_a5'], [1.0]),
                       ('faces_n1', 'T', ['faces_n1'], [1.0]),
                       ('faces_n2', 'T', ['faces_n2'], [1.0]),
                       ('faces_n3', 'T', ['faces_n3'], [1.0]),
                       ('faces_n4', 'T', ['faces_n4'], [1.0]),
                       ('faces_n5', 'T', ['faces_n5'], [1.0]),
                    ]
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
        contrastsT = [
            # already in the Effect of Interest contrast list
            # ("control", "T", ['control', ], [1, ]),
            ("angry", "T", ['faces_a1', 'faces_a2', 'faces_a3', 'faces_a4',
                            'faces_a5', ],
             [.2, .2, .2, .2, .2, ]),
            ("neutral", "T", ['faces_n1', 'faces_n2', 'faces_n3', 'faces_n4',
                              'faces_n5', ],
             [.2, .2, .2, .2, .2, ]),
            ("control - neutral", "T", ['faces_n1', 'faces_n2', 'faces_n3',
                                        'faces_n4', 'faces_n5', 'control'],
             [-0.2, -0.2, -0.2, -0.2, -0.2, 1]),
            ("neutral - control", "T", ['faces_n1', 'faces_n2', 'faces_n3',
                                        'faces_n4', 'faces_n5', 'control'],
             [0.2, 0.2, 0.2, 0.2, 0.2, -1]),
            ("control - angry", "T", ['faces_a1', 'faces_a2', 'faces_a3',
                                      'faces_a4', 'faces_a5', 'control'],
             [-0.2, -0.2, -0.2, -0.2, -0.2, 1]),
            ("angry - control", "T", ['faces_a1', 'faces_a2', 'faces_a3',
                                      'faces_a4', 'faces_a5', 'control'],
             [0.2, 0.2, 0.2, 0.2, 0.2, -1]),
            ("angry - neutral", "T", ['faces_a1', 'faces_a2', 'faces_a3',
                                      'faces_a4', 'faces_a5', 'faces_n1',
                                      'faces_n2', 'faces_n3', 'faces_n4',
                                      'faces_n5'],
             [.2, .2, .2, .2, .2, -0.2, -0.2, -0.2, -0.2, -0.2]),
            ("neutral - angry", "T", ['faces_a1', 'faces_a2', 'faces_a3',
                                      'faces_a4', 'faces_a5', 'faces_n1',
                                      'faces_n2', 'faces_n3', 'faces_n4',
                                      'faces_n5'],
             [-0.2, -0.2, -0.2, -0.2, -0.2, .2, .2, .2, .2, .2, ]),
            ("angry+neutral - control", "T", ['faces_a1', 'faces_a2',
                                              'faces_a3', 'faces_a4',
                                              'faces_a5', 'faces_n1',
                                              'faces_n2', 'faces_n3',
                                              'faces_n4', 'faces_n5',
                                              'control'],
             [.1, .1, .1, .1, .1, .1, .1, .1, .1, .1, -1]),
            ("control - angry+neutral", "T", ['faces_a1', 'faces_a2',
                                              'faces_a3', 'faces_a4',
                                              'faces_a5', 'faces_n1',
                                              'faces_n2', 'faces_n3',
                                              'faces_n4', 'faces_n5',
                                              'control'],
             [-.1, -.1, -.1, -.1, -.1, -.1, -.1, -.1, -.1, -.1, 1]),
            ] + shadow_contrastsT_EI + shadow_contrastsT_RP + shadow_contrastsT_Comp

        # renamming for the sake of readibility
        # contrastsF contains the list of individual F contrast's
        contrastF_EI = shadow_contrastsT_EI
        contrastF_RP = shadow_contrastsT_RP
        contrastF_Comp = shadow_contrastsT_Comp
        constrastsF = [['Effects of interest', 'F', contrastF_EI],
                       ['Effects of rp', 'F', contrastF_RP],
                       ['Effects of compcorr', 'F', contrastF_Comp]]

        # All  type of contrasts are gathered
        contrasts = contrastsT + constrastsF
        return contrasts

    else:
        raise Exception


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
First Level FT

python imagen_first_level_ft.py \
-s 000001441076 \
-t BL \
-i /neurospin/imagen/BL/processed/spm_preprocessing/000001441076/EPI_faces/swau000001441076s002a001.nii.gz \
-f /neurospin/imagen/BL/processed/freesurfer \
-n /neurospin/imagen/BL/processed/spm_new_segment/000001441076/u000001441076000001441076s006a1001_seg8.mat \
-r /neurospin/imagen/BL/processed/spm_preprocessing/000001441076/EPI_faces/rp_au000001441076s002a001.txt \
-b /neurospin/imagen/BL/processed/nifti/000001441076/BehaviouralData/ft_000001441076.csv \
-o /tmp/IMAGEN_TEST_FT
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
    default="/drf/local/spm12",
    help="the spm directory.")
parser.add_argument(
    "-l", "--fslconfig", dest="fslconfig", type=is_file,
    default="/etc/fsl/4.1/fsl.sh",
    help="the FSL configuration file path.")
parser.add_argument(
    "-g", "--fsconfig", dest="fsconfig", type=is_file,
    default="/drf/local/freesurfer/SetUpFreeSurfer.sh",
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
parser.add_argument(
    "-p", "--template", dest="template", type=is_file,
    default="/drf/local/spm12/tpm/TPM.nii",
    help="the template file.")
args = parser.parse_args()


# Create the subject output directory
soutdir = os.path.join(args.outdir, args.sid, "EPI_faces")
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
    use_nipype=True,
    output_directory=capsulwd)
print "    ... done."

# Get the pipeline
pipeline = get_process_instance("clinfmri.statistics.spm_first_level_pipeline.xml")

# unzip nifti file (to be destroyed after)
fmri_session_unizp = os.path.join(capsulwd,
                                  os.path.basename(
                                      args.inputvolume).replace(".gz", ""))

with gzip.open(args.inputvolume, 'rb') as f:
    file_content = f.read()
    with open(fmri_session_unizp, "wb") as _file:
        _file.write(file_content)

# generate onset
log_onset, onset_file = generate_onsets(args.behavfile, args.timepoint,
                                        soutdir)
if not onset_file:
    if args.verbose:
        print "{} - {}".format(args.sid, log_onset)
    # csv file invalid STOP
    raise Exception("{} - {}".format(args.sid, log_onset))

pl_contrast = set_pipeline_contrasts(args.timepoint)

# Configure the pipeline
# FreeSurfer config
pipeline.fsconfig = args.fsconfig
# Smoothing already performed in proproc IMAGEN
pipeline.smoother_switch = "no_smoothing"
# the 6 basic movement regressors are completed with wm, ventricles and
# extra mvt
pipeline.complete_regressors = "yes"
# output directory with all results
#pipeline.output_directory = outdir_worker
# sequence information
pipeline.time_repetition = 2.2
# contrasts we have defined above
pipeline.contrasts = pl_contrast
# the mask (constant reference variable)
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
# world to world transformation matrix
pipeline.w2w_mat_file = args.matfile
# number of extra noise covars to extract
pipeline.nb_csf_covars = 6
pipeline.nb_wm_covars = 3
pipeline.time_repetition = 2.2
#
pipeline.realignment_parameters = args.rpfile
# erosion of anatomical masks before resampling
pipeline.erode_path_nb_wm = 3
pipeline.erode_path_nb_csf = 1
pipeline.template = args.template
#
# now run pipeline
#
study_config.run(pipeline, args.verbose)

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
