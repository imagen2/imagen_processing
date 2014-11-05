#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# CW iomport
from cubicweb.dataimport import SQLGenObjectStore

# Define imagen groups
IMAGEN_GROUPS = ("OPEN_BL", "OPEN_FU1", "OPEN_FU2", "RESTRICTED_BL",
                "RESTRICTED_FU1", "RESTRICTED_FU2")


class ImagenPerms(object):
    """ Class that enables us to set the database permissions (ie., create group
    and corresponding rights based on the 'in_assessment' relations).
    """

    def __init__(self, session):
        """ Initialize the ImagenPerms class

        Parameters
        ----------
        session: cw.session (mandatory)
            a cubicweb session.
        """
        # CW
        self.session = session
        self.store = SQLGenObjectStore(self.session)

    ###########################################################################
    #   Public Methods
    ###########################################################################

    def cleanup(self):
        """ Method to cleanup temporary items and to commit changes
        """
        # Send the new entities to the db
        self.store.flush() 

        # Now commit everything
        self.store.commit()

    def set_permissions(self):
        """ Set the imagen db permissions.

        Special rules for timepoints and genetic data.
        Note that this script do not deal with genetic data.
        """
        # Create/get all groups
        groups = {}
        for group_name in IMAGEN_GROUPS:

            # Create/get the entity
            group_entity = self._get_or_create_unique_entity(
                rql=("Any X Where X is CWGroup, X name "
                     "'{0}'".format(group_name)),
                entity_name="CWGroup",
                name=group_name)

            # Store the result
            groups[group_name] = group_entity

        # Get all the assessments
        rset = self.session.execute("Any X Where X is Assessment")

        # Go through all assessment entities
        for assessment_entity in rset.entities():

            # Get the timepoint
            timepoint = assessment_entity.timepoint

            # Add the relation with the group
            self._set_unique_relation(groups["OPEN_{0}".format(timepoint)].eid,
                "can_read", assessment_entity.eid)

        # Send the new entities to the db
        self.store.flush()
            


    ###########################################################################
    #   Private Methods
    ###########################################################################

    def _set_unique_relation(self, source_eid, relation_name, detination_eid,
                             check_unicity=True, subjtype=None):
        """ Method to set a relation between to entities

        Parameters
        ----------
        source_eid: str (mandatory)
            the source entity identifier.
        relation_name: str (mandatory)
            the relation name.
        detination_eid: str (mandatory)
            the destination entity identifier.
        check_unicity: bool (optional)
            if True check if the relation already exists in the data base.
        """
        # With unicity contrain
        if check_unicity:
            # First build the rql request
            rql = "Any X Where X eid '{0}', X {1} Y, Y eid '{2}'".format(
                source_eid, relation_name, detination_eid)

            # Execute the rql request
            rset = self.session.execute(rql)

            # The request returns some data -> do nothing
            if rset.rowcount == 0:
                self.store.relate(source_eid, relation_name, detination_eid,
                                  subjtype=subjtype)
                #question_entity.wx_set(source_eid, relation_name, detination_eid)

        # Without unicity constrain
        else:
            self.store.relate(source_eid, relation_name, detination_eid,
                              subjtype=subjtype)

    def _get_or_create_unique_entity(self, rql, entity_name, check_unicity=True,
                                     *args, **kwargs):
        """ Method to create a new unique entity.
        First check that the entity do not exists by executing the rql request

        Parameters
        ----------
        rql: str (madatory)
            the rql request to check unicity.
        entity_name: str (madatory)
            the name of the entity we want to create.
        check_unicity: bool (optional)
            if True check if the entity already exists in the data base.

        Returns
        -------
        entity: CW entity
            the requested entity.
        """
        # With unicity contrain
        if check_unicity:
            # First execute the rql request
            rset = self.session.execute(rql)

            # The request returns some data, get the unique entity
            if rset.rowcount > 0:
                if rset.rowcount > 1:
                    raise Exception(
                        "The database is corrupted, please "
                        "investigate: {0}.".format(entity_name))
                entity = rset.get_entity(0, 0)
            # Create a new unique entity
            else:
                entity = self.store.create_entity(entity_name, **kwargs)
        # Without unicity constrain
        else:
            entity = self.store.create_entity(entity_name, **kwargs)

        return entity
