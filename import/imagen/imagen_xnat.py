#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
from lxml import etree
import re
import hashlib
import os
import logging
import sys
import copy

# CW iomport
from cubicweb.dataimport import SQLGenObjectStore
from dataio.dataimport import MassiveObjectStore

# Parser import
from imagen_xnat_parser import (build_scan, eval_xml_path, build_questionnaire)
from imagen_xnat_parser import xnat_patient_structure as xnat_patient_structure_ref
from imagen_xnat_parser import xnat_scan_structure as xnat_scan_structure_ref
from imagen_xnat_parser import xnat_questionnaire_structure as xnat_questionnaire_structure_ref


class XnatConverter(object):
    """ Class that enables the conversion of the xnat imagen database to the
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
        # CW
        self.session = session
        self.inline_relations_in_schema = inline_relations_in_schema
        self.massive_importation = massive_importation
        if not self.massive_importation:
            self.store = SQLGenObjectStore(self.session)
        else:
            self.store = MassiveObjectStore(self.session)

        # Structure to speed up the insertion
        self.assessment_entities = {}
        self.questionnaire_entities = {}
        self.question_entities = {}

        # Relation mapping
        self.rtype_map = {
            "related_study": "r_related_study",
            "instance_of": "r_instance_of",
            "concerns": "r_concerns",
            "uses_device": "r_uses_device",
            "measure": "r_measure",
            "questionnaire": "r_questionnaire",
            "has_data": "r_has_data",
            "question": "r_question",
            "questionnaire_run": "r_questionnaire_run",
        }

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
        if self.massive_importation:
            self.store.cleanup()

    def parse(self, xml_file):
        """ Method to get the data we want to insert.
        """
        # Load the xml file
        tree = etree.parse(xml_file)
        xml_root = tree.getroot()
        nsmap = xml_root.nsmap

        # Parse the xml file
        xnat_patient_structure = copy.deepcopy(xnat_patient_structure_ref)
        xnat_questionnaire_structure = copy.deepcopy(
            xnat_questionnaire_structure_ref)
        xnat_scan_structure = copy.deepcopy(xnat_scan_structure_ref)
        eval_xml_path(xnat_patient_structure, xml_root, nsmap, True)
        eval_xml_path(xnat_questionnaire_structure, xml_root, nsmap, False)
        eval_xml_path(xnat_scan_structure, xml_root, nsmap, False)

        # Hack the code in study field to get the psc1 code
        cis = xnat_patient_structure["Subject"]["code_in_study"]
        xnat_patient_structure["Subject"]["code_in_study"] = cis.replace("IMAGEN_", "")

        # Organize the parsed data to be compliant with the cw organization
        # Do questionnaire
        patient_questionnaires = []
        for qname, qtypes in xnat_questionnaire_structure.iteritems():
            for qtype, qelements in qtypes.iteritems():
                for qelement in qelements:
                    if len(qelement) == 1:
                        patient_questionnaires.append(
                            self._build_questionnaire(qelement[0], nsmap))

        # Do scan
        patient_scans = []
        for sname, stypes in xnat_scan_structure.iteritems():
            for stype, selements in stypes.iteritems():
                for selement in selements:
                    patient_scans.append(self._build_scan(selement, nsmap))

        self.xnat_patient_structure = xnat_patient_structure
        self.patient_questionnaires = patient_questionnaires
        self.patient_scans = patient_scans

    def import_in_db(self, insert=True):
        """ Export the xml description of a patient informations inserted in the
        xnat database.
        """
        # Set local variables
        xnat_patient_structure = self.xnat_patient_structure
        patient_questionnaires = self.patient_questionnaires
        patient_scans = self.patient_scans

        # First get/create the study, the center, the device, and the subject
        center_entity = self._get_or_create_unique_entity(
            rql=("Any X Where X is Center, X identifier "
                 "'{0}'".format(
                 xnat_patient_structure["Center"]["identifier"].strip("'\""))),
            entity_name="Center",
            **xnat_patient_structure["Center"])
        study_entity = self._get_or_create_unique_entity(
            rql=("Any X Where X is Study, X name "
                 "'{0}'".format(
                 xnat_patient_structure["Study"]["name"].strip("'\""))),
            entity_name="Study",
            **xnat_patient_structure["Study"])
        device_entity = self._get_or_create_unique_entity(
            rql=("Any X Where X is Device, X model "
                 "'{0}'".format(
                 xnat_patient_structure["Device"]["model"].strip("'\""))),
            entity_name="Device",
            **xnat_patient_structure["Device"])
        subject_entity = self._get_or_create_unique_entity(
            rql=("Any X Where X is Subject, X identifier "
                 "'{0}'".format(
                 xnat_patient_structure["Subject"]["identifier"].strip("'\""))),
            entity_name="Subject",
            **xnat_patient_structure["Subject"])
        self._set_unique_relation(subject_entity.eid, "related_studies",
                                  study_entity.eid)

        # do not insert questionnaire for the moment
        # ToDo: uncomment me.
        if 0:
            # Then get/create all the questionnaires
            for patient_questionnaire in patient_questionnaires:

                # Assessment
                assessment_intern_tag = "{0}_{1}".format(
                    patient_questionnaire["Assessment"]["age_of_subject"],
                    patient_questionnaire["Assessment"]["identifier"])
                if assessment_intern_tag in self.assessment_entities:
                    assessment_entity = self.assessment_entities[assessment_intern_tag]
                else:
                    assessment_entity = self._get_or_create_unique_entity(
                        rql=("Any X Where X is Assessment, X identifier "
                             "'{0}', X age_of_subject '{1}'".format(
                             patient_questionnaire["Assessment"]["identifier"].strip("'\""),
                             patient_questionnaire["Assessment"]["age_of_subject"].strip("'\""))),
                        entity_name="Assessment",
                        check_unicity=False,
                        **patient_questionnaire["Assessment"])
                    self.assessment_entities[
                        assessment_intern_tag] = assessment_entity
                    self._set_unique_relation(assessment_entity.eid,
                        self.rtype_map["related_study"], study_entity.eid, subjtype="Assessment")
                    self._set_unique_relation(subject_entity.eid,
                        "concerned_by", assessment_entity.eid)
                    self._set_unique_relation(center_entity.eid,
                        "holds", assessment_entity.eid)

                    # Group
                    group_name = "OPEN_{0}".format(
                        patient_questionnaire["Assessment"]["timepoint"])
                    # Create/get the entity
                    group_entity = self._get_or_create_unique_entity(
                        rql=("Any X Where X is CWGroup, X name "
                             "'{0}'".format(group_name)),
                        entity_name="CWGroup",
                        name=unicode(group_name))
                    self._set_unique_relation(group_entity.eid,
                        "can_read", assessment_entity.eid)                    

                # Questionnaire
                questionnaire_intern_tag = patient_questionnaire["Questionnaire"]["name"]
                if questionnaire_intern_tag in self.questionnaire_entities:
                    questionnaire_entity = self.questionnaire_entities[questionnaire_intern_tag]
                    # ToDo: restore the question_entities structure? I think it is
                    # not necessary but I may be wrong.
                else:
                    # Create a questionnaire form
                    questionnaire_entity = self._get_or_create_unique_entity(
                        rql=("Any X Where X is Questionnaire, X name "
                             "'{0}'".format(
                             patient_questionnaire["Questionnaire"]["name"].strip("'\""))),
                        entity_name = "Questionnaire",
                        check_unicity=False, ##
                        **patient_questionnaire["Questionnaire"])
                    self.questionnaire_entities[
                        questionnaire_intern_tag] = questionnaire_entity
                    self.question_entities[questionnaire_intern_tag] = {}


                # Create corresponding questions
                # Need to check that questions are all in memory
                # Xnat do not export null fields
                for question in patient_questionnaire["Question"]:
                    if not question["text"] in self.question_entities[questionnaire_intern_tag]:
                        question_entity = self._get_or_create_unique_entity(
                            rql=("Any X Where X is Question, X identifier "
                                 "'{0}'".format(
                                 question["identifier"].strip("'\""))),
                            entity_name = "Question",
                            check_unicity=False, ##
                            **question)
                        self.question_entities[questionnaire_intern_tag][
                            question["text"]] = question_entity
                        self._set_unique_relation(question_entity.eid, 
                            self.rtype_map["questionnaire"],
                            questionnaire_entity.eid, subjtype="Question")

                # Get access directly to questions
                question_entities = self.question_entities[questionnaire_intern_tag]

                # QuestionnaireRun (always inserted)
                qr_entity = self._get_or_create_unique_entity(
                    rql="",
                    entity_name="QuestionnaireRun",
                    check_unicity=False,
                    **patient_questionnaire["QuestionnaireRun"])
                self._set_unique_relation(qr_entity.eid, self.rtype_map["instance_of"],
                    questionnaire_entity.eid, subjtype="QuestionnaireRun")
                self._set_unique_relation(assessment_entity.eid, "uses",
                    qr_entity.eid)
                self._set_unique_relation(qr_entity.eid, self.rtype_map["related_study"],
                    study_entity.eid, subjtype="QuestionnaireRun")
                self._set_unique_relation(qr_entity.eid, self.rtype_map["concerns"],
                    subject_entity.eid, subjtype="QuestionnaireRun")
                self._set_unique_relation(qr_entity.eid, "in_assessment",
                    assessment_entity.eid, subjtype="QuestionnaireRun")

                # OpenAnswer (always inserted)
                for answer in patient_questionnaire["OpenAnswer"]:
                    question_intern_tag = answer.pop("text") 
                    question_entity = question_entities[question_intern_tag]
                    answer_entity = self._get_or_create_unique_entity(
                        rql="",
                        entity_name="OpenAnswer",
                        check_unicity=False,
                        **answer)
                    self._set_unique_relation(answer_entity.eid, self.rtype_map["question"],
                        question_entity.eid, subjtype="OpenAnswer")
                    self._set_unique_relation(answer_entity.eid, self.rtype_map["questionnaire_run"],
                        qr_entity.eid, subjtype="OpenAnswer")
                    self._set_unique_relation(answer_entity.eid, "in_assessment",
                        assessment_entity.eid, subjtype="OpenAnswer")

                # ExternalResource (always inserted)
                for resource in patient_questionnaire["ExternalResource"]:
                    resource_entity = self._get_or_create_unique_entity(
                        rql="",
                        entity_name="ExternalResource",
                        check_unicity=False,
                        **resource)
                    self._set_unique_relation(qr_entity.eid,
                        "external_resources", resource_entity.eid)
                    self._set_unique_relation(resource_entity.eid,
                        self.rtype_map["related_study"], study_entity.eid,
                        subjtype="ExternalResource")
                    self._set_unique_relation(resource_entity.eid, "in_assessment",
                        assessment_entity.eid, subjtype="ExternalResource")

        # Then get/create all the scans
        if 0:
            print patient_scans[0]["ExternalResource"][0]
            print patient_scans[0]["Scan"][0][0]
            print patient_scans[0]["Scan"][0][1]
            print patient_scans[0]["Assessment"][0]
            print patient_scans[0]["ScoreValue"]
            print len(patient_scans)
            print xnat_patient_structure

        # Create a object to store all inserted scans, remove dicomtarballs
        # systematically
        inserted_scan_eids = []
        
        # Go through all patient scans
        for patient_scan in patient_scans:

            # Assessment + Scan (always inserted)
            scan_entities = []
            for scan_item, assessment_item in zip(
                        patient_scan["Scan"], patient_scan["Assessment"]):

                # Create the assessment
                assessment_intern_tag = "{0}_{1}".format(
                    assessment_item["age_of_subject"],
                    assessment_item["identifier"])
                if assessment_intern_tag in self.assessment_entities:
                    assessment_entity = self.assessment_entities[assessment_intern_tag]
                else:
                    assessment_entity = self._get_or_create_unique_entity(
                        rql=("Any X Where X is Assessment, X identifier "
                             "'{0}', X age_of_subject '{1}'".format(
                             assessment_item["identifier"].strip("'\""),
                             assessment_item["age_of_subject"].strip("'\""))),
                        entity_name="Assessment",
                        check_unicity=False,
                        **assessment_item)
                    self.assessment_entities[
                        assessment_intern_tag] = assessment_entity
                    self._set_unique_relation(assessment_entity.eid,
                        self.rtype_map["related_study"], study_entity.eid, subjtype="Assessment")
                    self._set_unique_relation(subject_entity.eid,
                        "concerned_by", assessment_entity.eid)
                    self._set_unique_relation(center_entity.eid,
                        "holds", assessment_entity.eid)

                    # Group
                    group_name = "OPEN_{0}".format(
                        assessment_item["timepoint"])
                    # Create/get the entity
                    group_entity = self._get_or_create_unique_entity(
                        rql=("Any X Where X is CWGroup, X name "
                             "'{0}'".format(group_name)),
                        entity_name="CWGroup",
                        name=unicode(group_name))
                    self._set_unique_relation(group_entity.eid,
                        "can_read", assessment_entity.eid)

                if (scan_item[0]["format"] is not None and
                    "DICOM" not in scan_item[0]["format"] and 
                    scan_item[0]["identifier"] not in inserted_scan_eids):

                    # Store the new scan eid
                    inserted_scan_eids.append(scan_item[0]["identifier"])

                    # Create the scan entity
                    scan_entity = self._get_or_create_unique_entity(
                            rql=("Any X Where X is Scan, X identifier "
                                 "'{0}'".format(scan_item[0]["identifier"])),
                            entity_name="Scan",
                            check_unicity=False,
                            **scan_item[0])
                    self._set_unique_relation(scan_entity.eid,
                        self.rtype_map["uses_device"], device_entity.eid, subjtype="Scan")
                    self._set_unique_relation(scan_entity.eid,
                        self.rtype_map["concerns"], subject_entity.eid, subjtype="Scan")
                    self._set_unique_relation(assessment_entity.eid,
                        "uses", scan_entity.eid)
                    self._set_unique_relation(scan_entity.eid, "in_assessment",
                        assessment_entity.eid, subjtype="Scan")
                    
                    # Type this entity if necessary
                    dtype_struct = None
                    if scan_item[1] is not None:
                        dtype_struct = scan_item[1].copy()
                    if dtype_struct is not None:
                        dtype = dtype_struct.pop("type")
                        dtype_entity = self._get_or_create_unique_entity(
                            rql="",
                            entity_name=dtype,
                            check_unicity=False,
                            **dtype_struct)
                        self._set_unique_relation(scan_entity.eid,
                            self.rtype_map["has_data"], dtype_entity.eid,
                            subjtype="Scan")
                        self._set_unique_relation(dtype_entity.eid, "in_assessment",
                            assessment_entity.eid, subjtype=dtype)

                    # Store created scan entities
                    scan_entities.append(scan_entity)

            # Send the new entities to the db
            self.store.flush()

            # External resource (always inserted)
            for resource_item in patient_scan["ExternalResource"]:
                # Create the resource entity
                resource_entity = self._get_or_create_unique_entity(
                    rql="",
                    entity_name="ExternalResource",
                    check_unicity=False,
                    **resource_item)
                self._set_unique_relation(resource_entity.eid,
                    self.rtype_map["related_study"], study_entity.eid,
                    subjtype="ExternalResource")
                for scan_entity in scan_entities:
                    assessment_entity = scan_entity.in_assessment[0]
                    self._set_unique_relation(scan_entity.eid,
                        "external_resources", resource_entity.eid)
                    self._set_unique_relation(resource_entity.eid, "in_assessment",
                        assessment_entity.eid, subjtype="ExternalResource")

            # Score value (always inserted) 
            for score_item in patient_scan["ScoreValue"]:
                # Create the resource entity
                score_entity = self._get_or_create_unique_entity(
                    rql="",
                    entity_name="ScoreValue",
                    check_unicity=False,
                    **score_item)
                for scan_entity in scan_entities:
                    assessment_entity = scan_entity.in_assessment[0]
                    self._set_unique_relation(scan_entity.eid,
                        self.rtype_map["measure"], score_entity.eid, subjtype="Scan")
                    self._set_unique_relation(score_entity.eid, "in_assessment",
                        assessment_entity.eid, subjtype="ScoreValue")

        # Send the new entities to the db
        self.store.flush()           

    ###########################################################################
    #   Private Parsing Xml Methods
    ###########################################################################

    def _build_scan(self, scan_xml_elements, nsmap=None):
        """ Method to construct the scan (scan - external resource - score value)
        from an IMAGEN scan element.

        Parameters
        ----------
        scan_xml_elements: list of lxml.etree._Element (mandatory)
            list of structures that contain the imagen scan informations.
            The first item may contains sequence information as spacing.
            If the last item is not None, it is considered as an external resource
            of all the other elements
        nsmap: dict (optional)
            namespace where to execute the xml command

        Returns
        -------
        cw_scan: list dict
            a list of dictionaries with four keys (Scan - ExternalResource -
            *Data - ScoreValue) that contains the entity parameter decriptions
        """
        return build_scan(scan_xml_elements, nsmap)

    def _build_questionnaire(self, questionnaire_xml_element, nsmap=None):
        """ Method to construct the questionnaire (questions - answers) from
        an IMAGEN experiment element.
    
        Parameters
        ----------
        questionnaire_xml_element: lxml.etree._Element (mandatory)
            structure that contains the imagen questionnaire informations.
        nsmap: dict (optional)
            namespace where to execute the xml command

        Returns
        -------
        cw_questionnaire: dict
            a dictionary with six keys (Questionnaire - QuestionnaireRun -
            Question - OpenAnswer - ExternalResource - Assessment) that
            contains the entity parameter decriptions
        """
        return build_questionnaire(questionnaire_xml_element, nsmap)

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
        # Remove subjtype for massive importation since the store do not deal
        # with inline relations
        if not self.inline_relations_in_schema:
            subjtype = None

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

    def _progress_bar(self, ratio, title="", bar_length=40):
        """ Method to generate a progress bar.

        Parameters
        ----------
        ratio: float (mandatory 0<ratio<1)
            float describing the current processing status.
        title: str (optional)
            a title to identify the progress bar.
        bar_length: int (optional)
            the length of the bar that will be ploted.
        """
        progress = int(ratio * 100.)
        block = int(round(bar_length * ratio))
        text = "\r{2} in Progress: [{0}] {1}%".format(
            "=" * block + " " * (bar_length - block), progress, title)
        sys.stdout.write(text)
        sys.stdout.flush()


if __name__ == "__main__":

    xml_file = "/home/ag239446/tmp/IMAGEN_000000001274.xml"
    converter = XnatConverter(None)
    converter.import_xml_file(xml_file)
        
