# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Cubicweb import
from cubicweb.web.action import Action
from logilab.common.registry import yes


###############################################################################
# ACTIONS
###############################################################################

class NeuroSpinAction(Action):
    __regid__ = "neurospin"
    __select__ = yes()

    category = "footer"
    order = 3
    title = "NeuroSpin"

    def url(self):
        return "http://i2bm.cea.fr/drf/i2bm/Pages/NeuroSpin.aspx"


def registration_callback(vreg):

    # Update the footer
    vreg.register(NeuroSpinAction)
