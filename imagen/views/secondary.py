# -*- coding: utf-8 -*-
# copyright 2013-2016 CEA (Saclay, FRANCE), all rights reserved.
# contact http://www.cea.fr -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.


from cubicweb.predicates import is_instance
from cubicweb.view import EntityView
from cubes.piws.views.secondary import (OutOfContextScanView,
                                        BaseOutOfContextView,
                                        OutOfContextSubjectView)
from cubes.brainomics.views.outofcontext import GenomicMeasureOutOfContextView


###############################################################################
# Genetics
###############################################################################

class GeneticOutOfContextView(BaseOutOfContextView):
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("GenomicMeasure")

    def entity_description(self, entity):
        """ Generate a dictionary with the entity description.
        """
        out = {}
        try:
            eGenPlat = entity.platform[0]
            out["Platform"] = eGenPlat.name
            out["Chromosom set"] = entity.chromset
            eassessment = entity.in_assessment[0]
            out["Timepoint"] = eassessment.timepoint
        except:
            pass
        return out


###############################################################################
# Subjects
###############################################################################

class OutOfContextImagenSubjectView(BaseOutOfContextView):
    __select__ = EntityView.__select__ & is_instance("Subject")

    def entity_description(self, entity):
        """ Generate a dictionary with the Subject description.
        """
        desc = {}
        desc["Gender"] = entity.gender
        desc["Handedness"] = entity.handedness
        return desc


def registration_callback(vreg):
    """ Update outofcontext views
    """
    vreg.register_and_replace(GeneticOutOfContextView,
                              GenomicMeasureOutOfContextView)
    vreg.register_and_replace(
        OutOfContextImagenSubjectView, OutOfContextSubjectView)
