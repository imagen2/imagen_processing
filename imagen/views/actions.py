# -*- coding: utf-8 -*-
# copyright 2013-2016 CEA (Saclay, FRANCE), all rights reserved.
# contact http://www.cea.fr -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.

from logilab.common.registry import yes
from cubicweb.web.action import Action
from cubes.piws.views.actions import PoweredByPIWSAction


###############################################################################
# ACTIONS
###############################################################################
class ImagenAction(Action):
    __regid__ = "imagen"
    __select__ = yes()
    category = "footer"
    order = 1
    title = _("Imagen")

    def url(self):
        return 'http://www.imagen-europe.com/'


class NeurospinAction(Action):
    __regid__ = "neurospin"
    __select__ = yes()
    category = "footer"
    order = 2
    title = _("NeuroSpin")

    def url(self):
        return 'http://i2bm.cea.fr/dsv/i2bm/NeuroSpin'


class ImagenLicenseAction(Action):
    __regid__ = "license"
    __select__ = yes()
    category = "footer"
    order = 3
    title = _("License")

    def url(self):
        return self._cw.build_url("license")


class ImagenLegalAction(Action):
    __regid__ = "legal"
    __select__ = yes()
    category = "footer"
    order = 4
    title = _("Legal")

    def url(self):
        return self._cw.build_url("legal")


class ImagenNSPoweredByAction(Action):
    __regid__ = "poweredby"
    __select__ = yes()
    category = "footer"
    order = 5
    title = _("Powered by PIWS")

    def url(self):
        return "https://github.com/neurospin/piws"


def registration_callback(vreg):

    # Update the footer
    vreg.register(ImagenLicenseAction)
    vreg.register(ImagenLegalAction)
    vreg.register(ImagenNSPoweredByAction)
    vreg.register(ImagenAction)
    vreg.register(NeurospinAction)
    vreg.unregister(PoweredByPIWSAction)
