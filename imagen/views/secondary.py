#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

from cubicweb.predicates import is_instance
from cubicweb.view import EntityView

from cubes.medicalexp.views.secondary import (
    ScoreValueOutOfContextView, ExternalResourcesSummaryView,
    AssessmentOutOfContextView, SubjectOutOfContextView)
from cubes.questionnaire.views.outofcontext import (
    QuestionnaireRunOutOfContextView)
from cubes.neuroimaging.views.secondary import ScanOutOfContextView
from cubes.genomics.views.outofcontext import GenomicMeasureOutOfContextView

###############################################################################
# Scans 
###############################################################################
class ImagenScanOutOfContextView(EntityView):
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("Scan")

    def cell_call(self, row, col):
        """ Create the NSScanOutOfContextView view line by line
        """
        # Get the scan entity
        entity = self.cw_rset.get_entity(row, col)

        # Get the subject/study related entities
        subject = entity.r_concerns[0]
        #study = entity.related_study[0]

        # Get the scan image url
        image = u'<img alt="" src="%s">' %  self._cw.data_url(entity.symbol)

        # Create the div that will contain the list item
        self.w(u'<div class="ooview"><div class="well">')

        # Create a bootstrap row item
        self.w(u'<div class="row">')
        # > first element: the image
        self.w(u'<div class="col-md-8">')
        self.w(u'<div class="col-md-2"><p class="text-center">{0}</p></div>'.format(image))
        # > second element: the scan description + link
        self.w(u'<div class="col-md-10"><h4>{0}</h4>'.format(entity.view("incontext")))
        self.w(u'Type <em>{0}</em> - Fromat <em>{1}</em></div>'.format(entity.type, entity.format))
        self.w(u'</div>')
        # > third element: the see more button
        self.w(u'<div class="col-md-4">')
        self.w(u'<button class="btn btn-danger" type="button" style="margin-top:8px" data-toggle="collapse" data-target="#info-%s">' % row)
        self.w(u'See more')
        self.w(u'</button></div>')
        # Close row item
        self.w(u'</div>')

        # Get the scan description
        dtype_entity = entity.r_has_data[0]

        # Create a div that will be show or hide when the see more button is
        # clicked
        self.w(u'<div id="info-%s" class="collapse">' % row)
        self.w(u'<dl class="dl-horizontal">')
        # > image shape
        #self.w(u'<dt>Image Shape (x)</dt><dd>{0}</dd>'.format(
        #    dtype_entity.shape_x))
        #self.w(u'<dt>Image Shape (y)</dt><dd>{0}</dd>'.format(
        #    dtype_entity.shape_y))
        #self.w(u'<dt>Image Shape (z)</dt><dd>{0}</dd>'.format(
        #    dtype_entity.shape_z))
        # > image resolution
        if not dtype_entity.__class__.__name__ == "PROCESSINGData":
            self.w(u'<dt>Voxel resolution (x)</dt><dd>{0}</dd>'.format(
                dtype_entity.voxel_res_x))
            self.w(u'<dt>Voxel resolution (y)</dt><dd>{0}</dd>'.format(
                dtype_entity.voxel_res_y))
            self.w(u'<dt>Voxel resolution (z)</dt><dd>{0}</dd>'.format(
                dtype_entity.voxel_res_z))
            # > image TR
            self.w(u'<dt>Repetition time</dt><dd>{0}</dd>'.format(
                dtype_entity.tr))
            # > image TE
            self.w(u'<dt>Echo time</dt><dd>{0}</dd>'.format(
                dtype_entity.te))
            # > Scanner field
            #self.w(u'<dt>Scanner field</dt><dd>{0}</dd>'.format(
            #    dtype_entity.field))
        # > Realted entities
        self.w(u'<dt>Ralated subject</dt><dd>{0}</dd>'.format(
            subject.view("incontext")))
        #self.w(u'<dt>Ralated study</dt><dd>{0}</dd>'.format(
        #    study.view("incontext")))
        self.w(u'</div>')

        # Close list item
        self.w(u'</div></div>')


###############################################################################
# Assessment 
###############################################################################
class ImagenAssessmentOutOfContextView(EntityView):
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("Assessment")

    def cell_call(self, row, col):
        """ Create the NSAssessmentOutOfContextView view line by line
        """
        # Get the assessment entity
        entity = self.cw_rset.get_entity(row, col)

        # Get the subject/study/center related entities
        subject = entity.reverse_concerned_by[0]
        study = entity.r_related_study[0]
        center = entity.reverse_holds[0]
        run_items = []
        run_items.extend(entity.related_processing)
        run_items.extend(entity.uses)

        # Get the subject gender image url
        image = u'<img alt="" src="%s">' %  self._cw.data_url(entity.symbol)

        # Create the div that will contain the list item
        self.w(u'<div class="ooview"><div class="well">')

        # Create a bootstrap row item
        self.w(u'<div class="row">')
        # > first element: the image
        self.w(u'<div class="col-md-8">')
        self.w(u'<div class="col-md-2"><p class="text-center">{0}</p></div>'.format(image))
        # > second element: the scan description + link
        self.w(u'<div class="col-md-10"><h4>{0}</h4>'.format(entity.view("incontext")))
        self.w(u'Study <em>{0}</em> - Timepoint <em>{1}</em></div>'.format(
            study.name, entity.timepoint))
        self.w(u'</div>')
        # > third element: the see more button
        self.w(u'<div class="col-md-4">')
        self.w(u'<button class="btn btn-danger" type="button" style="margin-top:8px" data-toggle="collapse" data-target="#info-%s">' % row)
        self.w(u'See more')
        self.w(u'</button></div>')
        # Close row item
        self.w(u'</div>')

        # Create a div that will be show or hide when the see more button is
        # clicked
        self.w(u'<div id="info-%s" class="collapse">' % row)
        self.w(u'<dl class="dl-horizontal">')
        self.w(u'<dt>Acquisition center</dt><dd>{0}</dd>'.format(
            center.name))
        self.w(u'<dt>Gender</dt><dd>{0}</dd>'.format(
            subject.gender))
        self.w(u'<dt>Handedness</dt><dd>{0}</dd>'.format(
            subject.handedness))
        self.w(u'<dt>Age</dt><dd>{0}</dd>'.format(
            entity.age_of_subject))
        self.w(u'<dt>Identifier</dt><dd>{0}</dd>'.format(
            entity.identifier))
        self.w(u'<dt>Related runs</dt><dd>{0}</dd>'.format(
            " - ".join([x.view("incontext") for x in run_items])))
        self.w(u'</div>')

        # Close list item
        self.w(u'</div></div>')


###############################################################################
# Subject 
###############################################################################
class ImagenSubjectOutOfContextView(EntityView):
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("Subject")

    def cell_call(self, row, col):
        """ Create the NSSubjectOutOfContextView view line by line
        """
        # Get the assessment entity
        entity = self.cw_rset.get_entity(row, col)

        # Get the subject/study/center related entities
        assessment_items = entity.concerned_by

        # Get the subject gender image url
        image = u'<img alt="" src="%s">' %  self._cw.data_url(entity.symbol)

        # Create the div that will contain the list item
        self.w(u'<div class="ooview"><div class="well">')

        # Create a bootstrap row item
        self.w(u'<div class="row">')
        # > first element: the image
        self.w(u'<div class="col-md-8">')
        self.w(u'<div class="col-md-2"><p class="text-center">{0}</p></div>'.format(image))
        # > second element: the scan description + link
        self.w(u'<div class="col-md-10"><h4>{0}</h4>'.format(entity.view("incontext")))
        self.w(u'Gender <em>{0}</em> - Handedness <em>{1}</em></div>'.format(
            entity.gender, entity.handedness))
        self.w(u'</div>')
        # > third element: the see more button
        self.w(u'<div class="col-md-4">')
        self.w(u'<button class="btn btn-danger" type="button" '
                'style="margin-top:8px" data-toggle="collapse" '
                'data-target="#info-%s">' % row)
        self.w(u'See more')
        self.w(u'</button></div>')
        # Close row item
        self.w(u'</div>')

        # Create a div that will be show or hide when the see more button is
        # clicked
        self.w(u'<div id="info-%s" class="collapse">' % row)
        self.w(u'<dl class="dl-horizontal">')
        self.w(u'<dt>Related assessments</dt><dd>{0}</dd>'.format(
            " - ".join(['<a href="{0}">{1}</a>'.format(
                x.absolute_url(), x.identifier) for x in assessment_items])))
        # > create longitudinal summary views
        href = self._cw.build_url(
            "view", vid="highcharts-relation-summary-view",
            rql="Any A WHERE S eid '{0}', S concerned_by A".format(entity.eid),
            relation="uses", subject_attr="timepoint", object_attr="type",
            title="Acquisition status: {0}".format(entity.code_in_study))
        self.w(u'<dt>Acquisition summary</dt><dd><a href="{0}">'
                'status</a></dd>'.format(href))
        #href = self._cw.build_url(
        #    "view", vid="highcharts-relation-summary-view",
        #    rql="Any A WHERE S eid '{0}', S concerned_by A".format(entity.eid),
        #    relation="related_processing", subject_attr="timepoint",
        #    object_attr="tool", title="Processing status: {0}".format(entity.code_in_study))
        #self.w(u'<dt>Processing summary</dt><dd><a href="{0}">'
        #        'status</a></dd>'.format(href))
        #href = self._cw.build_url(
        #    "view", vid="questionnaire-longitudinal-measures",
        #    rql=("Any QR WHERE S eid '{0}', S concerned_by A, A uses QR, "
        #         "QR is QuestionnaireRun".format(entity.eid)),
        #    patient_id=entity.code_in_study)
        #self.w(u'<dt>Measure summary</dt><dd><a href="{0}">status</a>'
        #        '</dd>'.format(href))
        self.w(u'</div>')

        # Close list item
        self.w(u'</div></div>')


###############################################################################
# QuestionnaireRun 
###############################################################################
class ImagenQuestionnaireRunOutOfContextView(EntityView):
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("QuestionnaireRun")

    def cell_call(self, row, col):
        """ Create the NSQuestionnaireRunOutOfContextView view line by line
        """
        # Get the processing run entity
        entity = self.cw_rset.get_entity(row, col)

        # Get the subject/study/center related entities
        subject = entity.concerns[0]
        questionnaire = entity.instance_of[0]

        # Get the subject gender image url
        image = u'<img alt="" src="%s">' %  self._cw.data_url(entity.symbol)

        # Create the div that will contain the list item
        self.w(u'<div class="ooview"><div class="well">')

        # Create a bootstrap row item
        self.w(u'<div class="row">')
        # > first element: the image
        self.w(u'<div class="col-md-2"><p class="text-center">{0}</p></div>'.format(image))
        # > second element: the scan description + link
        self.w(u'<div class="col-md-4"><h4>{0}</h4>'.format(entity.view("incontext")))
        self.w(u'</div>')
        # > third element: the see more button
        self.w(u'<div class="col-md-3">')
        self.w(u'<button class="btn btn-danger" type="button" style="margin-top:8px" data-toggle="collapse" data-target="#info-%s">' % row)
        self.w(u'See more')
        self.w(u'</button></div>')
        # Close row item
        self.w(u'</div>')

        # Create a div that will be show or hide when the see more button is
        # clicked
        self.w(u'<div id="info-%s" class="collapse">' % row)
        self.w(u'<dl class="dl-horizontal">')
        self.w(u'<dt>Related questionnaire</dt><dd>{0}</dd>'.format(
            questionnaire.view("incontext")))
        self.w(u'<dt>Relted subject</dt><dd>{0}</dd>'.format(
            subject.view("incontext")))
        self.w(u'</div>')

        # Close list item
        self.w(u'</div></div>')


###############################################################################
# GenomicMeasure 
###############################################################################
class ImagenGenomicMeasureRunOutOfContextView(EntityView):
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("GenomicMeasure")

    def cell_call(self, row, col):
        """ Create the NSQuestionnaireRunOutOfContextView view line by line
        """
        # Get the processing run entity
        entity = self.cw_rset.get_entity(row, col)

        # Get the subject/study/center related entities
        platform = entity.platform[0]

        # Get the subject gender image url
        image = u'<img alt="" src="%s">' % entity.image_url

        # Create the div that will contain the list item
        self.w(u'<div class="ooview">')
        self.w(u'<div class="well">')

        # Create a bootstrap row item
        self.w(u'<div class="row">')
        # > first element: the image
        self.w(u'<div class="col-md-2"><p class="text-center">{0}</p></div>'.format(image))
        # > second element: the scan description + link
        self.w(u'<div class="col-md-4"><h4>{0}</h4>'.format(entity.view("incontext")))
        self.w(u'</div>')
        # Close row item
        self.w(u'</div>')
        # > third element: informations
        self.w(u'<dl class="dl-horizontal">')
        self.w(u'<dt>Type</dt><dd>{0}</dd>'.format(entity.type))
        self.w(u'<dt>Format</dt><dd>{0}</dd>'.format(entity.format))
        self.w(u'<dt>Platform</dt><dd>{0}</dd>'.format(platform.identifier))
        self.w(u'</dl>')

        # close container
        self.w(u'</div>')
        self.w(u'</div>')


###############################################################################
# ExternalResource
###############################################################################
class ImagenExternalResourceOutOfContextView(EntityView):
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("ExternalResource")

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<div class=row>\n')
        self.w(u'<div class="col-md-2">\n')
        #self.w(u'<h1>%s</h1>' % entity.symbol)
        self.w(u'</div>')
        self.w(u'<div class="col-md-8">\n')
        self.w(u'<h4><a href="%s">%s</a></h4>' % (entity.absolute_url(),
                                                  entity.dc_title()))
        #self.w(u'File path <em>%s</em> <br />' % entity.filepath)
        self.w(u'</div>')
        self.w(u'</div>')


###############################################################################
# Factory 
###############################################################################
def registration_callback(vreg):
    """ Update outofcontext views
    """
    vreg.unregister(ExternalResourcesSummaryView)
    vreg.register(ImagenExternalResourceOutOfContextView)
    vreg.register_and_replace(
        ImagenAssessmentOutOfContextView, AssessmentOutOfContextView)
    vreg.register_and_replace(ImagenScanOutOfContextView, ScanOutOfContextView)
    vreg.register(ImagenQuestionnaireRunOutOfContextView)
    vreg.register_and_replace(
        ImagenSubjectOutOfContextView, SubjectOutOfContextView)
    vreg.register_and_replace(ImagenGenomicMeasureRunOutOfContextView,
        GenomicMeasureOutOfContextView)
