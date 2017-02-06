#!/usr/bin/env python

# Copyright (C) 2016  Ilya Veer, Johann Kruschwitz, Lea Waller
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import glob
import shutil


def docopy(s, e, doit=False):
    """
    copy s to e or alternatly write cmd to stdout
    """
    if doit:
        shutil.copyfile(s, e)
    else:
        print "cp {0} {1}".format(s, e)


def domkdir(p, doit=False):
    """
    mkdir or alternatly write cmd to stdout
    """
    if not os.path.exists(p):
        if doit:
            os.mkdir(p)
        else:
            os.mkdir(p)
            print "mkdir {0}".format(p)


def domakedirs(p, doit=False):
    """
    makedirs or alternatly write cmd to stdout
    """
    if not os.path.exists(p):
        if doit:
            os.makedirs(p)
        else:
            os.makedirs(p)
            print "mkdir -p {0}".format(p)

#racines
root_dir = "/neurospin/imagen/FU2/RAW/TO_TREAT/BERLIN"
target_dir = "/neurospin/imagen/iteration_6"
if not os.path.exists(target_dir):
    domkdir(target_dir)

#Effective command or not
doit = True

############### 1ab QC #################################################
#paires emetteurs -> (recepteurs_data, recepteurs_qc)
qc_emits = [os.path.join(root_dir, '1ab_QC/QC_BL/TSNR_images_BL'),
            os.path.join(root_dir, '1ab_QC/QC_FU2/TSNR_images_FU2'), ]
qc_receivs = [
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing_qc'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing_qc')]
preproc_receivs = [
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing')]

for qc_emit, qc_receiv, preproc_receiv in zip(qc_emits, qc_receivs, preproc_receivs):
    domakedirs(qc_receiv)
    if not os.path.exists(preproc_receiv):
        domakedirs(preproc_receiv)
    for root, dirs, files in os.walk(qc_emit):
        #push file png in qc tstd and tsnr dir reorg by subjects
        if 'slicesdir_t' in root:
            pngfiles = glob.glob(os.path.join(root, '0*.png'))
            subjects = [os.path.basename(i).split('_')[0] for i in pngfiles]
            # loop on subjects
            for s, f in zip(subjects, pngfiles):
                t = os.path.join(qc_receiv, s)
                domkdir(t)
                docopy(f, os.path.join(t, os.path.basename(f)), doit=doit)
        else:
            # to dispatch in preproc entry by subjects
            niigzfiles = glob.glob(os.path.join(root, '0*.nii.gz'))
            subjects = [os.path.basename(i).split('_')[0] for i in niigzfiles]
            # loop on subjects
            for s, f in zip(subjects, niigzfiles):
                t = os.path.join(preproc_receiv, s)
                domkdir(t)
                docopy(f, os.path.join(t, os.path.basename(f)), doit=doit)


############### 2a FEAT #################################################
#paires emetteurs -> (recepteurs_data, recepteurs_qc)
emits = [os.path.join(root_dir, '2a_FEAT/Motion_BL'),
         os.path.join(root_dir, '2a_FEAT/Motion_FU2'), ]
qc_receivs = [
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing_qc'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing_qc')]
preproc_receivs = [
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing')]

for emit, qc_receiv, preproc_receiv in zip(emits, qc_receivs, preproc_receivs):
    if not os.path.exists(qc_receiv):
        domakedirs(qc_receiv)
    if not os.path.exists(preproc_receiv):
        domakedirs(preproc_receiv)
    for root, dirs, files in os.walk(emit):
        #push file txt and par reorg by subjects
        if 'Motion_' in root:
            fdfiles = glob.glob(os.path.join(root, '*_fd.txt'))
            subjects = [os.path.basename(i).split('_')[0] for i in fdfiles]
            for s, f in zip(subjects, fdfiles):
                t = os.path.join(preproc_receiv, s)
                domkdir(t)
                docopy(f, os.path.join(t, os.path.basename(f)), doit=doit)
            parfiles = glob.glob(os.path.join(root, '*_mcf.par'))
            subjects = [os.path.basename(i).split('_')[0] for i in parfiles]
            for s, f in zip(subjects, parfiles):
                t = os.path.join(preproc_receiv, s)
                domkdir(t)
                docopy(f, os.path.join(t, os.path.basename(f)), doit=doit)


############### 2b_REGISTRATION #################################################
#paires emetteurs -> (recepteurs_data, recepteurs_qc)
emits = [
    os.path.join(root_dir, '2b_REGISTRATION/Registrations_BL'),
    os.path.join(root_dir, '2b_REGISTRATION/slicesdir_BL_registrations'),
    os.path.join(root_dir, '2b_REGISTRATION/Registrations_FU2'),
    os.path.join(root_dir, '2b_REGISTRATION/slicesdir_FU2_registrations'), ]
qc_receivs = [
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing_qc'),
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing_qc'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing_qc'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing_qc')]
preproc_receivs = [
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing'),
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing')]

for emit, qc_receiv, preproc_receiv in zip(emits, qc_receivs, preproc_receivs):
    if not os.path.exists(qc_receiv):
        domakedirs(qc_receiv)
    if not os.path.exists(preproc_receiv):
        domakedirs(preproc_receiv)
    if 'slicesdir' in emit:
        pngfiles = glob.glob(os.path.join(emit, '_usr*.png'))
        subjects = [os.path.basename(i).split('_')[12] for i in pngfiles]
        # loop on subjects
        for s, f in zip(subjects, pngfiles):
            t = os.path.join(qc_receiv, s)
            domkdir(t)
            docopy(f,
                   os.path.join(t, os.path.basename(f).replace('_usr_share_fsl_5.0_data_standard_', '')),
                   doit=doit)
        pngfiles = glob.glob(os.path.join(emit, '..*.png'))
        #print STOP
        if 'BETS' in pngfiles[0]:  # (chemin type BL)
            subjects = [os.path.basename(i).split('_BETS_')[1].split('_')[0] for i in pngfiles]
        elif 'laura' in pngfiles[0]:  # (chemin type FU2)
            subjects = [os.path.basename(i).split('IMAGEN_T1_FU2_')[1].split('_')[0] for i in pngfiles]
        else:
            print 'chemin incorrect', pngfiles[0]
            exit(1)
        # loop on subjects
        for s, f in zip(subjects, pngfiles):
            t = os.path.join(qc_receiv, s)
            domkdir(t)
            if 'BETS' in f:
                docopy(f,
                       os.path.join(t, os.path.basename(f).replace('.._.._T1_DATA_NEW_BETS_', '')),
                       doit=doit)
            elif 'laura' in f:
                docopy(f,
                       os.path.join(t, os.path.basename(f).replace('.._.._.._.._.._laura.daedelow_IMAGEN_T1_FU2_', '')),
                       doit=doit)
            else:
                print 'renommage incorrect', pngfiles[0]
                exit(1)
    elif 'Registrations' in emit:
        regfiles = glob.glob(os.path.join(emit, '*/reg/*'))
        subjects = [os.path.basename(i.split('/reg')[0]) for i in regfiles]
        # loop on subjects
        for s, f in zip(subjects, regfiles):
            t = os.path.join(preproc_receiv, s)
            domkdir(t)
            docopy(f, os.path.join(t, os.path.basename(f)), doit=doit)


############### 3 #################################################
#paires emetteurs -> (recepteurs_data, recepteurs_qc)
emits = [
    os.path.join(root_dir, '3_OUTPUT/Preprocessed_data/BL/rs_preproc_nonsmooth'),
    os.path.join(root_dir, '3_OUTPUT/Preprocessed_data/BL/rs_preproc_smooth'),
    os.path.join(root_dir, '3_OUTPUT/Preprocessed_data/FU2/rs_preproc_nonsmooth'),
    os.path.join(root_dir, '3_OUTPUT/Preprocessed_data/FU2/rs_preproc_smooth'),
    os.path.join(root_dir, '3_OUTPUT/TSNR_images_BL'),
    os.path.join(root_dir, '3_OUTPUT/TSNR_images_FU2'), ]
qc_receivs = [
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing_qc'),
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing_qc'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing_qc'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing_qc'),
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing_qc'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing_qc'), ]
preproc_receivs = [
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing'),
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing'),
    os.path.join(target_dir, 'BL/processed/rsfmri_preprocessing'),
    os.path.join(target_dir, 'FU2/processed/rsfmri_preprocessing'), ]

for emit, qc_receiv, preproc_receiv in zip(emits, qc_receivs, preproc_receivs):
    if not os.path.exists(qc_receiv):
        domakedirs(qc_receiv)
    if not os.path.exists(preproc_receiv):
        domakedirs(preproc_receiv)
    if 'Preprocessed_data' in emit:
        niigzfiles = glob.glob(os.path.join(emit, '0*/0*.nii.gz'))
        subjects = [os.path.basename(i).split('_')[0] for i in niigzfiles]
        # loop on subjects
        for s, f in zip(subjects, niigzfiles):
            t = os.path.join(preproc_receiv, s)
            domkdir(t)
            docopy(f, os.path.join(t, os.path.basename(f)), doit=doit)
    elif 'TSNR_images' in emit:
        niigzfiles = glob.glob(os.path.join(emit, '0*.nii.gz'))
        subjects = [os.path.basename(i).split('_')[0] for i in niigzfiles]
        # loop on subjects
        for s, f in zip(subjects, niigzfiles):
            t = os.path.join(preproc_receiv, s)
            domkdir(t)
            docopy(f, os.path.join(t, os.path.basename(f)), doit=doit)
    else:
        print 'acces incorrect', emit
        exit(1)
