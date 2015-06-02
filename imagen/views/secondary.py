#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Cubicweb import
from cubicweb.predicates import is_instance
from cubicweb.view import EntityView
from cubes.piws.views.secondary import OutOfContextScanView


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
        rql_secondary = ("Any SU, ST, TY, FO, SHX, SHY, SHZ, RESX, RESY, "
                         "RESZ, TR, TE, FI WHERE S is SCAN, "
                         "S subject SU, "
                         "S study ST, "
                         "S type TY, "
                         "S format FO, "
                         "S has_data SD, "
                         "SD shape_x SHX, "
                         "SD shape_y SHY, "
                         "SD shape_z SHZ, "
                         "SD voxel_res_x RESX, "
                         "SD voxel_res_y RESY, "
                         "SD voxel_res_z RESZ, "
                         "SD tr TR, "
                         "SD te TE, "
                         "SD field FI, "
                         "S eid '{0}'".format(entity.eid))
        rset = self._cw.execute(rql_secondary)
        # Parse rset
        _subject = rset.get_entity(0, 0)
        _study = rset.get_entity(0, 1)
        line = rset[0]
        _type = line[2]
        _format = line[3]
        _shape_x = line[4]
        _shape_y = line[8]
        _shape_z = line[6]
        _voxel_res_x = line[7]
        _voxel_res_y = line[8]
        _voxel_res_z = line[9]
        _tr = line[10]
        _te = line[11]
        _field = line[12]

        # Get the subject/study related entities
#        subject = entity.subject[0]
#        study = entity.study[0]

        # Get the scan image url
        image = u'<img alt="" src="%s">' % self._cw.data_url(entity.symbol)

        # Create the div that will contain the list item
        self.w(u'<div class="ooview"><div class="well">')

        # Create a bootstrap row item
        self.w(u'<div class="row">')
        # > first element: the image
        self.w(u'<div class="col-md-2"><p class="text-center">{0}</p>'
               '</div>'.format(image))
        # > second element: the scan description + link
        self.w(u'<div class="col-md-4"><h4>{0}</h4>'.format(
            entity.view("incontext")))
        self.w(u'Type <em>{0}</em> - Format <em>{1}</em></div>'.format(
            _type, _format))
        # > third element: the see more button
        self.w(u'<div class="col-md-3">')
        self.w(u'<button class="btn btn-danger" type="button" '
               'style="margin-top:8px" data-toggle="collapse" '
               'data-target="#info-%s">' % row)
        self.w(u'See more')
        self.w(u'</button></div>')
        # > fourth element: the documentation button
        if "EPI" in entity.type:
            href = self._cw.build_url("view", _notemplate=True,
                                      vid="doc_FMRIData")
            self.w(u'<a class="btn btn-warning" style="margin-top: 10px" '
                   'href="javascript:open_popup('
                   "'{0}'"
                   ')">documentation</a>'.format(href))
#        self.w(u'<a class="btn btn-warning" style="margin-top: 10px" '
#               'href="{0}">'.format(href))
#        self.w(u'Documentation</a>')
        self.w(u'<br/>')
        # Close row item
        self.w(u'</div>')

        # Get the scan description
#        dtype_entity = entity.has_data[0]

        # Create a div that will be show or hide when the see more button is
        # clicked
        self.w(u'<div id="info-%s" class="collapse">' % row)
        self.w(u'<dl class="dl-horizontal">')
        # > image shape
        self.w(u'<dt>Image Shape (x)</dt><dd>{0}</dd>'.format(
            _shape_x))
        self.w(u'<dt>Image Shape (y)</dt><dd>{0}</dd>'.format(
            _shape_y))
        self.w(u'<dt>Image Shape (z)</dt><dd>{0}</dd>'.format(
            _shape_z))
        # > image resolution
        self.w(u'<dt>Voxel resolution (x)</dt><dd>{0}</dd>'.format(
            _voxel_res_x))
        self.w(u'<dt>Voxel resolution (y)</dt><dd>{0}</dd>'.format(
            _voxel_res_y))
        self.w(u'<dt>Voxel resolution (z)</dt><dd>{0}</dd>'.format(
            _voxel_res_z))
        # > image TR
        self.w(u'<dt>Repetition time</dt><dd>{0}</dd>'.format(
            _tr))
        # > image TE
        self.w(u'<dt>Echo time</dt><dd>{0}</dd>'.format(
            _te))
        # > Scanner field
        self.w(u'<dt>Scanner field</dt><dd>{0}</dd>'.format(
            _field))
        # > Realted entities
        self.w(u'<dt>Ralated subject</dt><dd>{0}</dd>'.format(
            _subject.view("incontext")))
        self.w(u'<dt>Ralated study</dt><dd>{0}</dd>'.format(
            _study.view("incontext")))
        self.w(u'</div>')

        # Close list item
        self.w(u'</div></div>')

        self.w(u'<script language="javascript">'
               'function open_popup(page) {'
               'window.open(page,"documentation","menubar=no, '
               'status=no, scrollbars=no, menubar=no, width=600, height=450");'
               '}'
               '</script>')


def registration_callback(vreg):
    """ Update outofcontext views
    """
    vreg.register_and_replace(
        ImagenScanOutOfContextView, OutOfContextScanView)
