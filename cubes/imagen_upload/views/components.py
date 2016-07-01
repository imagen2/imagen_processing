# copyright 2016 CEA, all rights reserved.
# contact http://i2bm.cea.fr/drf/i2bm/NeuroSpin -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.

# CW import
from cubicweb.predicates import anonymous_user
from cubicweb.web import component

# Cubes import
from cubes.piws.views.components import PIWSNavigationtBox
from cubes.rql_upload.views.components import CWUploadedBox


class IMAGENCWUploadedBox(CWUploadedBox):
    """ Class that generate a left box on the web browser to access all user
        and group uploads.

    .. warning::

        It will NOT appear for anonymous users.
    """

    def render_body(self, w, **kwargs):
        super(IMAGENCWUploadedBox, self).render_body(w, **kwargs)

        rql = ("DISTINCT Any G WHERE G is CWGroup,"
               " G description ILIKE '%acquisition_centre%',"
               " U in_group G, U login '{}'")
        rql = rql.format(self._cw.user_data()['login'])
        rset = self._cw.execute(rql)
        for entity in rset.entities():
#            if entity.name == 'managers' or entity.name == 'users':
#                continue
            href = self._cw.build_url(
                "view",
                rql=("Any X ORDERBY X DESC WHERE X is CWUpload,"
                     " X upload_fields F, F name 'centre',"
                     " F value '{}'".format(entity.name))
            )
            w(u'<div class="btn-toolbar">')
            w(u'<div class="btn-group-vertical btn-block">')
            w(u'<a class="btn btn-primary" href="{0}">'.format(href))
            w(u'{} uploads</a>'.format(entity.name))
            w(u'</div></div><br/>')


class DashboardsBox(component.CtxComponent):
    """ Class that generate a left box on the web browser
        to access all dashboards (user and centre(s)).

    .. warning::

        It will NOT appear for anonymous users.
    """
    __regid__ = "ctx-dashboards-box"
    __select__ = (component.CtxComponent.__select__ & ~anonymous_user())
    title = _("Dashboards")
    context = "left"
    order = -1

    def render_body(self, w, **kwargs):
        # my dashboard
        href = self._cw.build_url(
            "view", vid="dashboard-view",
            title="My dashboard",
            user=self._cw.user_data()['login'])
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'My dashboard</a>')
        w(u'</div></div><br/>')

        # centre dashboard
        rql = ("DISTINCT Any G WHERE G is CWGroup,"
               " G description ILIKE '%acquisition_centre%',"
               " U in_group G, U login '{}'")
        rql = rql.format(self._cw.user_data()['login'])
        rset = self._cw.execute(rql)
        for entity in rset.entities():
            href = self._cw.build_url(
                "view", vid="dashboard-view",
                title='{} dashboard'.format(entity.name),
                centre=entity.name
            )
            w(u'<div class="btn-toolbar">')
            w(u'<div class="btn-group-vertical btn-block">')
            w(u'<a class="btn btn-primary" href="{0}">'.format(href))
            w(u'{} dashboard</a>'.format(entity.name))
            w(u'</div></div><br/>')


def registration_callback(vreg):

    # Update components
    vreg.unregister(PIWSNavigationtBox)
    vreg.register_and_replace(IMAGENCWUploadedBox, CWUploadedBox)
    vreg.register(DashboardsBox)
