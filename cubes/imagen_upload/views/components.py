# copyright 2016 CEA, all rights reserved.
# contact http://i2bm.cea.fr/drf/i2bm/NeuroSpin -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.

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

        rql = "DISTINCT Any G WHERE G is CWGroup, U in_group G, U login '{}'"
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


def registration_callback(vreg):

    # Update components
    vreg.unregister(PIWSNavigationtBox)
    vreg.register_and_replace(IMAGENCWUploadedBox, CWUploadedBox)
