#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Piws import
from cubes.piws.views.components import NSNavigationtBox
from cubes.rql_upload.views.components import CWUploadBox

# Cubicweb import
from cubicweb.web import component
from cubicweb.predicates import match_view


import json
###############################################################################
# Navigation Box
###############################################################################


class ImagenNSNavigationtBox(NSNavigationtBox):
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

        # Exams
#        w(u'<div class="btn-toolbar">')
#        w(u'<div class="btn-group-vertical btn-block">')
#        href = self._cw.build_url(rql="Any A Where A is Assessment")
#        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
#        w(u'Exams</a>')
#        w(u'</div></div><br/>')

        # Scan
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql="Any S Where S is Scan")
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Images</a>')
        w(u'</div></div><br/>')

        # QuestionnaireRun
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        ajaxcallback = "get_questionnaires_data"
        rql_labels = ("DISTINCT Any T ORDERBY T WHERE A is Assessment, "
                      "A timepoint T")
        href = self._cw.build_url(
            "view", vid="jtable-table",
            rql_labels=rql_labels, ajaxcallback=ajaxcallback,
            title="All Questionnaires", elts_to_sort=["ID"],
            tooltip="Questionnaire_general_doc")
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Questionaires</a>')
        w(u'</div></div><br/>')

        # GenomicMeasures
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql="Any GM Where GM is GenomicMeasure")
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Genomic measures</a>')
        w(u'</div></div><br/>')

        # Processed data
        w(u'<div class="btn-toolbar" >')
        w(u'<div class="btn-group-vertical btn-block">')
        w(u'<a class="btn btn-info" '
          'data-toggle="collapse" data-target="#processed_buttons">')
        w(u'Processed Data</a>')
        w(u'</div>')
        w(u'</div>')
        w(u'<div id="processed_buttons" class="collapse">')
        w(u'<div class="panel panel-info">')
        w(u'<div class="panel-body">')

        # button 1: Genetics
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql="Any PR Where PR is ProcessingRun")
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Genetics</a>')
        w(u'</div></div><br/>')

        # button 2: Scans
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql=('Any G Where G is GenomicMeasure,'
                                       ' G type "qc"'))
        w(u'<a class="btn btn-primary" href="">')
        w(u'Scans</a>')
        w(u'</div></div><br/>')

        w(u'</div></div></div><br>')

        # CWSearch
        w(u'<hr>')
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql="Any S Where S is CWSearch")
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'My searches</a>')
        w(u'</div></div><br/>')

        # QC central
        w(u'<hr>')
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url("view", vid="QC_central")
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'QC central</a>')
        w(u'</div></div><br/>')


class StatisticBox(component.CtxComponent):
    """
    parse a json file and generate a box displaying the content of the database
    """

    __regid__ = "stat_box"
    context = "right"
    title = unicode("Database status")
    order = 0
    __select__ = match_view("index_view")

    def render_body(self, w):
        """
        parse the file, return nothing if file is not found
        """

        try:
            stat_file = self.repo.vreg.config["stat_file"]
            with open(stat_file, "r") as stat:
                stat_dict = json.load(stat)


def registration_callback(vreg):

    # Update components
    vreg.unregister(CWUploadBox)
    vreg.register(ImagenNSNavigationtBox)
    vreg.unregister(NSNavigationtBox)
