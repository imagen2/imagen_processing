#!/bin/bash

set -e

fail() {
	printf '%s\n' $1 >&2
	exit ${2-1}
}

real=$1

echo_time=$(fslval "${real}" descrip | cut --delimiter=";" --field=1 | cut --delimiter='=' --field=2)
if [ -z "${echo_time}" ]
then
	fail "Missing echo time in descrip of \"${real}\""
fi

prefix=$(dirname "${real}")/$(basename "${real}" _real.nii.gz)
imaginary="${prefix}_imaginary.nii.gz"

if [ ! -f "${imaginary}" ]
then
	fail "Missing imaginary image \"${imaginary}\""
fi

complex="${prefix}_complex.nii.gz"
fslcomplex -complex "${real}" "${imaginary}" "${complex}"

fslcomplex -realpolar "${complex}" "${prefix}_magnitude.nii.gz" "${prefix}_phase.nii.gz"
rm "${complex}"

cat <<EOF > "${prefix}_magnitude.json"
{
	"EchoTime": ${echo_time}
}
EOF
