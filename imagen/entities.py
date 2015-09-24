# -*- coding: utf-8 -*-
# copyright 2014-2015 CEA (Saclay, FRANCE), all rights reserved.
# contact http://www.cea.fr -- mailto:imagendatabase@cea.fr
#
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

from cubicweb.entities import AnyEntity
from cubes.piws.entities import GenomicMeasure


class ImagenGenomicMeasure(AnyEntity):
    __regid__ = "GenomicMeasure"

    def dc_title(self):
        """ Method the defined the processing run entity title
        """
        return "Genomic Measure ({0}-{1})".format(
            self.in_assessment[0].timepoint, self.type)

    @property
    def symbol(self):
        """ This property will return a symbol cooresponding to the processing
        run type
        """
        return "images/genetics_chip.png"


###############################################################################
# Register views
###############################################################################

def registration_callback(vreg):
    """ Update outofcontext views.
    """
    vreg.unregister(GenomicMeasure)
    vreg.register(ImagenGenomicMeasure)
