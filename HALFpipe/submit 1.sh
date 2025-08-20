#!/bin/bash

#SBATCH --job-name=stratify_london_cns
#SBATCH --output=halfpipe.log.txt

#SBATCH --time=4-0
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=22504M
#SBATCH --gres=localtmp:42k

#SBATCH --array=1-2

run_cmd() {
    cmd="$*"

    printf '%s\n' --------------------

    echo "${cmd}"

    start_seconds=$(date +%s)

    eval "$@"
    exit_code=$?

    end_seconds=$(date +%s)

    duration=$((end_seconds-start_seconds))

    if [[ ${exit_code} -gt 0 ]]; then
        echo "ERROR: command exited in ${duration} seconds with nonzero status $exit_code"
    else
        echo "INFO: Command exited successfully in ${duration} seconds"
    fi

    printf '%s\n' --------------------

    return ${exit_code}
}


if ! [ -x "$(command -v singularity)" ]; then
module load singularity
fi

workdir=/fast/work/groups/ag_walter/halfpipe/stratify/london_cns

nipypedir=$(mktemp -d)

run_cmd singularity run \
--contain --cleanenv  \
--bind /fast:/fast \
--bind /tmp:/tmp \
--bind ${nipypedir}:${workdir}/nipype \
/fast/groups/ag_walter/work/containers/halfpipe-latest-240226.sif \
--workdir ${workdir} \
--only-run \
--uuid  $(ls -t graphs.*.* | head -n1 | cut -d. -f2) \
--subject-chunks \
--only-chunk-index ${SLURM_ARRAY_TASK_ID} \
--nipype-n-procs 2 \
--keep none \
--subject-list ${workdir}/subject-list.txt

run_cmd cp -rnv ${nipypedir}/* ${workdir}/nipype
