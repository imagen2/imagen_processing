#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2011-2015 CEA
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
"""
@author: Vincent Frouin, Benjamin Thyreau
Copyright (C) 2011-2015 CEA
"""
import generate_onsets


def generate_spm_model_intra_EPIstopsignal(in_fn, out_fn):

    behav = in_fn

    def onsets_to_matlabstring(factorlist, namelist):
        onsetlist = [('[' + " ".join(['%4.2f' % x for x in vec]) + ']' if len(vec) else 'nan') for vec in factorlist]
        durationlist = [('[0]' if len(vec) else 'nan') for vec in factorlist]
        S = "%% Onsets names:\ncond = struct('name',  { '%s' }, ...\n'onset', { %s }', ...\n'duration', { %s })\n" % \
            ("', '".join(namelist), ",\n".join(onsetlist), ", ".join(durationlist))
        return S

    def consess_to_matlabstring(cons, fcons):
        tstrs = ["consess{%d}.tcon.name = '%s';\nconsess{%d}.tcon.convec = %s;" % (i+1, c[0], i+1, str(c[1].tolist()).replace(',', '')) for i, c in enumerate(cons)]
        fstrs = ["consess{%d}.fcon.name = '%s';\nconsess{%d}.fcon.convec = {[%s]}';" % (i+len(cons)+1, c[0], i+len(cons)+1, ";\n ".join([" ".join(["%4.4f" % x for x in l]) for l in c[1]])) for i, c in enumerate(fcons)]
        return "\n".join(tstrs + fstrs)

    trialname = 'swea'
    factorlist, namelist = generate_onsets.generate_SS(trialname, behav)
    for i, x in enumerate(factorlist):
        if len(x) == 0:
            print "WARNING : factor %s is empty on %s. Will generate null spmT" % (namelist[i], trialname)
    contrast_infos = generate_onsets.generate_contrasts_SS(trialname, factorlist, namelist, othername=['']*6, width=1)  # WARNING sync 'width' with the template .m job (hrf.derivs)!

    header_jobscript = (onsets_to_matlabstring(factorlist, namelist) + '\n' +
                        consess_to_matlabstring(*contrast_infos))
    fp = open(out_fn, 'w')
    fp.write(header_jobscript)
    fp.close()


if __name__ == "__main__":
    behav = '/neurospin/imagen/processed/nifti/000055417875/BehaviouralData/ss_000055417875.csv'

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_fn', action='store', dest='inf',
                        default=behav,
                        help='In file')
    parser.add_argument('--out_fn', action='store', dest='outf',
                        help='Out file')
    args = parser.parse_args()
    print args.inf, args.outf

    generate_spm_model_intra_EPIstopsignal(args.inf, args.outf)
