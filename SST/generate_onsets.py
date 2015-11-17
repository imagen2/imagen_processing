# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:49:33 2015

@author: vf140245, Benjamin Thyreau
Copyrignt : CEA NeuroSpin - 2015
"""


import numpy as np
import re
import codecs


def parse_columns_csv(f, format, sep = '\t', skiplines = 0, skipOnEmpty_Column = None):
    for i in range(skiplines):
        f.readline()
    content = [k.split('\t') for k in f if k.rstrip() ] # skip blank lines
    mcontent = [x for x in zip(*content)]
    #acontent = [np.array(x) for x in zip(*content)]
    if skipOnEmpty_Column:
        #linesMask = acontent[skipOnEmpty_Column] != ''
	linesMask = np.array([x != '' for x in mcontent[skipOnEmpty_Column]])
    	#if False in linesMask:
    	#	print "parse warning : Skipping as Time seems empty, at line(s)", np.nonzero(linesMask == False)[0]
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
	    v = np.array([codecs.encode(x, 'latin1').strip('"') for x in v], 'S') # Force converting from utf8 to latin1
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


def generate_SS(trialname, csvfile):
	#TR = 2.2 #should be on swaImg.rtime !
	out = parse_columns_csv(codecs.open(csvfile, encoding='utf-8'), 'iSiifSiiSiiSfif', skiplines=2, skipOnEmpty_Column = 2)

	out = detectAndFixTimeResets(out, 2)

	Trial, Trial_Category, Trial_Start_Time_Onset, Pre_determined_randomised_onset, Go_Stimulus_Presentation_Time, Stimulus_Presented, Delay, Stop_Stimulus_Presentation_Time, Response_made_by_subject, Absolute_Response_Time, Relative_Response_Time, Response_Outcome, Real_Jitter, Pre_determined_Jitter, Success_Rate_of_Variable_Delay_Stop_Trials = out

	GoTime = Go_Stimulus_Presentation_Time / 1000.
	StopTime = (Go_Stimulus_Presentation_Time + Delay) / 1000.

	Trial, Trial_Category, Trial_Start_Time_Onset, Pre_determined_randomised_onset, Go_Stimulus_Presentation_Time, Stimulus_Presented, Delay, Stop_Stimulus_Presentation_Time, Response_made_by_subject, Absolute_Response_Time, Relative_Response_Time, Response_Outcome, Real_Jitter, Pre_determined_Jitter, Success_Rate_of_Variable_Delay_Stop_Trials = out

#GO      LeftArrow       GO_SUCCESS
#GO      LeftArrow       GO_TOO_LATE
#GO      LeftArrow       GO_WRONG_KEY_RESPONSE
#STOP_VAR        LeftArrow       STOP_FAILURE
#STOP_VAR        LeftArrow       STOP_SUCCESS
#STOP_VAR        LeftArrow       STOP_TOO_EARLY_RESPONSE
#GO      RightArrow      GO_SUCCESS
#GO      RightArrow      GO_TOO_LATE
#GO      RightArrow      GO_WRONG_KEY_RESPONSE
#STOP_VAR        RightArrow      STOP_FAILURE
#STOP_VAR        RightArrow      STOP_SUCCESS
#STOP_VAR        RightArrow      STOP_TOO_EARLY_RESPONSE
	if trialname == "swea_mvtroi":
		stop_success = GoTime[Response_Outcome == 'STOP_SUCCESS']
		stop_failure = GoTime[Response_Outcome == 'STOP_FAILURE']

		go_toolate = GoTime[Response_Outcome == 'GO_TOO_LATE']
		go_wrong = GoTime[Response_Outcome == 'GO_WRONG_KEY_RESPONSE']

		namelist = ["stop_success", "stop_failure", "go_toolate", "go_wrong"]
		factorlist = [stop_success, stop_failure, go_toolate, go_wrong]
	else:
		go_success = GoTime[(Response_Outcome == 'GO_SUCCESS') | (Response_Outcome == 'STOP_TOO_EARLY_RESPONSE')]
		go_toolate = GoTime[Response_Outcome == 'GO_TOO_LATE']
		go_wrong = GoTime[Response_Outcome == 'GO_WRONG_KEY_RESPONSE']
		stop_success = GoTime[Response_Outcome == 'STOP_SUCCESS']
		stop_failure = GoTime[Response_Outcome == 'STOP_FAILURE']

		namelist = ["go_success", "go_toolate", "go_wrong", "stop_success", "stop_failure"]
		factorlist = [go_success, go_toolate, go_wrong, stop_success, stop_failure]

	return factorlist ,namelist

def generate_contrasts_SS(trialname, factorlist, namelist, othername = [''] * 6, width = 3):
	bloc0 = [0.] * width
	bloc1 = [1.] + [0.] * (width - 1)

	# ensemble des facteurs qui n'ont pas d'occurence:
	badfactors = set([name for name, factor in zip(namelist, factorlist) if len(factor) == 0])

	C = dict((name, np.array( bloc0 * i + bloc1 + bloc0 * (len(namelist)-i-1) + [0]*len(othername) + [0] )) for i, name in enumerate(namelist))
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
			x[...,-1] = 1
			name = 'unestimable (was "%s") replaced by dummy' % name
		else: # normalize
			x = C[name].copy()
			x[x > 0] /= abs(x[x > 0].sum())
			x[x < 0] /= abs(x[x < 0].sum())
		return name, x

	# Contrastes T :
	connamelist = [ x for x in namelist]
	if trialname == "swea_mvtroi": # nouveau modele
		connamelist += parseadd('stop_success - stop_failure', "'stop_success' - 'stop_failure'")
		connamelist += parseadd('stop_failure - stop_success', "- 'stop_success - stop_failure'")

	else: # ancien modele (pour swea)
		connamelist = [ x for x in namelist]
		connamelist += parseadd('stop_success - go_success', "'stop_success' - 'go_success'")
		connamelist += parseadd('go_success - stop_success', "- 'stop_success - go_success'")
		connamelist += parseadd('stop_success - stop_failure', "'stop_success' - 'stop_failure'")
		connamelist += parseadd('stop_failure - stop_success', "- 'stop_success - stop_failure'")
		connamelist += parseadd('go_success - stop_failure', "'go_success' - 'stop_failure'")
		connamelist += parseadd('stop_failure - go_success', "- 'go_success - stop_failure'")
		connamelist += parseadd('go_wrong - go_success', "'go_wrong' - 'go_success'")
		connamelist += parseadd('go_success - go_wrong', "- 'go_wrong - go_success'")

	# Contrastes F :
	fconnamelist = []
	if trialname == "swea_mvtroi":
		fconnamelist += vectoradd('Effect of interest', namelist, np.vstack([C[x] for x in namelist[:2]]))
	else: # ancien modele (pour swea, avec baseline)
		fconnamelist += vectoradd('Effect of interest', namelist, np.vstack([C[x] for x in namelist]))

	if trialname == "swea_mvtroi":
		# modele avec 6+3+3 + 9 reg de mvt et rois
		fconnamelist += vectoradd('Effect of rp', [], np.column_stack((np.zeros((12, width * len(namelist))), np.identity(12))))
		fconnamelist += vectoradd('Effect of rp high', [], np.column_stack((np.zeros((6, width * len(namelist) + 6)), np.identity(6))))
		fconnamelist += vectoradd('Effect of ventricles', [], np.column_stack((np.zeros((9, width * len(namelist) + 12)), np.identity(9), np.zeros(9))))
	else:
		# modele avec 18-reg de mvt
		fconnamelist += vectoradd('Effect of rp', [], np.column_stack((np.zeros((18, width * len(namelist))), np.identity(18), np.zeros(18))))
		fconnamelist += vectoradd('Effect of rp high', [], np.column_stack((np.zeros((12, width * len(namelist) + 6)), np.identity(12), np.zeros(12))))

	return [cleancon(x) for x in connamelist], [cleancon(x) for x in fconnamelist]