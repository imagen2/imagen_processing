#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

from cubes.brainomics.views.primary import BrainomicsPrimaryView
from cubicweb.web.views.primary import PrimaryView


def registration_callback(vreg):
    """ Update  primary views
    """
    vreg.register_and_replace(PrimaryView, BrainomicsPrimaryView)

