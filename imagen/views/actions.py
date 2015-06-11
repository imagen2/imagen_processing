#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Cubicweb import
from cubicweb.predicates import yes
from cubicweb.web.action import Action
from cubes.piws.views.actions import LicenseAction, LegalAction, NSPoweredByAction


###############################################################################
# ACTIONS
###############################################################################
class NeurospinAction(Action):
    __regid__ = "neurospin"
    __select__ = yes()
    category = "footer"
    order = 1
    title = _("Neurospin")

    def url(self):
        return 'http://dsv.cea.fr/dsv/english/Pages/Welcome.aspx'

class ImagenAction(Action):
    __regid__ = "imagen"
    __select__ = yes()
    category = "footer"
    order = 2
    title = _("Imagen")

    def url(self):
        return 'http://www.imagen-europe.com/'

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
    title = _("&#169 2014, Neurospin Analysis Platform developers")

    def url(self):
        return "http://www-centre-saclay.cea.fr/fr/NeuroSpin"


def registration_callback(vreg):

    # Update the footer
    vreg.register(ImagenLicenseAction)
    vreg.register(ImagenLegalAction)
    vreg.register(ImagenNSPoweredByAction)
    vreg.register(NeurospinAction)
    vreg.register(ImagenAction)
    vreg.unregister(LicenseAction)
    vreg.unregister(LegalAction)
    vreg.unregister(NSPoweredByAction)
