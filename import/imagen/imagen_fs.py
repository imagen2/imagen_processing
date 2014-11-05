#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Bioresource import
from imagen_xnat import XnatConverter


class FsConverter(XnatConverter):
    """ Class that enables the conversion of the imagen file system to the
    cubicweb 3.17.4 database system.
    """

    def __init__(self, session, massive_importation=False,
                 inline_relations_in_schema=True):
        """ Initialize the NcbiMeta class

        Parameters
        ----------
        session: cw.session (mandatory)
            a cubicweb session.
        massive_importation: bool (optional: default False)
            if set to True use a massive object store, otherwise use a sqlgen 
            object store.
        inline_relations_in_schema: bool (optional: default True)
            if set to False, assume that no inlined relation will be inserted.
        """
        # Inheritance
        super(FsConverter, self).__init__(session, massive_importation,
                                          inline_relations_in_schema)

    ###########################################################################
    #   Public Methods
    ###########################################################################

    def parse(self, patient_structure, patient_questionnaires, patient_scans):
        """ Method to get the data we want to insert.
        """
        self.xnat_patient_structure = patient_structure
        self.patient_questionnaires = patient_questionnaires
        self.patient_scans = patient_scans
