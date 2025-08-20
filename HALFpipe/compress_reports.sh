#!/bin/bash

#SBATCH --job-name=compress-reports
#SBATCH --output=halfpipe.log.txt

#SBATCH --time=1:0:0
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2048M

working_directory=$(pwd)
site=$(basename ${working_directory})

pushd reports; zip --recurse-patterns --symlinks ../../reports/ds-stratify_site-${site}.zip "*"; popd
