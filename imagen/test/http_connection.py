#! /usr/bin/env python
##########################################################################
# Brainomics - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os
import sys
import numpy as np
import urllib2
import urllib
import json
import traceback

# Global variable that specify the export cw format
_EXPORT_TYPE = "json"


class HTTPConnection(object):
    """ Tool to dump the data stored in a cw instance.

    Attributes
    ----------
    url : str
        the url to the cw instance.
    login : str
        the cw login.
    opener:  OpenerDirector
        object that contains the connexion to the cw instance.
    """
    def __init__(self, url, login, password):
        """ Initilize the HTTPConnection class.

        Parameters
        ----------
        url: str (mandatory)
            the url to the cw instance.
        login: str (mandatory)
            the cw login.
        password: str (mandatory)
            the cw user password.
        """
        # Class parameters
        self.url = url
        self.login = login
        self._connect(password)

    ###########################################################################
    # Public Members
    ###########################################################################

    def entities(self, entity_type):
        """ Method that loads all the eids from a cw entity.

        Parameters
        ----------
        entity_type: str (mandatory)
            the name of the entity we want to dump the representations in
            the cw db.

        Returns
        -------
        rset: list of str
            a list with all the eids of the requested entity.
        """
        # Create a dictionary with the request meta information
        data = {
            "vid": "e" + _EXPORT_TYPE + "export",
        }

        # Get the result set
        rset = json.load(self.opener.open(self.url + '/' + entity_type,
                                          urllib.urlencode(data)))
        return rset

    def rql_entities(self, rql, entity_parameters=None):
        """ Method that dump the specified entity parameters.

        If various entities are requested by the user (Any X, Y Where ...),
        only the first one is dumped (X).
        The first requested entity must be an entity (Any X Where X is Subject)
        and NEVER an entity parameters (WRONG: Any N, X Where X is Subject, X
        name N).

        Parameters
        ----------
        rql: str (mandatory)
            the rql rquest that will be executed on the cw instance
        entity_parameters: list of str (optional)
            the list of parameters we want to return
            if None, return all the entity parameters.

        Returns
        -------
        rset_sheet: dict of dict of str
            the keys of the first dictionary correspond to row labels, and the
            keys of the second one to column labels. The table values are
            stored within this structure.
        """
        # Create a dictionary with the request meta information
        data = {
            "rql": rql,
            "vid": "e" + _EXPORT_TYPE + "export",
        }

        # Get the result set
        try:
            rset = json.load(self.opener.open(self.url, urllib.urlencode(data)))
        except:
            info = list(sys.exc_info())
            traceback.print_exc()
            traceback._print(traceback.sys.stdout,
                "".join(["Help:", self.rql_entities.__doc__]))
            sys.exit(1)

        # Filter the result
        rset_sheet = {}
        for entity_description in rset:
            row_name = (entity_description.pop("__cwetype__") + "_" +
                        str(entity_description.pop("eid")))
            # No filter, add all the entity parameters
            if entity_parameters is None:
                for key in ["modification_date", "creation_date", "cwuri"]:
                    entity_description.pop(key)
                rset_sheet[row_name] = entity_description
            # Filter the description accoring to the input scpecifications
            else:
                rset_sheet[row_name] = dict(
                    (key, value)
                    for key, value in entity_description.iteritems()
                    if key in entity_parameters)

        return rset_sheet

    def rql(self, rql):
        """ Method that loads the rset from a rql request.

        Parameters
        ----------
        rql: str (mandatory)
            the rql rquest that will be executed on the cw instance

        Returns
        -------
        rset: list of list of str
            a list that contains the requested entity parameters.
        """
        # Create a dictionary with the request meta information
        data = {
            "rql": rql,
            "vid": _EXPORT_TYPE + "export",
        }

        # Get the result set
        rset = json.load(self.opener.open(self.url, urllib.urlencode(data)))

        return rset

    ###########################################################################
    # Private Members
    ###########################################################################

    def _connect(self, password):
        """ Method to create an object that handle opening of HTTP URLs.

        .. notes::

            If the Python installation has SSL support
            (i.e., if the ssl module can be imported),
            HTTPSHandler will also be added?

        Parameters
        ----------
        password: str (mandatory)
            the cw user password.
        """
        # Create the handler
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        # Create a dictionary with the connection meta information
        data = {
            "__login": self.login,
            "__password": password,
        }
        # Connect to the cw instance
        self.opener.open(self.url, urllib.urlencode(data))

