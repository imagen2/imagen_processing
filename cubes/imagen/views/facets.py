##########################################################################
# NSAp - Copyright (C) CEA, 2013 - 2016
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html for details.
##########################################################################

# Cubicweb import
from cubicweb.web import facet
from cubicweb.predicates import is_instance

from cubes.piws.views.facets import LabelFacet, ScanFieldFacet, StudyFacet

###############################################################################
# FACETS
###############################################################################

class ImagenLabelFacet(LabelFacet):
    """ Redefine the LabelFacet from PIWS to remove "Scan" from the list of
        entities on which the LabelFacet is applied.
    """
    __select__ = is_instance("ProcessingRun", "QuestionnaireRun",
                             "GenomicMeasure")


class ImagenTypeFacet(facet.RQLPathFacet):
    """ Define a new Facet to filter on type. Created for Scans.
    """
    __regid__ = "type-facet"
    __select__ = is_instance("Scan")
    path = ["X type T"]
    order = 1
    filter_variable = "T"
    title = _("Types")

###############################################################################
# Registration callback
###############################################################################

def registration_callback(vreg):

    # Remove the PIWS LabelFacet and replace with ImagenLabelFacet
    # The difference is that we don't want the "Label facet" to apply on scans
    # but instead filter scans based on "type", in particular for EPI to be
    # able to differenciate between the paradigms e.g. EPI_faces, EPI_mid...
    vreg.unregister(LabelFacet)
    vreg.register(ImagenLabelFacet)
    vreg.register(ImagenTypeFacet)
    vreg.unregister(ScanFieldFacet)
    vreg.unregister(StudyFacet)
