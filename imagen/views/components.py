# -*- coding: utf-8 -*-
# copyright 2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# copyright 2013 CEA (Saclay, FRANCE), all rights reserved.
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

from cubicweb.web.views.bookmark import BookmarksBox
from cubes.brainomics.views.components import (BrainomicsEditBox,
    BrainomicsDownloadBox, BrainomicsLinksCenters)
from cubicweb.web import component
from cubicweb.predicates import (none_rset, one_line_rset, is_instance, nonempty_rset,
                                 has_related_entities, match_view, match_user_groups,
                                 anonymous_user, relation_possible)
from cubicweb.web.views.facets import FilterBox


###############################################################################
# Navigation Box 
###############################################################################
class ImagenNavLeftBox(component.CtxComponent):
    """ Display a box containing navigation shortcuts
    """
    __regid__ = 'nav_box'
    title = _('Navigation')

    def render_body(self, w):
        # Subjects
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql='Any S Where S is Subject')
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
        href = self._cw.build_url(rql='Any S Where S is Scan')
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Scans</a>')
        w(u'</div></div><br/>')

        #Genetics
        w(u'<div class="btn-toolbar" >')
        w(u'<div class="btn-group-vertical btn-block">')
        w(u'<a class="btn btn-info" '
               'data-toggle="collapse" data-target="#genetic_buttons">')
        w(u'Genetics</a>')
        w(u'</div>')
        w(u'</div>')

        w(u'<div id="genetic_buttons" class="collapse">')
        #button 1: raw
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql=('Any G Where G is GenomicMeasure,'
                                       ' G type "raw"'))
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Raw data</a>')
        w(u'</div></div>')
        #button 2: QC
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql=('Any G Where G is GenomicMeasure,'
                                       ' G type "qc"'))
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'QC data</a>')
        w(u'</div></div>')
        #button 3: imputed
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql=('Any G Where G is GenomicMeasure,'
                                       ' G type "imput"'))
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Imputed data</a>')
        w(u'</div></div>')
        w(u'</div><br/>')
        
        # Questionnaires
        #w(u'<div class="btn-toolbar">')
        #w(u'<div class="btn-group-vertical btn-block">')
        #href = self._cw.build_url(rql='Any Q Where Q is Questionnaire')
        #w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        #w(u'Questionnaires</a>')
        #w(u'</div></div><br/>')

        # Questionnaire Runs
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(rql='Any Q Where Q is QuestionnaireRun')
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Questionnaires</a>')
        w(u'</div></div><br/>')

        # ExternalResource
        #w(u'<div class="btn-toolbar">')
        #w(u'<div class="btn-group-vertical btn-block">')
        #href = self._cw.build_url(rql='Any E Where E is ExternalResource')
        #w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        #w(u'Resources</a>')
        #w(u'</div></div><br/>')

        # ScoreValue
        #w(u'<div class="btn-toolbar">')
        #w(u'<div class="btn-group-vertical btn-block">')
        #href = self._cw.build_url(rql='Any S Where S is ScoreValue')
        #w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        #w(u'Scores</a>')
        #w(u'</div></div><br/>')

        # Help
        w(u'<br/><br/>')
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url("view", vid="help")
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Help</a>')
        w(u'</div></div><br/>')


###############################################################################
# Statistic boxes
###############################################################################
class ImagenSubjectStatistics(component.CtxComponent):
    """ Display a box containing links to statistics on the cw entities.
    """
    __regid__ = "subject_statistics"
    context = "left"
    title = _("Statistics")
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
        href = self._cw.build_url("view", vid="highcharts-basic-pie",
                                  rql="Any H WHERE S is Subject, S handedness H",
                                  title="Subject handednesses")
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Subject handedness repartition</a>')
        w(u'</div></div><br/>')

        # Create a view to see the db subject status
        #href = self._cw.build_url(
        #    "view", vid="highcharts-relation-summary-view",
        #    rql="Any S WHERE S is Subject", title="Insertion status",
        #    relation="concerned_by", subject_attr="identifier",
        #    object_attr="timepoint")
        #w(u'<div class="btn-toolbar">')
        #w(u'<div class="btn-group-vertical btn-block">')
        #w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        #w(u'Insertion status</a>')
        #w(u'</div></div><br/>')

        # Create a view to see the subject center/timepoint repartition in the db
        href = self._cw.build_url("view", vid="welcome-view",
                                  title="Subjects repartition")
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Subjects repartition</a>')
        w(u'</div></div><br/>')


class ImagenAssessmentStatistics(component.CtxComponent):
    """ Display a box containing links to statistics on the cw entities.
    """
    __regid__ = "assessment_statistics"
    context = "left"
    title = _("Statistics")
    order = 1
    __select__ = is_instance("Assessment")

    def render_body(self, w, **kwargs):
        """ Method to create the statistic box content.
        """
        # Create a view to see the db acquistion status
        href = self._cw.build_url(
            "view", vid="highcharts-relation-summary-view",
            rql="Any A WHERE A is Assessment", title="Acquisition status",
            relation="uses", subject_attr="timepoint", object_attr="label")
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Acquisition status</a>')
        w(u'</div></div><br/>')

        # Create a view to see the db processing status
        #href = self._cw.build_url(
        #    "view", vid="highcharts-relation-summary-view",
        #    rql="Any A WHERE A is Assessment", title="Processing status",
        #    relation="related_processing", subject_attr="timepoint",
        #    object_attr="tool")
        #w(u'<div class="btn-toolbar">')
        #w(u'<div class="btn-group-vertical btn-block">')
        #w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        #w(u'Processing status</a>')
        #w(u'</div></div><br/>')

        # Create a view to see the db subject age distribution
        href = self._cw.build_url(
            "view", vid="highcharts-basic-plot",
            rql="Any A WHERE X is Assessment, X age_of_subject A",
            title="Age distribution", is_hist=True)
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'Age distribution</a>')
        w(u'</div></div><br/>')


###############################################################################
# Facet box
###############################################################################
class ImagenFilterBox(FilterBox):
    title = "Filters"

    def render_body(self, w, **kwargs):

        req = self._cw
        rset, vid, divid, paginate = self._get_context()
        assert len(rset) > 1

        if vid is None:
            vid = req.form.get('vid')

        hiddens = {}
        for param in ('subvid', 'vtitle'):
            if param in req.form:
                hiddens[param] = req.form[param]

        self.generate_form(w, rset, divid, vid, paginate=paginate,
                           hiddens=hiddens, **self.cw_extra_kwargs)
        

###############################################################################
# Factory
###############################################################################
def registration_callback(vreg):
    vreg.unregister(BrainomicsLinksCenters)
    vreg.unregister(BookmarksBox)
    vreg.unregister(BrainomicsDownloadBox)
    vreg.unregister(BrainomicsEditBox)
    vreg.register(ImagenNavLeftBox)
    vreg.register(ImagenSubjectStatistics)
    vreg.register(ImagenAssessmentStatistics)
    #vreg.register_and_replace(ImagenFilterBox, FilterBox)

