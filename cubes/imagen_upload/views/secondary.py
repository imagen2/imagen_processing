# -*- coding: utf-8 -*-
# copyright 2016 CEA, all rights reserved.
# contact http://i2bm.cea.fr/drf/i2bm/NeuroSpin -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.

from cubes.piws.views import secondary


class OutOfContextCWUploadView(secondary.OutOfContextCWUploadView):
    """ CWUpload secondary rendering.
    """

    def entity_description(self, entity):
        """ Generate a dictionary with the CWUpload description.
        """
        desc = {}
        desc["Form"] = entity.form_name
        desc["Status"] = entity.status
        desc["Subject"] = entity.get_field_value('sid')
        desc["Time Point"] = entity.get_field_value('time_point')
        return desc


def registration_callback(vreg):
    vreg.register_and_replace(OutOfContextCWUploadView,
                              secondary.OutOfContextCWUploadView)
