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
@author: Benjamin Thyreau, Jean-Baptiste Poline, Vincent Frouin, Dimitri Papadopoulos
Copyright (c) 2011-2015 CEA
"""
import numpy as np
import re
import codecs


def parse_columns_csv(f, format, sep='\t', skiplines=0, skipOnEmpty_Column=None):
    for i in range(skiplines):
        f.readline()
    content = [k.split('\t') for k in f if k.rstrip()]  # skip blank lines
    mcontent = [x for x in zip(*content)]
    #acontent = [np.array(x) for x in zip(*content)]
    if skipOnEmpty_Column:
        #linesMask = acontent[skipOnEmpty_Column] != ''
        linesMask = np.array([x != '' for x in mcontent[skipOnEmpty_Column]])
        #if False in linesMask:
        #    print "parse warning : Skipping as Time seems empty, at line(s)", np.nonzero(linesMask == False)[0]
    else:
        linesMask = np.ones(len(mcontent[0]), bool_)
    out = []
    for v, c in zip(mcontent, format):
        if c == 'i':
            #v[v == ''] = 0
            v = np.array([int(x) if x else 0 for x in v], 'i')
        elif c == 'f':
            #v[v == ''] = np.nan
            v = np.array([float(x) if x else np.nan for x in v], 'f')
        elif c == 'S':
            v = np.array([codecs.encode(x, 'latin1').strip('"') for x in v], 'S')  # Force converting from utf8 to latin1
        elif c == '_':
            #v[:] = ''
            v = np.zeros(len(v), 'S')
            c = 'S'
        out.append(v[linesMask])
    return out


def detectAndFixTimeResets(out, timeColumnNumber):
    if len(set([len(x) for x in out])) != 1:
        print "parse WARNING : not all parsed columns have the same length!", [len(x) for x in out]
    rewindIndex = np.nonzero(out[timeColumnNumber][1:] < out[timeColumnNumber][:-1])[0] + 1
    if len(rewindIndex) > 0:
        out = [x[rewindIndex[-1]:] for x in out]
        print "parse WARNING : Seems that the session has been restarted in logfile (time seems to rewind)", rewindIndex
        print "Reading from line number ", rewindIndex[-1], "(excluding skipped lines)", out[timeColumnNumber][0:3], "..."
    return out


def generate_MID_nonparam(csvfile):
    out = parse_columns_csv(codecs.open(csvfile, encoding='utf-8'), 'iSiiSiiiiSiiSiifi', skiplines=2, skipOnEmpty_Column=2)
    out = detectAndFixTimeResets(out, 2)

    Trial, Trial_Category, Trial_Start_Time_Onset, Pre_determined_Onset, Cue_Presented, Anticipation_Phase_Start_Time, Anticipation_Phase_Duration, Target_Phase_Start_Time, Target_Phase_Duration, Response_Made_by_Subject, Response_time, Feedback_Phase_Start_Time, Outcome, Amount, Fixation_Phase_Start_Time, Success_Rate, Scanner_Pulse = out

    AnticipStartTime = Anticipation_Phase_Start_Time / 1000.
    #AnticipDuration = Anticipation_Phase_Duration / 1000.
    ResponseTime = Response_time / 1000.
    FeedbackStartTime = (Target_Phase_Start_Time + Target_Phase_Duration) / 1000.
    # MODELE NON PARAMETRE
    if 1:
        didpress = np.array([not x.endswith("NO RESPONSE") for x in Response_Made_by_Subject])

        anticip_hit_largewin = AnticipStartTime[(Trial_Category == 'BIG_WIN') & (Outcome == 'SUCCESS')]
        anticip_hit_smallwin = AnticipStartTime[(Trial_Category == 'SMALL_WIN') & (Outcome == 'SUCCESS')]
        anticip_hit_nowin = AnticipStartTime[(Trial_Category == 'NO_WIN') & (Outcome == 'SUCCESS')]

        # missed => too late or too early, but never NO RESPONSE
        anticip_missed_largewin = AnticipStartTime[(Trial_Category == 'BIG_WIN') & (Outcome == 'FAILURE') & didpress]
        anticip_missed_smallwin = AnticipStartTime[(Trial_Category == 'SMALL_WIN') & (Outcome == 'FAILURE') & didpress]
        anticip_missed_nowin = AnticipStartTime[(Trial_Category == 'NO_WIN') & (Outcome == 'FAILURE') & didpress]

        anticip_noresp = AnticipStartTime[(Outcome == 'FAILURE') & (didpress is False)]

        # Include those silly "TO_EARLY:Left/Right" as "Left/Right"
        allResponsesAtLeft = np.array([x.endswith('Left') for x in Response_Made_by_Subject])
        pressleft = ResponseTime[allResponsesAtLeft]
        allResponsesAtRight = np.array([x.endswith('Right') for x in Response_Made_by_Subject])
        pressright = ResponseTime[allResponsesAtRight]

        feedback_hit_largewin = FeedbackStartTime[(Trial_Category == 'BIG_WIN') & (Outcome == 'SUCCESS')]
        feedback_hit_smallwin = FeedbackStartTime[(Trial_Category == 'SMALL_WIN') & (Outcome == 'SUCCESS')]
        feedback_hit_nowin = FeedbackStartTime[(Trial_Category == 'NO_WIN') & (Outcome == 'SUCCESS')]

        feedback_missed_largewin = FeedbackStartTime[(Trial_Category == 'BIG_WIN') & (Outcome == 'FAILURE') & didpress]
        feedback_missed_smallwin = FeedbackStartTime[(Trial_Category == 'SMALL_WIN') & (Outcome == 'FAILURE') & didpress]
        feedback_missed_nowin = FeedbackStartTime[(Trial_Category == 'NO_WIN') & (Outcome == 'FAILURE') & didpress]

        feedback_noresp = FeedbackStartTime[(Outcome == 'FAILURE') & (didpress is False)]

        namelist = ["anticip_hit_largewin", "anticip_hit_smallwin", "anticip_hit_nowin", "anticip_missed_largewin", "anticip_missed_smallwin", "anticip_missed_nowin", "anticip_noresp", "feedback_hit_largewin", "feedback_hit_smallwin", "feedback_hit_nowin", "feedback_missed_largewin", "feedback_missed_smallwin", "feedback_missed_nowin", "feedback_noresp", "pressleft", "pressright"]
        factorlist = [eval(x) for x in namelist]
        #modulationnamelist = ["anticip_hit_modgain", "anticip_missed_modgain", "feedback_hit_modgain", "feedback_missed_modgain"]
        #modulationnameparams = [eval(x) for x in modulationnamelist]
        #modulewhere = np.array([namelist.index(re.sub('_mod.*', '', x)) for x in modulationnamelist]) + 1

        return factorlist, namelist  #, modulationnameparams, modulationnamelist, modulewhere


def generate_contrasts_MID_nonparam(trialname, factorlist, namelist, othername=['']*6, width=3):
    bloc0 = [0.] * width
    bloc1 = [1.] + [0.] * (width - 1)

    # ensemble des facteurs qui n'ont pas d'occurence:
    badfactors = set([name for name, factor in zip(namelist, factorlist) if len(factor) == 0])

    #nl = modulationnamelist[:]
    #namelist = reduce(list.__add__, [([name] + ( [nl.pop(0)] if (i+1) in modulewhere else [] )) for i, name in enumerate(namelist)])

    C = dict((name, np.array(bloc0 * i + bloc1 + bloc0 * (len(namelist)-i-1) + [0]*len(othername) + [0])) for i, name in enumerate(namelist))

    def vectoradd(name, involvednames, vect):
        C[name] = vect
        if badfactors.intersection(involvednames):
            badfactors.add(name)
        return [name]

    def parseadd(name, formula):
        tmp = re.findall("([+-])?\s*'([^']+)'", formula)
        return vectoradd(name, [x[1] for x in tmp], np.sum([C[f] * (-1 if s is '-' else 1) for s, f in tmp], 0))

    def cleancon(name):
        if name in badfactors:
            x = np.zeros_like(C[name])
            x[..., -1] = 1
            name = 'unestimable (was "%s") replaced by dummy' % name
        else:  # normalize
            x = C[name].copy()
            x[x > 0] /= abs(x[x > 0].sum())
            x[x < 0] /= abs(x[x < 0].sum())
        return name, x

    # Contrastes T :
    connamelist = []
    connamelist += parseadd("anticip", "'anticip_hit_largewin' + 'anticip_hit_smallwin' + 'anticip_hit_nowin' + 'anticip_missed_largewin' + 'anticip_missed_smallwin' + 'anticip_missed_nowin'")  # pas noresp
    connamelist += parseadd("anticip_hit", "'anticip_hit_largewin' + 'anticip_hit_smallwin' + 'anticip_hit_nowin'")
    connamelist += parseadd("anticip_missed", "'anticip_missed_largewin' + 'anticip_missed_smallwin' + 'anticip_missed_nowin'")
    connamelist += parseadd("anticip_noresp", "'anticip_noresp'")

    # Section : effect of hit, missed, and noresp, whatever the Gain, during Anticipation
    connamelist += parseadd("anticip_hit-missed", "'anticip_hit' - 'anticip_missed'")
    connamelist += parseadd("anticip_missed-hit", "'anticip_missed' - 'anticip_hit'")

    connamelist += parseadd("anticip_hit-noresp", "'anticip_hit' - 'anticip_noresp'")
    connamelist += parseadd("anticip_noresp-hit", "'anticip_noresp' - 'anticip_hit'")

    connamelist += parseadd("anticip_hit_largewin - smallwin", "'anticip_hit_largewin' - 'anticip_hit_smallwin'")
    connamelist += parseadd("anticip_hit_largewin - nowin", "'anticip_hit_largewin' - 'anticip_hit_nowin'")
    connamelist += parseadd("anticip_hit_smallwin - nowin", "'anticip_hit_smallwin' - 'anticip_hit_nowin'")

    connamelist += parseadd("anticip_missed_largewin - smallwin", "'anticip_missed_largewin' - 'anticip_missed_smallwin'")
    connamelist += parseadd("anticip_missed_largewin - nowin", "'anticip_missed_largewin' - 'anticip_missed_nowin'")
    connamelist += parseadd("anticip_missed_smallwin - nowin", "'anticip_missed_smallwin' - 'anticip_missed_nowin'")

    connamelist += parseadd("anticip - anticip_noresp", "'anticip_hit' + 'anticip_missed' - 'anticip_noresp'")

    connamelist += parseadd("feedback", "'feedback_hit_largewin' + 'feedback_hit_smallwin' + 'feedback_hit_nowin' + 'feedback_missed_largewin' + 'feedback_missed_smallwin' + 'feedback_missed_nowin'")  # pas noresp
    connamelist += parseadd("feedback_hit", "'feedback_hit_largewin' + 'feedback_hit_smallwin' + 'feedback_hit_nowin'")
    connamelist += parseadd("feedback_missed", "'feedback_missed_largewin' + 'feedback_missed_smallwin' + 'feedback_missed_nowin'")
    # See also below for the win-limited contrast

    # Section : effect of hit, missed, whatever the Gain, during Feedback
    connamelist += parseadd("feedback_hit-missed", "'feedback_hit' - 'feedback_missed'")
    connamelist += parseadd("feedback_missed-hit", "'feedback_missed' - 'feedback_hit'")

    #! connamelist += parseadd("feedback_largewin - nowin","'feedback_hit_largewin' + 'feedback_hit_smallwin' - 'feedback_hit_nowin' + 'feedback_missed_largewin' + 'feedback_missed_smallwin' - 'feedback_missed_nowin'") # !

    # Section: exploring the Gain effect
    connamelist += parseadd("feedback_hit_largewin - smallwin", "'feedback_hit_largewin' - 'feedback_hit_smallwin'")
    connamelist += parseadd("feedback_hit_largewin - nowin", "'feedback_hit_largewin' - 'feedback_hit_nowin'")
    connamelist += parseadd("feedback_hit_smallwin - nowin", "'feedback_hit_smallwin' - 'feedback_hit_nowin'")

    connamelist += parseadd("feedback_missed_largewin - smallwin", "'feedback_missed_largewin' - 'feedback_missed_smallwin'")
    connamelist += parseadd("feedback_missed_largewin - nowin", "'feedback_missed_largewin' - 'feedback_missed_nowin'")
    connamelist += parseadd("feedback_missed_smallwin - nowin", "'feedback_missed_smallwin' - 'feedback_missed_nowin'")

    connamelist += parseadd("press L + R", "'pressleft' + 'pressright'")
    connamelist += parseadd("press L - R", "'pressleft' - 'pressright'")
    connamelist += parseadd("press R - L", "- 'press L - R'")

    # NOUVEAU !
    # Section: contrasts on reward vs no reward
    connamelist += parseadd("anticip_hit_somewin - nowin", "'anticip_hit_largewin' + 'anticip_hit_smallwin' - 'anticip_hit_nowin'")
    connamelist += parseadd("anticip_missed_somewin - nowin", "'anticip_missed_largewin' + 'anticip_missed_smallwin' - 'anticip_missed_nowin'")

    connamelist += parseadd("feedback_hit_somewin - nowin", "'feedback_hit_largewin' + 'feedback_hit_smallwin' - 'feedback_hit_nowin'")
    connamelist += parseadd("feedback_missed_somewin - nowin", "'feedback_missed_largewin' + 'feedback_missed_smallwin' - 'feedback_missed_nowin'")

    # Section : on reward-only, hit-missed
    connamelist += parseadd("feedback_somewin_hit - missed", "'feedback_hit_largewin' + 'feedback_hit_smallwin' - 'feedback_missed_largewin' - 'feedback_missed_smallwin'")
    connamelist += parseadd("feedback_somewin_missed - hit", "- 'feedback_somewin_hit - missed'")

    # Nouveau:
    connamelist += parseadd("feedback_somewin - nowin", "'feedback_hit_somewin - nowin' + 'feedback_missed_somewin - nowin'")

    # Nouveau 23.06.2010; contrastes sur la baseline:
    connamelist += parseadd("anticip_hit_largewin", "'anticip_hit_largewin'")
    connamelist += parseadd("- anticip_hit_largewin", "- 'anticip_hit_largewin'")
    connamelist += parseadd("feedback_hit_largewin", "'feedback_hit_largewin'")
    connamelist += parseadd("- feedback_hit_largewin", "- 'feedback_hit_largewin'")
    connamelist += parseadd("anticip_hit_largewin - feedback_hit_largewin", "'anticip_hit_largewin' - 'feedback_hit_largewin'")
    connamelist += parseadd("feedback_hit_largewin - anticip_hit_largewin", "- 'anticip_hit_largewin - feedback_hit_largewin'")  # rev
    connamelist += parseadd("anticip_hit_nowin - feedback_hit_nowin", "'anticip_hit_nowin' - 'feedback_hit_nowin'")
    connamelist += parseadd("feedback_hit_nowin - anticip_hit_nowin", "- 'anticip_hit_nowin - feedback_hit_nowin'")

    # Contrastes F :
    fconnamelist = []
    #fconnamelist += vectoradd('Missed with Response VS Missed w/o Response', namelist, np.vstack([C[x] for x in namelist]))
    fconnamelist += vectoradd('Effect of interest', namelist, np.vstack([C[x] for x in namelist]))
    fconnamelist += vectoradd('Anticip_hit_GainEffect', ["anticip_hit_largewin - smallwin", "anticip_hit_smallwin - nowin"], np.vstack([C["anticip_hit_largewin - smallwin"], C["anticip_hit_smallwin - nowin"]]))
    fconnamelist += vectoradd('Anticip_missed_GainEffect', ["anticip_missed_largewin - smallwin", "anticip_missed_smallwin - nowin"], np.vstack([C["anticip_missed_largewin - smallwin"], C["anticip_missed_smallwin - nowin"]]))
    fconnamelist += vectoradd('Feedback_hit_GainEffect', ["feedback_hit_largewin - smallwin", "feedback_hit_smallwin - nowin"], np.vstack([C["feedback_hit_largewin - smallwin"], C["feedback_hit_smallwin - nowin"]]))
    fconnamelist += vectoradd('Feedback_missed_GainEffect', ["feedback_missed_largewin - smallwin", "feedback_missed_smallwin - nowin"], np.vstack([C["feedback_missed_largewin - smallwin"], C["feedback_missed_smallwin - nowin"]]))

    if trialname == "swea_mvtroi":
        # modele avec 6+3+3 + 9 reg de mvt et rois
        fconnamelist += vectoradd('Effect of rp', [], np.column_stack((np.zeros((12, width * len(namelist))), np.identity(12))))
        fconnamelist += vectoradd('Effect of rp high', [], np.column_stack((np.zeros((6, width * len(namelist) + 6)), np.identity(6))))
        fconnamelist += vectoradd('Effect of ventricles', [], np.column_stack((np.zeros((9, width * len(namelist) + 12)), np.identity(9))))
    else:
        # modele avec 18-reg de mvt
        fconnamelist += vectoradd('Effect of rp', [], np.column_stack((np.zeros((18, width * len(namelist))), np.identity(18), np.zeros(18))))
        fconnamelist += vectoradd('Effect of rp high', [], np.column_stack((np.zeros((12, width * len(namelist) + 6)), np.identity(12), np.zeros(12))))

    return [cleancon(x) for x in connamelist], [cleancon(x) for x in fconnamelist]
