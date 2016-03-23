# -*- coding: utf-8 -*-
# copyright 2016 CEA, all rights reserved.
# contact http://i2bm.cea.fr/drf/i2bm/NeuroSpin -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.

"""cubicweb-imagen-upload postcreate script, executed at instance creation time or when
the cube is added to an existing instance.

You could setup site properties or a workflow here for example.
"""

# Example of site property change
set_property('ui.site-title', "Imagen Database")

import json


_LDAP_CONFIGURATION_FILE = '/neurospin/imagen/src/scripts/ldap/configuration.json'

with open(_LDAP_CONFIGURATION_FILE) as configuration_file:
    configuration = json.load(configuration_file)

    _LDAP_CONFIGURATION_DETAILS = {
        'synchronization-interval': u'30min',
        'data-cnx-dn': configuration['data-cnx-dn'],
        'data-cnx-password': configuration['data-cnx-password'],
        'user-base-dn': u'ou=People,dc=imagen2,dc=cea,dc=fr',
        'user-attrs-map': u'userPassword:upassword,mail:email,uid:login',
        'group-base-dn': u'ou=Groups,dc=imagen2,dc=cea,dc=fr',
        'group-attrs-map': u'memberUid:member,cn:name',
    }


_LDAP_CONFIGURATION = u"""
# Is the repository responsible to automatically import content from this
# source? You should say yes unless you don't want this behaviour or if you use
# a multiple repositories setup, in which case you should say yes on one
# repository, no on others.
synchronize=yes

# Interval in seconds between synchronization with the external source (default
# to 5 minutes, must be >= 1 min).
synchronization-interval=%(synchronization-interval)s

# Maximum time allowed for a synchronization to be run. Exceeded that time, the
# synchronization will be considered as having failed and not properly released
# the lock, hence it won't be considered
max-lock-lifetime=1h

# Should already imported entities not found anymore on the external source be
# deleted?
delete-entities=no

# Time before logs from datafeed imports are deleted.
logs-lifetime=10d

# Timeout of HTTP GET requests, when synchronizing a source.
http-timeout=1min

# authentication mode used to authenticate user to the ldap.
auth-mode=simple

# realm to use when using gssapi/kerberos authentication.
#auth-realm=

# user dn to use to open data connection to the ldap (eg used to respond to rql
# queries). Leave empty for anonymous bind
data-cnx-dn=%(data-cnx-dn)s

# password to use to open data connection to the ldap (eg used to respond to
# rql queries). Leave empty for anonymous bind.
data-cnx-password=%(data-cnx-password)s

# base DN to lookup for users; disable user importation mechanism if unset
user-base-dn=%(user-base-dn)s

# user search scope (valid values: "BASE", "ONELEVEL", "SUBTREE")
user-scope=ONELEVEL

# classes of user (with Active Directory, you want to say "user" here)
user-classes=top,posixAccount

# additional filters to be set in the ldap query to find valid users
user-filter=

# attribute used as login on authentication (with Active Directory, you want to
# use "sAMAccountName" here)
user-login-attr=uid

# name of a group in which ldap users will be by default. You can set multiple
# groups by separating them by a comma.
user-default-group=users

# map from ldap user attributes to cubicweb attributes (with Active Directory,
# you want to use
# sAMAccountName:login,mail:email,givenName:firstname,sn:surname)
user-attrs-map=%(user-attrs-map)s

# base DN to lookup for groups; disable group importation mechanism if unset
group-base-dn=%(group-base-dn)s

# group search scope (valid values: "BASE", "ONELEVEL", "SUBTREE")
group-scope=ONELEVEL

# classes of group
group-classes=top,posixGroup

# additional filters to be set in the ldap query to find valid groups
group-filter=

# map from ldap group attributes to cubicweb attributes
group-attrs-map=%(group-attrs-map)s"""


def _escape_rql(request):
    return request.replace('\\', '\\\\').replace("'", "\\'")


_LDAP_ATTRIBUTES = {
    u'name': u'Imagen',
    u'type': u'ldapfeed',
    u'config': _escape_rql(_LDAP_CONFIGURATION % _LDAP_CONFIGURATION_DETAILS),
    u'url': u'ldap://127.0.0.1/',
    u'parser': u'ldapfeed',
}


def _create_or_update_ldap_data_source(session):
    """Create or update the LDAP data source
"""
    name = _LDAP_ATTRIBUTES[u'name']
    req = "Any X WHERE X is CWSource, X name '%(name)s'" % {'name': name}
    rset = session.execute(req)
    if rset:
        req = "SET"
        for attribute, value in _LDAP_ATTRIBUTES.iteritems():
            req += " X %(attribute)s '%(value)s'," % {'attribute': attribute, 'value': value}
        req = req[:-1]
        req += " WHERE X is CWSource, X name '%(name)s'" % {'name': name}
    else:
        req = "INSERT CWSource X:"
        for attribute, value in _LDAP_ATTRIBUTES.iteritems():
            req += " X %(attribute)s '%(value)s'," % {'attribute': attribute, 'value': value}
        req = req[:-1]
    rset = session.execute(req)
    session.commit()


if __name__ == '__main__':
    _create_or_update_ldap_data_source(session)
