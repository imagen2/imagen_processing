#!/bin/bash

#SBATCH --job-name=synthseg

#SBATCH --output=synthseg.log.txt
#SBATCH --open-mode=append

#SBATCH --partition=gpu

#SBATCH --time=12:0:0
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --gres=gpu:tesla:1 

cd /fast/work/groups/ag_walter/newdata/stratify/code

singularity run \
    --nv \
    --bind /fast:/fast \
    ~/work/containers/synthseg-2022-12-09-2dd6c9af5aac.sif \
        --i synthseg_i.filtered.txt \
        --o synthseg_o.filtered.txt \
        --robust
