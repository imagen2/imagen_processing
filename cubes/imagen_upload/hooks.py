# -*- coding: utf-8 -*-
# copyright 2016 CEA, all rights reserved.
# contact http://i2bm.cea.fr/drf/i2bm/NeuroSpin -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.

"""cubicweb-imagen-upload specific hooks and operations"""

from cubicweb.server.hook import Hook


class ServerStartupHook(Hook):
    """
        Update repository cache with groups from indexation to ease LDAP
        synchronisation
    """
    __regid__ = 'imagen.update_cache_hook'
    events = ('server_startup', 'server_maintenance')

    def __call__(self):
        # get session

        # update repository cache
        with self.repo.internal_cnx() as cnx:
            rset = cnx.execute("Any X WHERE X is CWGroup")
            for egroup in rset.entities():
                if egroup.name in ["guests", "managers", "users", "owners"]:
                    continue
                self.repo._extid_cache[
                    'cn={0},ou=Groups,dc=imagen2,dc=cea,dc=fr'.format(
                        egroup.name)] = egroup.eid
