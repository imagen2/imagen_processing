# -*- coding: utf-8 -*-
# copyright 2013 =AGrigis, all rights reserved.
# contact http://www.logilab.fr -- mailto:=antoine.grigis@cea.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-neurospinweb views/forms/actions/components for web ui"""

from cubicweb.web.views.startup import IndexView
from cubes.brainomics.views.startup import BrainomicsIndexView
from cubicweb.predicates import is_instance
from cubicweb.web.views.primary import PrimaryView


###############################################################################
# Index View
###############################################################################
class ImagenIndexView(IndexView):

    def call(self, **kwargs):
        """ Class that defines the imagen index view.
        """
        # Get the card that contains some text description about this site
        rset = self._cw.execute("Any X WHERE X is Card, X title 'index'")
        self.wview("primary", rset=rset)


###############################################################################
# Card View
###############################################################################
class ImagenCardView(PrimaryView):
    """ Class that that defines how we print card entities.
    """
    __select__ = PrimaryView.__select__ & is_instance("Card")

    def call(self, rset=None, **kwargs):
        """ Format the card entity content.
        """
        # Get the rset
        rset = self.cw_rset or rset

        # Get additional resources links
        resources = {
            "welcome-url": self._cw.build_url("view", vid="welcome"),
            "license-url": self._cw.build_url("license"),
            "connect-image": self._cw.data_url("images/connect.jpg"),
            "database-image": self._cw.data_url("images/database.jpg"),
            "nsap-image": self._cw.data_url("images/neurospin.jpg"),
            "imagen-image": self._cw.data_url("images/imagen.jpg"),
            "nsap-url": ("http://www-dsv.cea.fr/neurospin"),
            "imagen-url": "http://www.imagen-europe.com/",
        }

        # Update card links links to content
        content = rset.get_entity(0, 0).content
        content = content % resources
        self.w(content)


###############################################################################
# Registry
###############################################################################
def registration_callback(vreg):
    vreg.register_and_replace(ImagenIndexView, BrainomicsIndexView)
    vreg.register(ImagenCardView)
