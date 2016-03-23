# -*- coding: utf-8 -*-
# copyright 2013-2016 CEA, all rights reserved.
# contact http://i2bm.cea.fr/drf/i2bm/NeuroSpin -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.

# Piws import
from cubes.rql_upload.views.components import CWUploadBox
from cubes.piws.views.components       import (PIWSNavigationtBox,
                                               PIWSSubjectStatistics,
                                               PIWSAssessmentStatistics)

# Cubicweb import
from cubicweb.web import component
from cubicweb.predicates import match_view, is_instance

from cubes.rql_upload.views.utils import load_forms

###############################################################################
# Navigation Box
###############################################################################

PIWSNavigationtBox.display_assessment = False


class ImagenPIWSNavigationtBox(PIWSNavigationtBox):
    """ Display a box containing navigation shortcuts.
    """

    def render_body(self, w):
        """ Create the diifferent item of the navigation box
        """
        # Subjects
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql="Any S Where S is Subject")
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Subjects</a>')
        w(u'</div></div><br/>')

        # Assessments
        if self.display_assessment:
            w(u'<div class="btn-toolbar">')
            w(u'<div class="btn-group-vertical btn-block">')
            href = self._cw.build_url(rql="Any A Where A is Assessment")
            w(u'<a class="btn btn-primary" href="{0}">'.format(href))
            w(u'Assessments</a>')
            w(u'</div></div><br/>')

        # Scan
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql="Any S Where S is Scan")
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Scans</a>')
        w(u'</div></div><br/>')

        # QuestionnaireRun
        ajaxcallback = "get_questionnaires_data"
        rql_labels = ("DISTINCT Any T ORDERBY T WHERE A is Assessment, "
                      "A timepoint T")
        rql_types = ("DISTINCT Any T ORDERBY T WHERE Q is Questionnaire, "
                      "Q type T")
        rset = self._cw.execute(rql_types)
        types = [line[0] for line in rset.rows]
        if len(types) > 0:
            # > main button
            w(u'<div class="btn-toolbar">')
            w(u'<div class="btn-group-vertical btn-block">')
            w(u'<a class="btn btn-info"'
               'data-toggle="collapse" data-target="#questionnaires">')
            w(u'Tables</a>')
            w(u'</div></div>')
            # > typed buttons container
            w(u'<div id="questionnaires" class="collapse">')
            w(u'<div class="panel-body">')
            w(u'<hr>')
            # > typed buttons
            for qtype in types:
                href = self._cw.build_url(
                    "view", vid="jtable-table",
                    rql_labels=rql_labels, ajaxcallback=ajaxcallback,
                    title="All Questionnaires", elts_to_sort=["ID"],
                    tooltip_name="All Questionnaires", qtype=qtype)
                w(u'<div class="btn-toolbar">')
                w(u'<div class="btn-group-vertical btn-block">')
                w(u'<a class="btn btn-primary" href="{0}">'.format(href))
                w(u'{0}</a>'.format(qtype))
                w(u'</div></div><br/>')
            w(u'<hr>')
            w(u'</div></div><br/>')

        # ProcessingRun
        rql_types = ("DISTINCT Any T ORDERBY T WHERE P is ProcessingRun, "
                      "P type T")
        rset = self._cw.execute(rql_types)
        types = [line[0] for line in rset.rows]
        if len(types) > 0:
            # > main button
            w(u'<div class="btn-toolbar">')
            w(u'<div class="btn-group-vertical btn-block">')
            w(u'<a class="btn btn-info"'
               'data-toggle="collapse" data-target="#processings">')
            w(u'Processed data</a>')
            w(u'</div></div>')
            # > typed buttons container
            w(u'<div id="processings" class="collapse">')
            w(u'<div class="panel-body">')
            w(u'<hr>')
            # > typed buttons
            for ptype in types:
                href = self._cw.build_url(rql="Any P Where P is ProcessingRun, "
                                              "P type '{0}'".format(ptype))
                w(u'<div class="btn-toolbar">')
                w(u'<div class="btn-group-vertical btn-block">')
                w(u'<a class="btn btn-primary" href="{0}">'.format(href))
                w(u'{0}</a>'.format(ptype))
                w(u'</div></div><br/>')
            w(u'<hr>')
            w(u'</div></div><br/>')

        # GenomicMeasures
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql="Any GM Where GM is GenomicMeasure")
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Genomic measures</a>')
        w(u'</div></div><br/>')

        # CWSearch
        w(u'<hr>')
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql="Any S Where S is CWSearch")
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'<span class="glyphicon glyphicon-shopping-cart"></span> '
          u'My cart</a>')
        w(u'</div></div><br/>')

        # CWUpload
        config = load_forms(self._cw.vreg.config)
        if config > 0:
            w(u'<div class="btn-toolbar">')
            w(u'<div class="btn-group-vertical btn-block">')
            href = self._cw.build_url(rql="Any U Where U is CWUpload")
            w(u'<a class="btn btn-primary" href="{0}">'.format(href))
            w(u'<span class="glyphicon glyphicon glyphicon-cloud-upload">'
                '</span> My uploads</a>')
            w(u'</div></div><br/>')


class StatisticBox(component.CtxComponent):
    """
    parse a json file and generate a box displaying the content of the database
    """

    __regid__ = "stat_box"
    contextual = True
    context = 'right'
    title = unicode("Database content")
    order = 0
    __select__ = match_view("index")

    def render_body(self, w):
        get_timepoint_label = self.match_timepoint_label()
        """
        parse the file, return nothing if file is not found
        """
        try:
            tot, percentages = self.get_stats()

            w(u"<strong>Number of subjects: {0}</strong>".format(tot))
            w(u"<hr>")
            w(u"<ul>")
            for item, dic in percentages.iteritems():
                n_timepoint = len(dic)
                v_timepoint = []
                for timepoint in dic:
                    if dic[timepoint] == 0:
                        n_timepoint -= 1
                    else:
                        v_timepoint.append(timepoint)
                w(u'<li>')
                w(u'{0}'.format(item))

                # build a small table
                w(u'<table class="table" style="margin: 0px; font-size: 10px;'
                  'line-height: 11px;">')
                w(u'<tr>')
                for value in v_timepoint:
                    w(u'<td style="border-top: none; width: {1}%">'
                      '{0}</td>'.format(get_timepoint_label[value],
                                        100. / n_timepoint))
                w(u"</tr>")

                w(u'<tr>')
                for timepoint in dic:
                    value = dic[timepoint]
                    if value == 0:
                        continue
                    w(u'<td style="border-top: none;">')
                    w(u'<div class="progress">')
                    w(u'<div class="progress-bar" role="progressbar" '
                      'aria-valuenow="{0}" aria-valuemin="0" aria-valuemax='
                      '"100" style="width:{0}%">'.format(value))
                    w(u'{0}%'.format(value))
                    w(u'</div>')
                    w(u"</div>")
                    w(u'</td>')
                w(u'</tr>')

                w(u'</table>')
                w(u'</li>')
            w(u'</li>')

        except:
            pass

    def match_timepoint_label(self):
        """
        return the label-abreviation tables for the timepoints
        """

        return {"BL": "Baseline", "FU1": "Follow-Up 1", "FU2": "Follow-Up 2"}

    def get_stats(self):

        timepoints = ['BL', 'FU1', 'FU2']
        scan_labels = ['ADNI_MPRAGE', 'B0', 'DTI', 'EPI', 'FLAIR', 'T2']

        rql_nb_subjects = 'DISTINCT Any COUNT(S) WHERE S is Subject'
        rset_nb_subjects = self._cw.execute(rql_nb_subjects)
        assert len(rset_nb_subjects) == 1
        nb_subjects = rset_nb_subjects[0][0]

        rql = "DISTINCT Any SID, T, SCL WHERE SC is Scan, " \
              "SC label SCL, " \
              "S scans SC, " \
              "S code_in_study SID, " \
              "SC in_assessment A, " \
              "A timepoint T"
        rset = self._cw.execute(rql)

        struct = {}
        for item in rset:
            subject = item[0]
            timepoint = item[1]
            found_label = item[2]
            if subject not in struct:
                struct[subject] = {}
            if timepoint not in struct[subject]:
                struct[subject][timepoint] = set()
            struct[subject][timepoint].add(found_label)

        totals = {}
        for scan_label in scan_labels:
            totals[scan_label] = {}
            for timepoint in timepoints:
                totals[scan_label][timepoint] = 0

        for subject, timepoint_data in struct.iteritems():
            for timepoint, found_labels_set in timepoint_data.iteritems():
                for scan_label in scan_labels:
                    if scan_label in found_labels_set:
                        totals[scan_label][timepoint] += 1

        percentages = {}
        for scan_label, timepoint_data in totals.iteritems():
            percentages[scan_label] = {}
            for timepoint, number in timepoint_data.iteritems():
                percentages[scan_label][timepoint] = \
                    round(float(number) / nb_subjects * 100, 1)

        return nb_subjects, percentages


class ImagenSubjectStatistics(component.CtxComponent):
    """ Display a box containing links to statistics on the cw entities.
    """
    __regid__ = "subject_statistics"
    context = "left"
    title = unicode("Statistics")
    order = 1
    __select__ = is_instance("Subject")

    def render_body(self, w, **kwargs):
        """ Method to create the statistic box content.
        """
        # Create a view to see the subject gender repartition in the db
        href = self._cw.build_url("view", vid="highcharts-basic-pie",
                                  rql="Any G WHERE S is Subject, S gender G",
                                  title="Subject genders")
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Subject gender repartition</a>')
        w(u'</div></div><br/>')

        # Create a view to see the subject handedness repartition in the db
        href = self._cw.build_url(
            "view", vid="highcharts-basic-pie",
            rql="Any H WHERE S is Subject, S handedness H",
            title="Subject handednesses")
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Subject handedness repartition</a>')
        w(u'</div></div><br/>')


def registration_callback(vreg):

    # Update components
    vreg.register(StatisticBox)
    vreg.unregister(CWUploadBox)
    vreg.unregister(PIWSNavigationtBox)
    vreg.register(ImagenPIWSNavigationtBox)
    vreg.unregister(PIWSSubjectStatistics)
    vreg.register(ImagenSubjectStatistics)
    vreg.unregister(PIWSAssessmentStatistics)
