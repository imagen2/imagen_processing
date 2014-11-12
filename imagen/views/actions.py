# -*- coding: utf-8 -*-
# copyright 2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# copyright 2013 CEA (Saclay, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
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

# System import
import re

# CW import
from logilab.common.registry import yes
from cubicweb.web.action import Action
from cubicweb.web.views.wdoc import AboutAction, HelpAction
from cubicweb.web.views.actions import PoweredByAction, GotRhythmAction
from cubicweb.predicates import (is_instance, nonempty_rset, anonymous_user,
                                 match_user_groups, relation_possible,
                                 multi_lines_rset)
from cubes.rql_download.views.actions import FSetAdaptor
from cubes.rql_download.views.components import RQL_DOWNLOAD_SEARCH_ENTITIES


###############################################################################
# ACTIONS 
###############################################################################

class LicenseAction(Action):
    __regid__ = "license"
    __select__ = yes()
    category = "footer"
    order = 1
    title = _("License")

    def url(self):
        return self._cw.build_url("license")


class LegalAction(Action):
    __regid__ = "legal"
    __select__ = yes()
    category = "footer"
    order = 2
    title = _("Legal")

    def url(self):
        return self._cw.build_url("legal")


class ImagenResourcePoweredByAction(Action):
    __regid__ = 'poweredby'
    __select__ = yes()
    category = 'footer'
    order = 3
    title = _('&#169; 2014 CEA<br/>')

    def url(self):
        return 'http://www-dsv.cea.fr/neurospin'


###############################################################################
# Adaptors
###############################################################################

RQL_DOWNLOAD_SEARCH_ENTITIES += ["GenomicMeasure"]


class ImagenAdaptor(Action):
    """ Action to download imagen entity objects.
    """
    __regid__ = "rqldownload-adaptors"
    __select__ = Action.__select__ & is_instance("Scan", "GenomicMeasure")
    __rset_type__ = "jsonexport"

    def rql(self, rql, parameter_name):
        """ Method that patch the rql.

        note::
            The patched rql returned first elements are then the file pathes.
            Reserved keys are 'PATH'.
        """
        # Check that reserved keys are not used
        split_rql = re.split(r"[ ,]", rql)
        for revered_key in ["PATH", ]:
            if revered_key in split_rql:
                raise ValidationError(
                    "CWSearch", {
                        "rql": _(
                            'cannot edit the rql "{0}", "{1}" is a reserved key, '
                            'choose another name'.format(rql, revered_key))})

        # Remove the begining of the rql in order to complete it
        formated_rql = " ".join(rql.split()[1:])

        # Complete the rql in order to access file pathes
        global_rql = ("Any PATH, {0}, {1} filepath PATH".format(
            formated_rql, parameter_name))

        return global_rql


def registration_callback(vreg):

    # Desactivate some actions for now
    vreg.unregister(AboutAction)
    vreg.unregister(HelpAction)
    vreg.unregister(GotRhythmAction)
    vreg.unregister(FSetAdaptor)

    vreg.register_and_replace(ImagenResourcePoweredByAction, PoweredByAction)
    vreg.register(LegalAction)
    vreg.register(LicenseAction)
    vreg.register(ImagenAdaptor)


