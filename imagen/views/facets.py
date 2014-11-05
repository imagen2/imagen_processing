#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# CW import
from cubicweb.web import facet
from cubicweb.selectors import is_instance
from cubes.neuroimaging.views.facets import ScanLabelFacet
from cubes.brainomics.views.facets import (
    MeasureAgeFacet, MeasureHandednessFacet, MeasureGenderFacet)

############################################################################
# FACETS 
############################################################################

class QuestionnaireRunQuestionnaireFacet(facet.RQLPathFacet):
    __regid__ = 'qr-questionnaire-facet'
    __select__ = is_instance('QuestionnaireRun')
    path = ['X r_instance_of Y', 'Y name N']
    order = 1
    filter_variable = 'N'
    title = _('Questionnaire')


#class QuestionnaireRunSubjectFacet(facet.RQLPathFacet):
#    __regid__ = 'qr-subject-facet'
#    __select__ = is_instance('QuestionnaireRun')
#    path = ['X r_concerns Y', 'Y code_in_study C']
#    order = 1
#    filter_variable = 'C'
#    title = _('Subject')


#class QuestionnaireRunAssessmentFacet(facet.RQLPathFacet):
#    __regid__ = 'qr-assessment-facet'
#    __select__ = is_instance('QuestionnaireRun')
#    path = ['X r_concerns Y', 'Y concerned_by Z', 'Z timepoint T']
#    order = 2
#    filter_variable = 'T'
#    title = _('Time point')

class ScanFormatFacet(facet.AttributeFacet):
    __regid__ = 'scan-format-facet'
    __select__ = facet.RelationAttributeFacet.__select__ & is_instance('Scan')
    rtype = 'format'
    title = _('Format')


class TimepointFacet(facet.RQLPathFacet):
    __regid__ = "timepoint-facet"
    __select__ = is_instance("Scan", "QuestionnaireRun")
    path = ["X in_assessment A", "A timepoint T"]
    order = 1
    filter_variable = "T"
    title = _("Timepoints")


class SubjectFacet(facet.RQLPathFacet):
    __regid__ = "subject-facet"
    __select__ = is_instance("Scan", "QuestionnaireRun")
    path = ["X r_concerns S", "S code_in_study C"]
    order = 3
    filter_variable = "C"
    title = _("Subjects")


class AssessmentTimepointFacet(facet.RQLPathFacet):
    __regid__ = "assessment-timepoint-facet"
    __select__ = is_instance("Assessment")
    path = ["X timepoint T"]
    order = 1
    filter_variable = "T"
    title = _("Timepoints")


class AssessmentSubjectFacet(facet.RQLPathFacet):
    __regid__ = "assessment-subject-facet"
    __select__ = is_instance("Assessment")
    path = ["S concerned_by X", "S code_in_study C"]
    order = 4
    filter_variable = "C"
    title = _("Subjects")


##############################################################################
# GenomicMeasure facets
##############################################################################

class GMChromsetFacet(facet.AttributeFacet):
    __regid__ = 'genomicmeasure-chromset-facet'
    __select__ = facet.RelationAttributeFacet.__select__ & is_instance('GenomicMeasure')
    rtype = 'chromset'
    title = _('Chromosome sets')


class GMQCFacet(facet.AttributeFacet):
    __regid__ = 'genomicmeasure-qc-facet'
    __select__ = facet.RelationAttributeFacet.__select__ & is_instance('GenomicMeasure')
    rtype = 'completed'
    title = _('QC genetics')


class GMformatFacet(facet.AttributeFacet):
    __regid__ = 'genomicmeasure-format-facet'
    __select__ = facet.RelationAttributeFacet.__select__ & is_instance('GenomicMeasure')
    rtype = 'format'
    title = _('Formats')


class GMSubjectFacet(facet.RQLPathFacet):
    __regid__ = "genomicmeasure-subject-facet"
    __select__ = is_instance("GenomicMeasure")
    path = ["X related_subjects S", "S code_in_study C"]
    order = 4
    filter_variable = "C"
    title = _("Subjects")


##############################################################################
# Factory
##############################################################################

def registration_callback(vreg):

    vreg.register(QuestionnaireRunQuestionnaireFacet)
    vreg.register(TimepointFacet)
    vreg.register(SubjectFacet)

    vreg.register(ScanFormatFacet)

    vreg.register(AssessmentTimepointFacet)
    vreg.register(AssessmentSubjectFacet)

    vreg.register(GMChromsetFacet)
    vreg.register(GMQCFacet)
    vreg.register(GMformatFacet)
    vreg.register(GMSubjectFacet)

    vreg.unregister(ScanLabelFacet)
    vreg.unregister(MeasureAgeFacet)
    vreg.unregister(MeasureHandednessFacet)
    vreg.unregister(MeasureGenderFacet)
