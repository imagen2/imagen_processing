#!/bin/bash

#SBATCH --job-name=plot-skull-strip
#SBATCH --output=halfpipe.log.txt

#SBATCH --time=4:0:0
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=65536M
#SBATCH --gres=localtmp:10k

run_cmd() {
    cmd="$*"

    echo "$cmd"

    eval "$@"

    EXIT_CODE=$?

    if [[ $EXIT_CODE -gt 0 ]]; then
        echo "ERROR: command exited with nonzero status $EXIT_CODE"
    fi

    return $EXIT_CODE
}

fail() {
    printf '%s\n' "$1" >&2
    exit "${2-1}"
}

base_directory=/fast/groups/ag_walter/work

working_directory=$(pwd)
site=$(basename ${working_directory})

data_directory=${base_directory}/newdata/stratify
rawdata_directory=${data_directory}/sorted/${site}
skull_strip_directory=${data_directory}/code/lea/skull_strip/

container=${base_directory}/containers/halfpipe-latest-240226.sif

export MPLCONFIGDIR=${HOME}/.cache/matplotlib

for rpt in $(find ${working_directory}/reports -name "*_skull_strip_report*svg")
do
    # remove `.svg` or `.backup.svg` suffixes
    prefix=$(dirname ${rpt})/$(basename ${rpt} | cut -d. -f1)
    if [ ! "${rpt}" == "${prefix}.backup.svg" ]
    then
        mv -n ${rpt} ${prefix}.backup.svg
    fi

    subject=$(basename ${prefix} | cut -d_ -f1 | cut -d- -f2)

    rawdata_file=$(find ${working_directory}/rawdata/sub-${subject} -name "*_T1w.nii.gz" | head -n 1)
    if [ -e "${rawdata_file}" ]
    then
        source_file=$(readlink --canonicalize ${rawdata_file})
    else
        echo "Could not find source file \"${subject}\"" >&2
        continue
    fi

    background=$(find -L ${rawdata_directory}/${subject} -name "*ADNI*MPRAGE*.nii.gz" | head -n 1)
    if [ ! -f ${background} ]
    then
        echo "Could not find background file for \"${subject}\"" >&2
        continue
    fi

    derivatives_directory=$(dirname ${rawdata_file} | sed "s#rawdata#derivatives/fmriprep#g")
    mask_file=$(find ${derivatives_directory} -name "*_desc-brain_mask.nii.gz" | grep -v space | head -n 1)
    if [ ! -f ${mask_file} ]
    then
        echo "Could not find mask file for \"${subject}\"" >&2
        continue
    fi

    echo singularity exec \
            --bind /fast:/fast \
            --bind /tmp:/tmp \
            ${container} \
        python ${base_directory}/halfpipe/plot_skull_strip.py \
            --mask-file ${mask_file} \
            --background-file ${background} \
        --output-file ${prefix}.svg
done | parallel --jobs 32 --verbose --line-buffer

run_cmd bash ${base_directory}/halfpipe/stratify/compress_reports.sh
