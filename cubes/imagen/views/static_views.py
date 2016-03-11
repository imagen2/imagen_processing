# -*- coding: utf-8 -*-
# copyright 2014-2016 CEA (Saclay, FRANCE), all rights reserved.
# contact http://www.cea.fr -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.


from cubicweb.view import EntityStartupView
from cubicweb.web.views.baseviews import NullView


class QC_central(EntityStartupView):
    __regid__ = 'QC_central'
    title = "QC central"

    def call(self, **kwargs):

        self._cw.add_js("pdfobject.js")

        self.w(u'<div class="panel panel-warning">')
        self.w(u'<div class="panel-heading">')
        self.w(u'<h2 class="panel-title">WORK IN PROGRESS</h2>')
        self.w(u'</div>')
        self.w(u'<div class="panel-body">')
        self.w(u"This page will gather all information about all quality"
               "that will be performed on the data. For each of them, the "
               "following details will be given:")
        self.w(u"<ul>")
        self.w(u"<li> How are QC outcomes displayed in the database </li>")
        self.w(u"<li> What is the meaning of each score </li>")
        self.w(u"<li> Who performed the QCs </li>")
        self.w(u"<li> When was the QCs performed </li>")
        self.w(u"<li> The tools and algorithms used for QCs </li>")
        self.w(u"<li> ... </li>")
        self.w(u"</ul>")
        self.w(u'</div>')
        self.w(u'</div>')

#        # EPI
#        self.w(u'<div class="panel panel-info">')
#        self.w(u'<div class="panel-heading">')
#        self.w(u'<div class="panel-title" ')
#        self.w(u'<h1><strong>EPI sequence</strong></h1>')
#        self.w(u'</div>')
#        # add download link
#        self.w(u'<a href="{0}"><button type="button">Download reference file ('
#               'pdf)</button></a>'.format(
#                   self._cw.data_url('EPI_doc.pdf'),))
#        self.w(u'</div>')
#        self.w(u'<div class="panel-body">')
#        # intro title
#        self.w(u'<div data-toggle="collapse" data-target="#doc_EPI_intro">')
#        self.w(u'<button type="button" class="btn btn-link">')
#        self.w(u'<center><h2><strong>Introduction</strong></h2></center>')
#        self.w(u'</button>')
#        self.w(u'<span class="caret"></span>')
#        self.w(u'</div>')
#
#        # INTRO BLOCK
#        self.w(u'<div id="doc_EPI_intro" class="collapse">')
#        self.w(u'<h2>Information common to all fMRI Protocols</h2>')
#        self.w(u'<h3>fMRI pre-processings</h3>')
#        self.w(u'The pre-processing of the EPI data are done within SPM8 '
#               '(Statistical Parametric Mapping, <a href="url">http://www.fil.'
#               'ion.ucl.ac.uk/spm/</a>). Time series data are first <b>correct'
#               'ed for slice-timin'
#               'g</b>, then corrected for movement (spatial <b>realignment</b>'
#               '), non-linearly warped on the <b>MNI space</b> (using a <b>cus'
#               'tom EPI template</b>), an'
#               'd gaussian-<b>smoothed at 5mm-FWHM</b>.')
#
#        self.w(u'<h3>fMRI first level analyses</h3>')
#        self.w(u'Activation maps are computed with SPM8, and regressed using a'
#               'general linear model (<b>GLM</b>) with <b>AR</b> noise model ('
#               'spm default) against a design-matrix built from the informatio'
#               'ns contained in the Imagen Behavioural Files (csv files). <b>E'
#               'stimated movement</b> was added to the design matrix in the fo'
#               'rm of 18 additional columns (3 translations, 3 rotations, 3 qu'
#               'adratic and 3 cubic translations, 3 translations shifted 1 TR '
#               'before, and 3 translations shifted 1 TR later). The regressors'
#               'modeling the experimental conditions are convolved using <b>SP'
#               "M's default HRF</b> (Hemodynamic Response Function). The estim"
#               'ated model ("beta") parameters maps are linearly-combined to y'
#               'ield contrasts maps and significance maps, hereafter respectiv'
#               'ely called <b>"con maps"</b> and <b>"spmT maps"</b>, while the'
#               'residual variance of the model fit is stored as an additional '
#               'map.')
#        self.w(u'<br>')
#
#        self.w(u'<center><figure><img src="{0}" alt="SPM '
#               'default hrf"/>'.format(
#                   self._cw.data_url("images/doc/spm_default_hrf.png")))
#        self.w(u'<figcaption>SPM default hrf</figcaption></figure></center>')
#
#        self.w(u'<h3>Additional Informations</h3>')
#        self.w(u'See also the document titled "Processing FAQ" for complementa'
#               'ry technical informations about the preprocessings. Although t'
#               'he data were computed with the SPM software, it was a major de'
#               'sign goal to make every files useable in any context, which me'
#               'ans at no point should the SPM software itself be required to '
#               'get access to major parameters. If some information seems to b'
#               'e missing, please contact <a href="mailto:imagendatabase@cea.f'
#               'r">imagendatabase@cea.fr</a> (before contacting directly Benja'
#               'min Thyreau (<a href="mailto:benjamin.thyreau@cea.fr">benjamin'
#               '.thyreau@cea.fr</a>) or Jean-Baptiste Poline (<a href="mailto:'
#               'jbpoline@gmail.com">jbpoline@gmail.com</a>)).'
#               '<br><br><u>Naming scheme note:</u><br><br>'
#               'Among a single protocol, we tried to standardize file sets and'
#               ' results across subjects, e.g. the contrast map file named con'
#               '_00NN.nii.gz always refers to the same contrast across subject'
#               's. It is however always advisable to have a quick look to ever'
#               'y files before processing to an analysis.'
#               '<br><br><u>Currently the following potential caveat are to be '
#               'carefully checked:</u><br><br>')
#        self.w(u'<ul>')
#        self.w(u'<li>Some contrasts for some subjects are not estimable ; ther'
#               'e can be several causes for that, but the most common case is '
#               'that a condition is never present/recorded for some subjects, '
#               'for instance, a Left-Right motor contrasts concerning an acqui'
#               'sition run whose push-button mechanically failed. Those <b>non'
#               ' estimable</b> contrasts contains the string "unestimable" in '
#               'the "de'
#               'scription" field of the Nifti image header. That information s'
#               'hould also be available directly from the Imagen database fron'
#               'tend.</li>')
#        self.w(u'<li>Although efforts were made to manually recover from some '
#               'common errors, subjects datasets which failed to be processed '
#               'for <b>any</b> reason may simply not be available in the datab'
#               'ase. Re'
#               'asons may include, but not limited to: bad or incomplete fMRI '
#               'runs, questionable values in the behavioural-csv files, algori'
#               'thmic failure of some previous step (e.g. preprocessing, dicom'
#               ' file-conversion), missing runs, etc.</li>')
#        self.w(u'<br><br><u>The following is task-specific references notes.</'
#               'u><br><br>')
#
#        self.w(u'</div>')
#        # END INTRO
#
#        # GCA subtitle
#        self.w(u'<div data-toggle="collapse" data-target="#doc_EPI_GCA">')
#        self.w(u'<button type="button" class="btn btn-link">')
#        self.w(u'<center><h2><strong>GCA – Global Cognitive Assessment'
#               '</strong></h2></center>')
#        self.w(u'</button>')
#        self.w(u'<span class="caret"></span>')
#        self.w(u'</div>')
#
#        # GCA block
#        # INTRO BLOCK
#        self.w(u'<div id="doc_EPI_GCA" class="collapse">')
#        self.w(u'In this Global Cognitive Assessment tasks, the subjects under'
#               'go a set of stimuli intended to highlight some specific brain '
#               'areas. Events are modeled as zero duration Dirac, convolved wi'
#               'th a standard Hemodynamic Response Function. Except for the re'
#               'corded motor responses, all other design-matrix columns should'
#               'be fairly similar between subjects.')
#        self.w(u'<h2>Behavioural-files input available</h2>')
#        self.w(u'4D fMRI sequence of 140 volumes, rtime 2.2s.<br>Behavioural f'
#               'iles (cga_*.csv) first few lines are pasted below:<br><br>')
#
#        self.w(u'<pre><code>')
#        self.w(u'GLOBAL_COGNITIVE_ASSESSMENT_TASK task 01.01.1900 19:46:55 Sub'
#               'ject ID: 000014185243 Task type: Scanning')
#        self.w(u'<div style="max-width:100%; overflow-x: scroll;">')
#        self.w(u'<table>')
#        self.w(u'<tr>')
#        self.w(u'<td>Trial</td>')
#        self.w(u'<td>Trial Category<td>')
#        self.w(u'<td>Trial Start Time (Onset)</td>')
#        self.w(u'<td>Pre-determined onset</td>')
#        self.w(u'<td>Stimulus Presented</td>')
#        self.w(u'<td>Stimulus presentation time</td>')
#        self.w(u'<td>Response made by subject</td>')
#        self.w(u'<td>Pre-determined Jitter</td>')
#        self.w(u'<td>Time response made</td>')
#        self.w(u'<td>Scanner Pulse</td>')
#        self.w(u'</tr>')
#        self.w(u'<tr>')
#        self.w(u'<td>1</td>')
#        self.w(u'<td>VISUAL_MATHS</td>')
#        self.w(u'<td>0</td>')
#        self.w(u'<td>0</td>')
#        self.w(u'<td>Rechne elf minus drei</td>')
#        self.w(u'<td>10</td>')
#        self.w(u'<td>B B B C C</td>')
#        self.w(u'<td>200</td>')
#        self.w(u'<td>0</td>')
#        self.w(u'<td>2187</td>')
#        self.w(u'</tr>')
#        self.w(u'</table>')
#
#        self.w(u'CGLOBAL_COGNITIVE_ASSESSMENT_TASK task 01/01/00 19:46 Subject'
#               'ID: 000014185243 Task type: Scanning')
#        self.w(u'<table>')
#        self.w(u'<tr>')
#        self.w(u'<td>Trial</td>')
#        self.w(u'<td>Trial Category<td>')
#        self.w(u'<td>Trial Start Time (Onset)</td>')
#        self.w(u'<td>Pre-determined onset</td>')
#        self.w(u'<td>Stimulus Presented</td>')
#        self.w(u'<td>Stimulus presentation time</td>')
#        self.w(u'<td>Response made by subject</td>')
#        self.w(u'<td>Pre-determined Jitter</td>')
#        self.w(u'<td>Time response made</td>')
#        self.w(u'<td>Scanner Pulse</td>')
#        self.w(u'</tr>')
#
#        self.w(u'<tr>')
#        self.w(u'<td>1</td>')
#        self.w(u'<td>VISUAL_MATHS</td>')
#        self.w(u'<td>0</td>')
#        self.w(u'<td>0</td>')
#        self.w(u'<td>Rechne elf minus drei</td>')
#        self.w(u'<td>10</td>')
#        self.w(u'<td>B B B C C</td>')
#        self.w(u'<td>200</td>')
#        self.w(u'<td>0</td>')
#        self.w(u'<td>2187</td>')
#        self.w(u'</tr><tr>')
#        self.w(u'<td>2</td>')
#        self.w(u'<td>VISUAL_MATHS</td>')
#        self.w(u'<td>2853</td>')
#        self.w(u'<td>2400</td>')
#        self.w(u'<td>Rechne sechzehn minus zwei</td>')
#        self.w(u'<td>2860</td>')
#        self.w(u'<td>1100</td>')
#        self.w(u'<td>0</td>')
#        self.w(u'<td>4390</td>')
#        self.w(u'</tr><tr>')
#        self.w(u'<td>3</td>')
#        self.w(u'<td>REST</td>')
#        self.w(u'<td>5700</td>')
#        self.w(u'<td>5700</td>')
#        self.w(u'<td>800</td>')
#        self.w(u'<td>0</td>')
#        self.w(u'<td>6581</td>')
#        self.w(u'</tr><tr>')
#        self.w(u'<td>4</td>')
#        self.w(u'<td>HORIZONTAL_CHECKERBOARD 8700</td>')
#        self.w(u'<td>8700</td>')
#        self.w(u'<td>8704</td>')
#        self.w(u'<td>500</td>')
#        self.w(u'<td>0</td>')
#        self.w(u'<td>11000</td>')
#        self.w(u'</tr><tr>')
#        self.w(u'<td>5</td>')
#        self.w(u'<td>PRESS_RIGHT_AUDITORY</td>')
#        self.w(u'<td>11400</td>')
#        self.w(u'<td>11400</td>')
#        self.w(u'<td>click3Right.wav 11413</td>')
#        self.w(u'<td>1400</td>')
#        self.w(u'<td>0</td>')
#        self.w(u'<td>17989</td>')
#        self.w(u'</tr><tr>')
#        self.w(u'<td>6</td>')
#        self.w(u'<td>LISTEN_SENTENCE 17989</td>')
#        self.w(u'<td>15000</td>')
#        self.w(u'<td>3.wav</td>')
#        self.w(u'<td>18002</td>')
#        self.w(u'<td>800</td>')
#        self.w(u'<td>0</td>')
#        self.w(u'<td>17989</td>')
#        self.w(u'</tr><tr>')
#        self.w(u'<td>7</td>')
#        self.w(u'<td>PRESS_RIGHT_VISUAL</td>')
#        self.w(u'<td>18020</td>')
#        self.w(u'<td>18000</td>')
#        self.w(u'<td>Druecke dreimal die rechte Taste</td>')
#        self.w(u'<td>18028</td>')
#        self.w(u'<td>C C C</td>')
#        self.w(u'<td>500</td>')
#        self.w(u'<td>20813</td>')
#        self.w(u'<td>19798</td>')
#        self.w(u'</tr>')
#        self.w(u'</table>')
#
#        self.w(u'</div>')
#
#        self.w(u'</pre></code>')
#        self.w(u'<br>')
#        self.w(u'Note : Time column may restart from 0, in this case everythin'
#               'g before is assumed to be pre-tests and discarded. This also a'
#               'pplies to other runs.')
#
#        self.w(u'<h2>Model</h2>')
#
#        self.w(u'The model is straightforward, using one regressor per conditi'
#               'on type. The events starting time are the one corresponding to'
#               ' the Stimulus Presentation, except for motor events which have'
#               ' explicit recorded values.')
#
#        self.w(u'<pre><code>')
#        self.w(u"StimTime = Stimulus_presentation_time / 1000.")
#        self.w(u"ResponseTime = Time_response_made / 1000.")
#        self.w(u"Auditory_math = StimTime[Trial_Category == 'AUDITORY_MATHS']")
#        self.w(u"Visual_math = StimTime[Trial_Category == 'VISUAL_MATHS']")
#        self.w(u"Listen_sentences = StimTime[Trial_Category == 'LISTEN_SENTEN"
#               "CE']")
#        self.w(u"Read_sentences = StimTime[Trial_Category == 'READ_SENTENCE']")
#        self.w(u"Motor_left = ResponseTime[left_press]")
#        self.w(u"Motor_right = ResponseTime[right_press]")
#        self.w(u"Press_visual = StimTime[(Trial_Category == 'PRESS_LEFT_VISUAL"
#               "') | (Trial_Category == 'PRESS_RIGHT_VISUAL')]")
#        self.w(u"Press_auditory = StimTime[(Trial_Category=='PRESS_LEFT_AUDITO"
#               "RY') |")
#        self.w(u"(Trial_Category=='PRESS_RIGHT_AUDITORY')]")
#        self.w(u"HCheckerboard = StimTime[(Trial_Category == 'HORIZONTAL_CHECK"
#               "ERBOARD')]")
#        self.w(u"VCheckerboard = StimTime[(Trial_Category == 'VERTICAL_CHECKER"
#               "BOARD')]")
#
#        self.w(u'</pre></code>')
#
#        self.w(u'<br>In case an event is not estimable (no occurrence of the c'
#               'ondition), the contrast is replaced by a dummy file to maintai'
#               'n correct file ordering, and the header'
#               "'s"
#               ' "description" field '
#               'is updated to "unestimable", as described in the overview sect'
#               'ion before.<br><br>')
#
#        self.w(u'<center><img src="{0}" alt="models"/>'
#               '</center>'.format(self._cw.data_url(
#                   "images/doc/GCA_model.png")))
#
#        self.w(u'<h2>Contrasts</h2>')
#        self.w(u'The following contrast maps are currently available:')
#        self.w(u'<ol>')
#        self.w(u"<li>'Auditory_math'</li>")
#        self.w(u"<li>'Visual_math'</li>")
#        self.w(u"<li>'Listen_sentences'</li>")
#        self.w(u"<li>'Read_sentences'</li>")
#        self.w(u"<li>'Motor_left'</li>")
#        self.w(u"<li>'Motor_right'</li>")
#        self.w(u"<li>'Press_visual'</li>")
#        self.w(u"<li>'Press_auditory'</li>")
#        self.w(u"<li>'HCheckerboard'</li>")
#        self.w(u"<li>'VCheckerboard'</li>")
#        self.w(u"<li>'Auditory' <em><font color='grey'>('Auditory_math' + 'Lis"
#               "ten_sentences' +"
#               " Press_auditory')</font></em></li>")
#        self.w(u"<li>'Visual' <em><font color='grey'>('Visual_math' + 'Read_se"
#               "ntences' + 'Press_visua"
#               "l' + 'HCheckerboard' + 'VCheckerboard')</font></em></li>")
#        self.w(u"<li>'Auditory - Visual' <em><font color='grey'>('Auditory_mat"
#               "h' + 'Listen_sentences'"
#               " + 'Press_auditory' - 'Visual_math' - 'Read_sentences' - 'Pres"
#               "s_visual' - 'HCheckerboard' - 'VCheckerboard')</font></em>"
#               "</li>")
#        self.w(u"<li>'Visual - Auditory' <em><font color='grey'>(- 'Auditory -"
#               " Visual')</font></em></li>")
#        self.w(u"<li>'Motor L - R' <em><font color='grey'>('Motor_left' - 'Mot"
#               "or_right')</font></em></li>")
#        self.w(u"<li>'Motor R - L' <em><font color='grey'>(- 'Motor L - R')</f"
#               "ont></em></li>")
#        self.w(u"<li>'Motor L + R' <em><font color='grey'>('Motor_left' + 'Mot"
#               "or_right')</font></em></li>")
#        self.w(u"<li>'Computation' <em><font color='grey'>('Auditory_math' + '"
#               "Visual_math')</font></em></li>")
#        self.w(u"<li>'Sentences' <em><font color='grey'>('Listen_sentences' + "
#               "'Read_sentences')</font></em></li>")
#        self.w(u"<li>'Sentences - Computation' <em><font color='grey'>('Listen"
#               "_sentences' + 'Read_sen"
#               "tences' - 'Auditory_math' - 'Visual_math')</font></em></li>")
#        self.w(u"<li>'Computation - Sentences' <em><font color='grey'>(- 'Sent"
#               "ences - Computation')</font></em></"
#               "li>")
#        self.w(u"<li>'AudioComputation - AudioSentences' <em><font color='grey"
#               "'>('Auditory_math' - 'L"
#               "isten_sentences')</font></em></li>")
#        self.w(u"<li>'VisualComputation - VisualSentences' <em><font color='gr"
#               "ey'>('Visual_math' - 'R"
#               "ead_sentences')</font></em></li>")
#        self.w(u"<li>'Motor - Cognitive' <em><font color='grey'>('Motor L + R'"
#               " - 'Sentences' - 'Compu"
#               "tation')</font></em></li>")
#        self.w(u"<li>'Cognitive - Motor' <em><font color='grey'>(- 'Motor - C"
#               "ognitive')</font></em></li>")
#        self.w(u"<li>'Checkerboard H + V' <em><font color='grey'>('HCheckerboa"
#               "rd' + 'VCheckerboard')"
#               "</font></em></li>")
#        self.w(u"<li>'Checkerboard H - V' <em><font color='grey'>('HCheckerboa"
#               "rd' - 'VCheckerboard')</font></em><"
#               "/li>")
#        self.w(u"<li>'Checkerboard V - H' <em><font color='grey'>(- 'Checkerbo"
#               "ard H - V')</font></em></li>")
#        self.w(u"<li>'Visual - Checkerboard' <em><font color='grey'>('Visual_m"
#               "ath' + 'Read_sentences'"
#               " + 'Press_visual' - 'Checkerboard H + V')</font></em></li>")
#        self.w(u"<li>'Read - Checkerboards' <em><font color='grey'>('Read_sent"
#               "ences' - 'HCheckerboard"
#               "' - 'VCheckerboard')</font></em></li>")
#        self.w(u"<li>'Read - HCheckerboards' <em><font color='grey'>('Read_sen"
#               "tences' - 'HCheckerboar"
#               "d')</font></em></li>")
#        self.w(u'</ol>')
#
#        self.w(u'<h2>Comments</h2>')
#
#        self.w(u"The only potentially unestimable regressors are the motor res"
#               "ponses. The pie chart below shows the number of recorded motor"
#               " responses during the task, across ~943 subjects, for the four"
#               " conditions involving motor condition. The corresponding regre"
#               "ssor gets unestimable if 0 event occurs, and prevent computati"
#               "on of all contrast maps which depend on that regressor. (i.e. "
#               'not limited to "pure motor" only ; e.g. a "Visual" map involve'
#               "s Press_visual which is a motor event). The pie-chart colors h"
#               "ighlight the best cases (Green, meaning all 5 events were reco"
#               "rded) and worse cases (Red, meaning 0 events have been recorde"
#               "d) proportions. As it shows, auditory motor 145 stimuli seems "
#               "to contain more failure cases than Visual motor ones.")
#
#        self.w(u'<center><img src="{0}" alt="number of correclty-pressed event'
#               's, for 943 subjects" width="100%"/></center>'.format(
#                   self._cw.data_url("images/doc/GCA_comments.png")))
#
#        self.w(u'Subjects missing enough recorded motor events to fully estima'
#               'te the model seems to be unevenly distributed per acquisition '
#               "centre. We're in the process of investigating it, but it might"
#               " reflect bad auditory device in the most affected centres.")
#
#        self.w(u'<center><img src="{0}" alt="distribution of the ~90 subjects '
#               'lacking enough motor events (from ~850 subject)" width="60%"'
#               '/></center>'.format(
#                   self._cw.data_url("images/doc/GCA_comments_2.png")))
#
#        self.w(u'<h2>subject-specific notes or workaround</h2>')
#
#        self.w(u'<ul><li>Manually-fixed csv:</li>')
#        self.w(u'<ul>')
#        self.w(u'<li>000022053782</li>')
#        self.w(u'<li>000054552397</li>')
#        self.w(u'<li>000079848243</li>')
#        self.w(u'<li>000086071132</li>')
#        self.w(u'</ul>')
#        self.w(u'<li>Empty csv:</li>')
#        self.w(u'<ul>')
#        self.w(u'<li>160000027074970</li>')
#        self.w(u'<li>000012809392</li>')
#        self.w(u'<li>000078056005</li>')
#        self.w(u'</ul>')
#        self.w(u'<li>Not yet fixed:</li>')
#        self.w(u'<ul>')
#        self.w(u'<li>000083358101</li>')
#        self.w(u'</ul>')
#        self.w(u'<li>Response Time is always 0 :</li>')
#        self.w(u'<ul>')
#        self.w(u'<li>000099677574</li>')
#        self.w(u'<li>000031171219</li>')
#        self.w(u'<li>000087296615</li>')
#        self.w(u'</ul>')
#        self.w(u'</ul>')
#
#        self.w(u'<h2>Unestimable or Excluded contrast maps</h2>')
#
#        self.w(u'A Group-wide distribution (computed on 1017 subject) of unest'
#               'imable contrasts or excluded subjects. Unestimable covers cont'
#               'rasts whose lack of events prevented the estimation of the cor'
#               'responding parameter value, while <em>excluded</em> covers ima'
#               'ges which'
#               ' were dropped due to a too abnormal activation profile compute'
#               'd with the automatic QC procedure.')
#
#        self.w(u'<center><figure><img src="{0}" alt="Number of unestimable or '
#               'excluded subject for contrast of EPI_global" width="100%"'
#               '/>'.format(
#                   self._cw.data_url("images/doc/GCA_Unestimable.png")))
#
#        self.w(u'<figcaption>(Note that only contrast 1-31 are relevant on thi'
#               's picture - ontrast 32 refers to a testing case)</figcaption>'
#               '</figure></center>')
#        self.w(u'</div>')
#        # end GCA block
#
#        # SST subtitle
#        self.w(u'<div data-toggle="collapse" data-target="#doc_EPI_SST">')
#        self.w(u'<button type="button" class="btn btn-link">')
#        self.w(u'<center><h2><strong>SST – Stop and Signal Task (SST)</strong>'
#               '</h2></center>')
#        self.w(u'</button>')
#        self.w(u'<span class="caret"></span>')
#        self.w(u'</div>')
#
#        # SST block
#        # INTRO BLOCK
#        self.w(u'<div id="doc_EPI_SST" class="collapse">')
#        self.w(u'bla')
#
#        self.w(u'</div>')
#        # end of SST block
#
#        # MID subtitle
#        self.w(u'<div data-toggle="collapse" data-target="#doc_MID">')
#        self.w(u'<button type="button" class="btn btn-link">')
#        self.w(u'<center><h2><strong>MID – Modified Incentive Delay</strong>'
#               '</h2></center>')
#        self.w(u'</button>')
#        self.w(u'<span class="caret"></span>')
#        self.w(u'</div>')
#
#        # MID block
#        # INTRO BLOCK
#        self.w(u'<div id="doc_MID" class="collapse">')
#
#        self.w(u'<div id="doc_MID_pdf" style="height:800px;">')
#        self.w(u"<p>It appears you don't have Adobe Reader or PDF support in t"
#               'his web browser. <a href="{0}">Click here to download t'
#               'he PDF</a></p>'.format(self._cw.data_url('EPI_doc.pdf')))
#        self.w(u'</div>')
#
#        self.w(u'</div>')
#        # end of MID block
#
#        # FACE subtitle
#        self.w(u'<div data-toggle="collapse" data-target="#doc_EPI_FACE">')
#        self.w(u'<button type="button" class="btn btn-link">')
#        self.w(u'<center><h2><strong>FT – Face Task</strong>'
#               '</h2></center>')
#        self.w(u'</button>')
#        self.w(u'<span class="caret"></span>')
#        self.w(u'</div>')
#
#        # FACE block
#        # INTRO BLOCK
#        self.w(u'<div id="doc_EPI_FACE" class="collapse">')
#
#        self.w(u'<div id="doc_EPI_FACE_pdf" style="height:800px;">')
#        self.w(u"<p>It appears you don't have Adobe Reader or PDF support in t"
#               'his web browser. <a href="{0}">Click here to download t'
#               'he PDF</a></p>'.format(self._cw.data_url('EPI_doc.pdf')))
#        self.w(u'</div>')
#
#        self.w(u'</div>')
#        # end of FACE block
#
#        self.w(u'</div>')
#        self.w(u'</div>')
#
#        # DTI
#        self.w(u'<div class="panel panel-info">')
#        self.w(u'<div class="panel-heading">')
#        self.w(u'<div class="panel-title" ')
#        self.w(u'<h1><strong>Diffusion sequence</strong></h1>')
#        self.w(u'</div>')
#        # add download link
#        self.w(u'<a href="{0}"><button type="button">Download reference file ('
#               'pdf)</button></a>'.format(
#                   self._cw.data_url('diffusion_doc.pdf'),))
#        self.w(u'</div>')
#        self.w(u'<div class="panel-body">')
#        self.w(u'<div id="doc_DTI_pdf" style="height:500px;">')
#        self.w(u"<p>It appears you don't have Adobe Reader or PDF support in t"
#               'his web browser. <a href="{0}">Click here to download t'
#               'he PDF</a></p>'.format(self._cw.data_url('diffusion_doc.pdf')))
#        self.w(u'</div>')
#
#        self.w(u'</div>')
#
#        self.w(u'</div>')
#        self.w(u'</div>')
#
#        # JAVASCRIPTS
#        self.w(u'<script type="text/javascript">')
#
#        # DTI
#        self.w(u'var pdfOpen_params_dti = {'
#               'navpanes: 1,'
#               'view: "FitH",'
#               'pagemode: "thumbs",'
#               'page: 1'
#               '};')
#        # EPI MID
#        self.w(u'var pdfOpen_params_mid = {'
#               'navpanes: 1,'
#               'view: "FitH",'
#               'pagemode: "thumbs",'
#               'page: 11'
#               '};')
#        # EPI FACE
#        self.w(u'var pdfOpen_params_face = {'
#               'navpanes: 1,'
#               'view: "FitH",'
#               'pagemode: "thumbs",'
#               'page: 20'
#               '};')
#
#        # DTI
#        self.w(u'var pdfAttributes_dti = {{'
#               'url: "{0}",'
#               'pdfOpenParams: pdfOpen_params_dti'
#               '}};'.format(self._cw.data_url('diffusion_doc.pdf')))
#        # EPI MID
#        self.w(u'var pdfAttributes_mid = {{'
#               'url: "{0}",'
#               'pdfOpenParams: pdfOpen_params_mid'
#               '}};'.format(self._cw.data_url('EPI_doc.pdf')))
#        # EPI FACE
#        self.w(u'var pdfAttributes_face = {{'
#               'url: "{0}",'
#               'pdfOpenParams: pdfOpen_params_face'
#               '}};'.format(self._cw.data_url('EPI_doc.pdf')))
#
#        self.w(u'window.onload = function (){')
#        # DTI
#        self.w(u'var doc_dti = new PDFObject(pdfAttributes_dti);'
#               'doc_dti.embed("doc_DTI_pdf");')
#        # EPI MID
#        self.w(u'var doc_epi_mid = new PDFObject(pdfAttributes_mid);'
#               'doc_epi_mid.embed("doc_MID_pdf");')
#        # EPI FACE
#        self.w(u'var doc_epi_face = new PDFObject(pdfAttributes_face);'
#               'doc_epi_face.embed("doc_EPI_FACE_pdf");'
#
#               '};')

        self.w(u'</script>')


class Doc_smri(EntityStartupView):
    __regid__ = "doc_MRIData"
    title = "sMRI documentation"

    def call(self, **kwargs):
        self.w(u"<h1><center><strong>structural MRI documentaion</strong>"
               "<center></h1>")
        self.w(u"<h2>  T1 ADNI MPRAGE </h2>")
        self.w(u"Sed fruatur sane hoc solacio atque hanc insignem ignominiam, "
               "quoniam uni praeter se inusta sit, putet esse leviorem, dum "
               "modo, cuius exemplo se consolatur, eius exitum expectet, "
               "praesertim cum in Albucio nec Pisonis libidines nec audacia "
               "Gabini fuerit ac tamen hac una plaga conciderit, ignominia "
               "senatus.")


class Doc_fmri(NullView):
    __regid__ = "doc_FMRIData"
    title = "fMRI documentation"
    templatable = False

    def call(self, **kwargs):

        page = u"""
        <!DOCTYPE html>
        <html xmlns:cubicweb="http://www.cubicweb.org" lang="en">
        <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=8" />
        """

        page += '<link rel="shortcut icon" href="{0}"/>'.format(
            self._cw.data_url("favicon.ico"))
        page += '<title>fMRI documentation (Imagen Database)</title>'
        page += '<script type="text/javascript" src="{0}"></script>'.format(
            self._cw.data_url("pdfobject.js"))
        page += "</head><body>"

        self.w(page)
        self.w(u"<p>It appears you don't have Adobe Reader or PDF support in "
               'this web browser. <a href="{0}">Click here to download '
               'the PDF</a></p>'.format(self._cw.data_url('EPI_doc.pdf')))
        self.w(u"</body>")
        self.w(u'<footer id="pagefooter" role="contentinfo">'
               '<a href="http://www.imagen-europe.com/">Imagen</a> | '
               '<a href="http://i2bm.cea.fr/dsv/i2bm/NeuroSpin/">NeuroSpin</a>'
               '</footer>')
        self.w(u'</html>')

        # JAVASCRIPTS
        self.w(u'<script type="text/javascript">')

        self.w(u'var pdfOpen_params_popup = {'
               'navpanes: 1,'
               'page: 1'
               '};')

        self.w(u'var pdfAttributes_popup = {{'
               'url: "{0}",'
               'pdfOpenParams: pdfOpen_params_popup'
               '}};'.format(self._cw.data_url('EPI_doc.pdf')))

        self.w(u'window.onload = function (){')
        self.w(u'var doc_popup = new PDFObject(pdfAttributes_popup);'
               'doc_popup.embed();'
               '};')
        self.w(u'</script>')


def registration_callback(vreg):
    vreg.register(QC_central)
    vreg.register(Doc_smri)
    vreg.register(Doc_fmri)
