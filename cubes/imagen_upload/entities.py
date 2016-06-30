# -*- coding: utf-8 -*-
# copyright 2016 CEA, all rights reserved.
# contact http://i2bm.cea.fr/drf/i2bm/NeuroSpin -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.

"""cubicweb-imagen-upload entity's classes"""

from cubes.rql_upload.entities import EntityCWUpload


class EntityCWUpload(EntityCWUpload):
    """ Overrired the 'CWUpload' entity associated functions. """

    def dc_title(self):
        """ Method that defines the upload entity title. """

        return u"{} for {} ({}) by {} on {} at {}".format(
            self.form_name,
            self.get_field_value('sid'),
            self.get_field_value('time_point'),
            self.dc_creator(),
            self.creation_date.strftime('%Y/%m/%d'),
            self.creation_date.strftime('%H:%M:%S')
        )
