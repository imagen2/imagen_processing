#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""cubicweb-imagen specific hooks and operations"""

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


class ImagenSessionOpenHook(Hook):
    __regid__ = "imagen.remove_userstatus"
    __select__ = Hook.__select__
    events = ('server_startup', 'server_maintenance')

    def __call__(self):

        with self.repo.internal_cnx() as cnx:

            if 'ctxcomponents' in cnx.vreg:

                cw_properties_list = [
                    {'pkey': u'ctxcomponents.userstatus.visible',
                     'value': 'NULL'},
                    {'pkey': u'ctxcomponents.userstatus.order',
                     'value': u'5'},
                    {'pkey': u'ctxcomponents.userstatus.context',
                     'value': u'header-right'}
                ]

                for item in cw_properties_list:
                    cnx.execute(u"DELETE Any X WHERE X is CWProperty, "
                                u"X pkey '%(pkey)s'" % item)

                cnx.execute(u"INSERT CWProperty X: X value %(value)s, "
                            u"X pkey '%(pkey)s'" % cw_properties_list[0])
                cnx.execute(u"INSERT CWProperty X: X value '%(value)s', "
                            u"X pkey '%(pkey)s'" % cw_properties_list[1])
                cnx.execute(u"INSERT CWProperty X: X value '%(value)s', "
                            u"X pkey '%(pkey)s'" % cw_properties_list[2])

                cnx.commit()
