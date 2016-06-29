# -*- coding: utf-8 -*-
# copyright 2016 CEA, all rights reserved.
# contact http://i2bm.cea.fr/drf/i2bm/NeuroSpin -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.

"""cubicweb-imagen-upload schema"""

from yams.buildobjs import String
from cubicweb.schemas.bootstrap import CWGroup

CWGroup.add_relation(String(maxsize=512), name='description')
