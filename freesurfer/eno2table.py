#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2019 CEA
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

# Create TSV tables with stats extracted from each individual dataset
# processed by FreeSurfer.

import os
import sys
import argparse
import re
import csv


ENO_REGEX = re.compile('orig.nofix lheno +=\s+(-?\d+), +rheno +=\s+(-?\d+)')

DELIMITER = [
    ('tab', '\t'),
    ('comma', ','),
    ('space', ' '),
    ('semicolon', ';'),
]


def extract_euler_number(logfile):
    with open(logfile) as f:
        for line in f:
            match = ENO_REGEX.match(line)
            if match:
                rheno = int(match.group(1))
                lheno = int(match.group(2))
                break
        else:
            rheno = None
            lheno = None
    return rheno, lheno


# extracts the Euler numbers of the orig.nofix surfaces
def extract_euler_numbers(subjects):
    subjects_dir = os.environ['SUBJECTS_DIR']
    print('SUBJECTS_DIR : ' + subjects_dir)
    print('Parsing the log files')

    result = {}
    for subject in subjects:
        logfile_path = os.path.join(subjects_dir,
                                    subject, 'scripts', 'recon-all.log')
        result[subject] = extract_euler_number(logfile_path)
    return result


def main(argv):
    parser = argparse.ArgumentParser(description='Extract Euler numbers from FreeSurfer log files.')
    parser.add_argument('-s', '--subjects',
                        nargs='*',
                        required=True,
                        help='subject1 <subject2 subject3..>')
    parser.add_argument('-t', '--tablefile',
                        required=True,
                        help='output table file')
    delimiter_args, _ = zip(*DELIMITER)
    parser.add_argument('-d', '--delimiter',
                        default=delimiter_args[0],
                        choices=delimiter_args,
                        help='delimiter between measures in the table')
    args = parser.parse_args(argv[1:])

    result = extract_euler_numbers(args.subjects)

    print('Writing the table to ' + args.tablefile)
    with open(args.tablefile, 'w', newline='') as csvfile:
        delimiters = {x[0]: x[1] for x in DELIMITER}
        writer = csv.writer(csvfile,
                            delimiter=delimiters[args.delimiter],
                            quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('orig.nofix', 'rheno', 'lheno', 'mean'))
        for subject in sorted(result.keys()):
            rh_eno, lh_eno = result[subject]
            if rh_eno and lh_eno:
                mean_eno = rh_eno + lh_eno
                if mean_eno % 2:
                    mean_eno /= 2
                else:
                    mean_eno //= 2
            else:
                mean_eno = None
            writer.writerow((subject, rh_eno, lh_eno, mean_eno))


if __name__ == "__main__":
    main(sys.argv)
