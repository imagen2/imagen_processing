#!/bin/bash

for sub in $(cat code/ids.txt); do

	site=$(grep ${sub} behavioral/ESTRA_recruitment_file_LONDON_2024-01-09_PSC2.csv | cut -d, -f3-4 | tr '[:upper:]' '[:lower:]' | tr ',' '_')
	
	if [ -z ${site} ]; then
		site=$(grep ${sub} behavioral/STRATIFY_participants.csv | cut -d, -f3-4 | tr '[:upper:]' '[:lower:]' | tr ',' '_')
	fi

	site=$(echo ${site} | sed s/_$//g)

	if [[ ${site} == berlin_ptb ]]; then
		site=berlin
	fi

	source=nifti/${sub}
	target=sorted/${site}
	if [ ! -e "${target}/${sub}" ]; then
        	rm -v sorted/*/${sub}
        	mkdir -p ${target}
                ln --symbolic --relative --no-target-directory --verbose ${source} ${target}/${sub}
	fi

one
