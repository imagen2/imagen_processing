# -*- coding: utf-8 -*-
# copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# copyright 2014 CEA (Saclay, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-suivimp views/forms/actions/components for web ui"""

from cubicweb.web.views import uicfg

_pvs = uicfg.primaryview_section
_pvdc = uicfg.primaryview_display_ctrl

uicfg.autoform_section.hide_fields('CWSearch', ('result', 'expiration_date', 'rset_type'))


###############################################################################
### SUBJECT ###################################################################
###############################################################################
# Studies
_pvs.tag_subject_of(('Subject', 'related_studies', 'Study'), 'attributes')
# Related therapies
_pvs.tag_subject_of(('Subject', 'related_therapies', 'Therapy'), 'attributes')
# Related diseases
_pvs.tag_subject_of(('Subject', 'related_diseases', 'Disease'), 'attributes')
# Measures
_pvs.tag_object_of(('GenomicMeasure', 'concerns', 'Subject'), 'relations')
_pvdc.tag_object_of(('GenomicMeasure', 'concerns', 'Subject'),
                      {'vid': 'outofcontext',
                       'label': _('Measures')})
# Admissions
_pvs.tag_object_of(('Admission', 'admission_of', 'Subject'), 'relations')
_pvdc.tag_object_of(('Admission', 'admission_of', 'Subject'),
                    {'vid': 'admission-view', 'order': 0, 'label': _('Admissions')})


###############################################################################
### STUDY #####################################################################
###############################################################################
# Data filepath
_pvs.tag_attribute(('Study', 'data_filepath'), 'hidden')
# Themes
_pvs.tag_subject_of(('Study', 'themes', 'Theme'), 'attributes')
# Related studies / Subject
_pvs.tag_object_of(('Subject', 'related_studies', 'Study'), 'relations')
_pvdc.tag_object_of(('Subject', 'related_studies', 'Study'),
                    {'label': _('Subjects'), 'vid': 'outofcontext'})
# Related study / Subject
_pvs.tag_object_of(('Subject', 'related_study', 'Study'), 'relations')
_pvdc.tag_object_of(('Subject', 'related_study', 'Study'),
                    {'label': _('Measures'), 'vid': 'outofcontext'})
# Studies
_pvs.tag_subject_of(('Study', 'substudy_of', 'Study'), 'attributes')
_pvs.tag_object_of(('Study', 'substudy_of', 'Study'), 'attributes')


###############################################################################
### THERAPY ###################################################################
###############################################################################
_pvs.tag_subject_of(('*', 'therapy_for', 'Disease'), 'attributes')
_pvs.tag_object_of(('*', 'related_therapies', 'Therapy'), 'attributes')
_pvs.tag_subject_of(('Therapy', 'therapy_for', '*'), 'attributes')
_pvs.tag_object_of(('*', 'taken_in_therapy', 'Therapy'), 'relations')
_pvdc.tag_object_of(('*', 'taken_in_therapy', 'Therapy'), {'vid': 'drugtake-table-view'})


###############################################################################
### CENTER ####################################################################
###############################################################################
# Name
_pvs.tag_attribute(('Center', 'name'), 'hidden')
# Assessment
_pvs.tag_subject_of(('Center', 'holds', 'Assessment'), 'relations')
_pvdc.tag_subject_of(('Center', 'holds', 'Assessment'), {'label': _('Assessment'), 'vid': 'table'})
# Device
_pvdc.tag_object_of(('Device', 'hosted_by', 'Center'), {'label': _('Devices'), 'vid': 'list'})
# subjects
_pvdc.display_rset('Center', 'relations',
                   {'rql': 'Any S WHERE S concerned_by Y, X holds Y',
                    'vid': 'table',
                    'order': 1,
                    'label': _('Subjects')})


###############################################################################
### DEVICE ####################################################################
###############################################################################
# Name
_pvs.tag_attribute(('Device', 'name'), 'hidden')
# Center
_pvs.tag_subject_of(('Device', 'hosted_by', 'Center'), 'attributes')
# Measures
_pvdc.tag_object_of(('*', 'uses_device', 'Device'),
                    {'label': _('Generated measures'), 'vid': 'outofcontext'})


###############################################################################
### ASSESSMENT ################################################################
###############################################################################
# Remove attributes in view
_pvs.tag_attribute(('Assessment', 'r_related_study'), 'hidden')
# Protocol
#_pvs.tag_subject_of(('Assessment', 'protocols', 'Protocol'), 'attributes')
# Subject
_pvs.tag_object_of(('Subject', 'concerned_by', 'Assessment'), 'attributes')
# Measures
_pvs.tag_subject_of(('Assessment', 'generates', '*'), 'relations')
_pvdc.tag_subject_of(('Assessment', 'generates', '*'),
                     {'vid': 'outofcontext', 'label': _('Generated measures')})
_pvs.tag_subject_of(('Assessment', 'uses', '*'), 'relations')
_pvdc.tag_subject_of(('Assessment', 'uses', '*'),
                     {'vid': 'outofcontext', 'label': _('Used measures')})


###############################################################################
### SCOREDEFINITION ###########################################################
###############################################################################
_pvs.tag_object_of(('ScoreValue', 'definition', 'ScoreDefinition'), 'relations')
_pvdc.tag_object_of(('ScoreValue', 'definition', 'ScoreDefinition'),
                    {'vid': 'scorevalue-incontext-table-view', 'label': _('Scores')})


###############################################################################
### SCOREGROUP ################################################################
###############################################################################
_pvs.tag_object_of(('*', 'related_score_groups', 'ScoreGroup'), 'attributes')
_pvs.tag_subject_of(('ScoreGroup', 'protocols', '*'), 'attributes')
_pvs.tag_subject_of(('ScoreGroup', 'scores', '*'), 'relations')
_pvdc.tag_subject_of(('ScoreGroup', 'scores', '*'),
                     {'label': _('Scores'), 'vid': 'scorevalue-outofcontext-table-view'})


###############################################################################
### INVESTIGATOR ##############################################################
###############################################################################
_pvs.tag_object_of(('Assessment', 'conducted_by', 'Investigator'), 'relations')
_pvdc.tag_object_of(('Assessment', 'conducted_by', 'Investigator'),
                    {'vid': 'list', 'label': _('Assessments conducted by this investigator')})


###############################################################################
### GENERICTERUN ##############################################################
###############################################################################
# Instance
_pvs.tag_subject_of(('GenericTestRun', 'instance_of', '*'), 'attributes')
# Concerns
_pvs.tag_subject_of(('GenericTestRun', 'concerns', 'Subject'), 'attributes')
# Measures
_pvs.tag_object_of(('*', 'measure', 'GenericTestRun'), 'relations')
_pvdc.tag_object_of(('*', 'measure', 'GenericTestRun'),
                    {'vid': 'scorevalue-outofcontext-tableview',
                     'label': _('score')})
_pvdc.tag_subject_of(('GenericTestRun', 'external_resources', '*'),
                     {'vid': 'list', 'label': _('External Resources')})


###############################################################################
### GENERICTEST ###############################################################
###############################################################################
_pvdc.tag_object_of(('*', 'instance_of', 'GenericTest'),
                    {'vid': 'list', 'label': _('Test runs')})


###############################################################################
### EXTERNALRESOURCE ##########################################################
###############################################################################
_pvs.tag_subject_of(('ExternalResource', 'related_study', '*'), 'attributes')
_pvdc.tag_subject_of(('ExternalResource', 'related_study', '*'),
                     {'vid': 'incontext', 'label': _('Study')})


###############################################################################
### GENOMICMEASURE ############################################################
###############################################################################
_pvs.tag_object_of(('*', 'generates', 'GenomicMeasure'), 'attributes')
_pvs.tag_subject_of(('GenomicMeasure', 'concerns', 'Subject'), 'attributes')
_pvs.tag_subject_of(('GenomicMeasure', 'related_study', 'Study'), 'attributes')
_pvs.tag_subject_of(('GenomicMeasure', 'platform', '*'), 'attributes')
_pvs.tag_object_of(('*', 'related_measure', 'GenomicMeasure'), 'relations')
_pvdc.tag_object_of(('*', 'related_measure', 'GenomicMeasure'),
                    {'label': _('Results'), 'vid': 'genmeas-table-view'})


###############################################################################
### GENE ######################################################################
###############################################################################
# Chromosomes
_pvs.tag_subject_of(('Gene', 'chromosomes', '*'), 'attributes')
_pvdc.tag_subject_of(('Gene', 'chromosomes', '*'),
                     {'vid': 'incontext', 'label': _('Chromosomes')})
# CGH results
_pvs.tag_object_of(('*', 'genes', 'Gene'), 'hidden')
_pvdc.display_rset('Gene', 'relations',
                   {'rql': 'Any CGH WHERE CGH genomic_region GR, GR genes X',
                    'vid': 'region-genmeas-table-view',
                    'order': 1,
                    'label': _('CGH results')})
# Sequencing results
_pvs.tag_object_of(('*', 'related_gene', 'Gene'), 'relations') # Mutation
_pvdc.tag_object_of(('*', 'related_gene', 'Gene'),
                    {'label': _('Sequencing results'),
                     'vid': 'gene-genmeas-table-view'})


###############################################################################
### GENOMICREGION #############################################################
###############################################################################
# Genes
_pvs.tag_subject_of(('GenomicRegion', 'genes', '*'), 'attributes')
# CGH results
_pvs.tag_object_of(('*', 'genomic_region', 'GenomicRegion'), 'relations')
_pvdc.tag_object_of(('*', 'genomic_region', 'GenomicRegion'),
                    {'label': _('CGH results'),
                     'vid': 'region-genmeas-table-view'})


###############################################################################
### QUESTIONNAIRERUN ##########################################################
###############################################################################
# Instance of
_pvs.tag_subject_of(('QuestionnaireRun', 'instance_of', '*'), 'attributes')
_pvdc.tag_subject_of(('QuestionnaireRun', 'instance_of', '*'), {'vid': 'incontext'})
# Subjects
_pvs.tag_subject_of(('QuestionnaireRun', 'concerns', '*'), 'attributes')
_pvdc.tag_subject_of(('QuestionnaireRun', 'concerns', '*'), {'vid': 'incontext'})
# Assessment
_pvs.tag_object_of(('*', 'generates', 'QuestionnaireRun'), 'attributes')
_pvdc.tag_object_of(('*', 'generates', 'QuestionnaireRun'), {'vid': 'incontext'})
# Additional scores
_pvs.tag_object_of(('*', 'measure', 'QuestionnaireRun'), 'relations')
_pvdc.tag_object_of(('*', 'measure', 'QuestionnaireRun'), {'vid': 'list'})
# Additional resources
_pvs.tag_subject_of(('QuestionnaireRun', 'external_resources', '*'), 'relations')
_pvdc.tag_subject_of(('QuestionnaireRun', 'external_resources', '*'), {'vid': 'list'})
# Answers
_pvs.tag_object_of(('*', 'questionnaire_run', 'QuestionnaireRun'), 'relations')
_pvdc.tag_object_of(('*', 'questionnaire_run', 'QuestionnaireRun'),
                    {'vid': 'answer-outofcontext-table-view'})


###############################################################################
### QUESTIONNAIRE #############################################################
###############################################################################
# Questionnaire runs
_pvs.tag_object_of(('*', 'instance_of', 'Questionnaire'), 'relations')
_pvdc.tag_object_of(('*', 'instance_of', 'Questionnaire'), {'vid': 'table'})
# Questions
_pvs.tag_object_of(('*', 'questionnaire', 'Questionnaire'), 'relations')
_pvdc.tag_object_of(('*', 'questionnaire', 'Questionnaire'), {'vid': 'question-table-view'})


###############################################################################
### QUESTION ##################################################################
###############################################################################
# Questionnaire
_pvs.tag_subject_of(('Question', 'questionnaire', '*'), 'attributes')
_pvdc.tag_subject_of(('Question', 'questionnaire', '*'), {'vid': 'incontext'})
# Answers
_pvs.tag_object_of(('*', 'question', 'Question'), 'relations')
_pvdc.tag_object_of(('*', 'question', 'Question'), {'vid': 'answer-incontext-table-view'})


###############################################################################
### SCAN ######################################################################
###############################################################################
_pvs.tag_subject_of(('Scan', 'concerns', '*'), 'attributes')
_pvs.tag_subject_of(('Scan', 'uses_device', '*'), 'attributes')
_pvs.tag_object_of(('*', 'generates', 'Scan'), 'attributes')
_pvs.tag_subject_of(('Scan', 'has_data', '*'), 'relations')
_pvdc.tag_subject_of(('Scan', 'has_data', '*'),
                     {'vid': 'scan-data-view', 'label': _(' ')})
_pvs.tag_object_of(('*', 'external_resources', 'ExternalResource'), 'relations')


###############################################################################
### DRUG ######################################################################
###############################################################################
_pvs.tag_object_of(('DrugTake', 'drug', '*'), 'relations')
_pvdc.tag_object_of(('DrugTake', 'drug', '*'), {'vid': 'drugtake-table-view'})


###############################################################################
### DISEASE ###################################################################
###############################################################################
_pvs.tag_object_of(('*', 'related_diseases', 'Disease'), 'relations')
_pvdc.tag_object_of(('*', 'related_diseases', 'Disease'), {'vid': 'table'})
_pvs.tag_object_of(('Diagnostic', 'diagnosed_disease', 'Disease'), 'relations')


###############################################################################
### BODYLOCATION ##############################################################
###############################################################################
_pvs.tag_subject_of(('Subject', 'related_lesions', '*'), 'attributes')
_pvs.tag_subject_of(('Disease', 'lesion_of', '*'), 'relations')
_pvs.tag_subject_of(('Drug', 'acts_on', '*'), 'relations')
_pvs.tag_subject_of(('BodyLocation', 'subpart_of', '*'), 'attributes')
_pvs.tag_object_of(('Diagnostic', 'diagnostic_location', 'BodyLocation'), 'relations')
_pvs.tag_object_of(('Diagnostic', 'metastatic_locations', 'BodyLocation'), 'relations')
