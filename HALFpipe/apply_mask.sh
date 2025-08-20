#!/bin/bash
#SBATCH --job-name=apply_mask

#SBATCH --output=apply_mask.log.txt
#SBATCH --open-mode=append

#SBATCH --time=12:0:0
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=96
#SBATCH --exclusive
#SBATCH --mem=0

cd /fast/work/groups/ag_walter/newdata/stratify/code/lea
mkdir -p skull_strip

for i in $(paste -d":" synthseg_i.txt synthseg_o.txt); do     
    a=$(echo $i | cut -d: -f1)
    b=$(echo $i | cut -d: -f2) 
    c=skull_strip/$(basename $b _dseg.nii.gz)_synthseg.nii.gz

    if [ -f $c ] || [ ! -f $b ]; then 
        continue
    fi

    echo $a "->" $c
    singularity exec \
        --bind /fast:/fast \
    /fast/work/groups/ag_walter/containers/halfpipe-latest-240220.sif \
        antsApplyTransforms --dimensionality 3 --input $b --reference-image $a --output tmp.nii.gz --interpolation MultiLabel --verbose

    singularity exec \
        --bind /fast:/fast \
    /fast/work/groups/ag_walter/containers/halfpipe-latest-240220.sif \
        $(pwd)/apply_mask.py $a tmp.nii.gz $c

    rm tmp.nii.gz
done
