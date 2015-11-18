#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Vincent Frouin, Benjamin Thyreau
Copyright (C) 2011-2015 CEA
"""
import generate_onsets


def generate_spm_model_intra_EPIstopsignal(in_fn, out_fn):

    behav = in_fn

    #
    def onsets_to_matlabstring(factorlist, namelist):
        onsetlist = [('[' + " ".join(['%4.2f' % x for x in vec]) + ']' if len(vec) else 'nan') for vec in factorlist]
        durationlist = [('[0]' if len(vec) else 'nan') for vec in factorlist]
        S = "%% Onsets names:\ncond = struct('name',  { '%s' }, ...\n'onset', { %s }', ...\n'duration', { %s })\n" % \
            ("', '".join(namelist), ",\n".join(onsetlist), ", ".join(durationlist))
        return S

    def consess_to_matlabstring(cons, fcons):
        tstrs = ["consess{%d}.tcon.name = '%s';\nconsess{%d}.tcon.convec = %s;" % (i+1, c[0], i+1, str(c[1].tolist()).replace(',', '')) for i, c in enumerate(cons)]
        fstrs = ["consess{%d}.fcon.name = '%s';\nconsess{%d}.fcon.convec = {[%s]}';" % (i+len(cons)+1, c[0], i+len(cons)+1,  ";\n ".join([" ".join(["%4.4f" % x for x in l]) for l in c[1]])) for i, c in enumerate(fcons)]
        return "\n".join(tstrs + fstrs)

    trialname = 'swea'
    factorlist, namelist = generate_onsets.generate_SS(trialname, behav)
    for i, x in enumerate(factorlist):
        if len(x) == 0:
            print "WARNING : factor %s is empty on %s. Will generate null spmT" % (s, namelist[i])
    #
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
