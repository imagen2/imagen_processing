# copyright 2016 CEA, all rights reserved.
# contact http://i2bm.cea.fr/drf/i2bm/NeuroSpin -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.

# CW imports
from cubicweb.web.views.startup import IndexView

# Cubes import
from cubes.piws.views.startup import NSIndexView


class IMAGENIndexView(IndexView):
    """ Class that defines the piws index view.
    """

    def call(self, **kwargs):
        """ Create the 'index' like page of our site.
        """
        # Get the card that contains some text description about this site
        self.w(u"THIS IS THE INDEX VIEW")
        rset = self._cw.execute("Any X WHERE X is Card, X title 'index'")

def registration_callback(vreg):
    vreg.register_and_replace(IMAGENIndexView, NSIndexView)
