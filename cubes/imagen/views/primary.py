# -*- coding: utf-8 -*-
# copyright 2013-2016 CEA, all rights reserved.
# contact http://i2bm.cea.fr/drf/i2bm/NeuroSpin -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.

from cubes.piws.views.primary import PIWSPrimaryView

import json


class ImagenPrimaryView(PIWSPrimaryView):

    def _prepare_side_boxes(self, entity):
        """ Create the right relation boxes to display.
        """

        sideboxes_config_filepath = self._cw.vreg.config[
            "sidebox_configuration"]
        sideboxes_config = {}
        if sideboxes_config_filepath:
            try:
                with open(sideboxes_config_filepath, 'r') as _file:
                    sideboxes_config = json.load(_file)
            except:
                sideboxes_config = {}
        sideboxes = []
        boxesreg = self._cw.vreg["ctxcomponents"]
        defaultlimit = self._cw.property_value("navigation.related-limit")
        if entity.cw_etype in sideboxes_config:
            for entry in sideboxes_config[entity.cw_etype]:
                rql_complete = "{0}, E eid '{1}'".format(entry["rql"],
                                                         entity.eid)
                rset = self._cw.execute(rql_complete)
                if rset.rowcount > 0:
                    box = boxesreg.select("relationbox", self._cw,
                                          rset=rset.limit(defaultlimit),
                                          rql=rql_complete,
                                          title=unicode(entry["box_title"]),
                                          context="incontext")
                    sideboxes.append(box)

        # XXX since we've two sorted list, it may be worth using bisect
        def get_order(x):
            if "order" in x.cw_property_defs:
                return x.cw_propval("order")
            # default to 9999 so view boxes occurs after component boxes
            return x.cw_extra_kwargs.get("dispctrl", {}).get("order", 9999)

        return sorted(sideboxes, key=get_order)

    def render_entity_relations(self, entity):
        """
        don't do anything, relation boxes are already handled in sideboxes
        """
        return None


def registration_callback(vreg):
    pass
