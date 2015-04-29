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
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql="Any A Where A is Assessment")
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Exams</a>')
        w(u'</div></div><br/>')

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
        ajaxcallback = "EuAims_get_questionnaires_data"
        rql_labels = ("DISTINCT Any T ORDERBY T WHERE A is Assessment, "
                      "A timepoint T")
        href = self._cw.build_url(
            "view", vid="jtable-table",
            rql_labels=rql_labels, ajaxcallback=ajaxcallback,
            title="All Questionnaires", elts_to_sort=["ID"])
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Questionaires</a>')
        w(u'</div></div><br/>')

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


def registration_callback(vreg):

    # Update components
    vreg.unregister(CWUploadBox)
    vreg.register_and_replace(ImagenNSNavigationtBox, NSNavigationtBox)
