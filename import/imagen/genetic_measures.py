#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os
import sys

# Tool import
from zipfile import ZipFile
import tarfile
import glob
import logging

# CubicWeb import
from cubicweb.dataimport import SQLGenObjectStore

# log
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
logger.addHandler(ch)


class GenomicMeasures(object):
    """ This class enables us to pase and load genetic data
    to the cubicweb database.
    """
    def __init__(self, project_name, session=None):
        """ Initialize the class

        Parameters
        ----------
        session: Session (mandatory)
            a cubicweb session.
        genomic_file: str (mandatory)
             a file to index.
        genomic_parameters: dic (mandatory)
             dictionary of parameters (attribute, relations ...)
        """
        # CW
        self.session = session
        self.store = SQLGenObjectStore(self.session)

        # Parameters
        self.project_name = project_name
        self.parsing_output = {}

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
        self.store.commit()
        if isinstance(self.store, MassiveObjectStore):
            self.store.cleanup()
        self.session.commit()

    def parse_data(self, folder_path):
        """ Parse folder and return the file with their parameters
        """
        # get raw data
        raw_dict = {}
        for raw_file in os.listdir(os.path.join(folder_path, "converted")):
            raw_dict[raw_file] = {
                "filepath": os.path.join(folder_path, "converted", raw_file),
                "identifier": raw_file[:-4],
                "type": "raw",
                "format": "plink",
                "chromset": "all",
                "completed": False,
                "related_subjects": self._get_subjects_from_zip(
                    os.path.join(folder_path, "converted", raw_file))}

        logger.info('Raw data done')

        # get QC data
        qc_dict = {}
        for qc_file in os.listdir(os.path.join(folder_path, "qc")):
            args = qc_file[:-4].split("_")

            qc_dict[qc_file] = {
                "filepath": os.path.join(folder_path, "qc", qc_file),
                "identifier": qc_file[:-4],
                "type": "qc",
                "format": "plink",
                "related_subjects": self._get_subjects_from_zip(
                    os.path.join(folder_path,
                     "qc", qc_file))}

            if not "nonqc" in args:
                qc_dict[qc_file]["completed"] = True,
            else:
                qc_dict[qc_file]["completed"] = False

            if "autosomes" in args:
                if "X" in args:
                    qc_dict[qc_file]["chromset"] = "autosomes_X"
                else:
                    qc_dict[qc_file]["chromset"] = "autosomes"
            else:
                qc_dict[qc_file]["chromset"] = "all"

        logger.info('QC data done')
        # browse imput
        subject_map = {}
        imput_dict = {}
        for modality_folder in os.listdir(os.path.join(folder_path,
                                                       "imput")):
            for data_folder in os.listdir(os.path.join(folder_path,
                                                       "imput",
                                                        modality_folder)):
                logger.info('Imput data: %s', data_folder)
                for imput_file in os.listdir(os.path.join(folder_path,
                                                       "imput",
                                                        modality_folder,
                                                        data_folder)):
                    logger.info('---processing %s', imput_file)
                    if "chr" in imput_file:
                        if "HapMap" in modality_folder:
                            # get "ImagenImputedXXX.tgz"
                            if data_folder in subject_map:
                                subjects = subject_map[data_folder]
                            else:
                                subjects = glob.glob(os.path.join(folder_path,
                                                       "imput",
                                                        modality_folder,
                                                        data_folder,
                                                        "ImagenImputed6*0.tgz"))
                                subjects = subjects[0]
                                subjects = self._get_subjects_from_tar(subjects)
                                subject_map[data_folder] = subjects
                            chr_nbr = imput_file.split(".")[0]
                            chr_nbr = chr_nbr[4:]
                        else:
                            # get origin file
                            subjects = ("/neurospin/imagen/genetic/qc/imput/"
                                        "1kG_HlM_VF_23mai2013/genetics_rawda"
                                        "ta/all_subjects_all_snps_common.fam")
                            subjects = self._get_subjects_from_fam(subjects)
                            chr_nbr = imput_file.split(".")[0]
                            chr_nbr = chr_nbr[4:]

                        imput_dict[imput_file] = {
                            "filepath": os.path.join(
                                folder_path, "imput", modality_folder,
                                data_folder, imput_file),
                            "identifier": imput_file[:-4],
                            "type": "imput",
                            "format": 'Mach',
                            "chromset": chr_nbr,
                            "completed": False,
                            "related_subjects": subjects}

                    else:
                        if data_folder in subject_map:
                            subjects = subject_map[data_folder]
                        else:
                            subjects = self._get_subjects_from_tar(os.path.join(
                                folder_path, "imput", modality_folder, data_folder,
                                imput_file))
                            subject_map[data_folder] = subjects
                        imput_dict[imput_file] = {
                            "filepath": os.path.join(
                                folder_path, "imput", modality_folder,
                                data_folder, imput_file),
                            "identifier": imput_file[:-4],
                            "type": "imput",
                            "format": 'plink',
                            "chromset": "autosomes",
                            "completed": False,
                            "related_subjects": subjects}

        logger.info('Imput data done')
        self.parsing_output = {"raw": raw_dict,
                               "qc": qc_dict,
                               "imput": imput_dict}

    def import_genomic_measure(self, ):
        """ Method that import genomic measures in the db based on parameters
        The database is already filles with subject and scan entities
        """
        """
        for entry in self.parsing_output:
            for sub_entry in self.parsing_output[entry]:
                print self.parsing_output[entry][sub_entry]
                print "#" * 40
        """
        # Study
        estudy = self._get_or_create_unique_entity(
            rql=("Any X Where X is Study, X name 'IMAGEN'"),
                 entity_name="Study",
                 name="IMAGEN")

        # Assessment
        eassessment = self._get_or_create_unique_entity(
            rql=("Any X Where X is Assessment, X timepoint "
                 "'BL', X identifier 'IMAGEN_dna'"),
            entity_name="Assessment",
            timepoint="BL",
            identifier="IMAGEN_dna")
        self._set_unique_relation(eassessment.eid, self.rtype_map["related_study"],
                                  estudy.eid, subjtype="Assessment")

        # Get all subjects in memory
        all_subject_psc2 = []
        for gtype, gdict in self.parsing_output.iteritems():
            for ctype, cdict in gdict.iteritems():
                all_subject_psc2.extend(cdict["related_subjects"])
        all_subject_psc2 = set(all_subject_psc2)

        nb_of_unique_psc2 = len(all_subject_psc2)
        subject_entities = {}
        for cnt, subject_psc2 in enumerate(all_subject_psc2):

            # Progress bar
            ratio = float(cnt + 1) / float(nb_of_unique_psc2)
            self._progress_bar(ratio, title="Importing subjects")

            # Subject
            subject_identifier = "IMAGEN_{0}".format(subject_psc2)
            esubject = self._get_or_create_unique_entity(
                rql=("Any X Where X is Subject, X identifier "
                     "'{0}'".format(subject_identifier)),
                entity_name="Subject",
                code_in_study=subject_psc2,
                gender="unknown",
                identifier=subject_identifier,
                handedness="unknown")
            self._set_unique_relation(
                esubject.eid, "concerned_by", eassessment.eid,
                subjtype="Subject", check_unicity=False)
            subject_entities[subject_psc2] = esubject

        # Group
        # Create/get the entity
        egroup = self._get_or_create_unique_entity(
            rql=("Any G Where G is CWGroup, G name 'RESTRICTED_BL'"),
            entity_name="CWGroup",
            name="RESTRICTED_BL")
        self._set_unique_relation(egroup.eid, "can_read", eassessment.eid)
        
        # Insert the genomic measures
        for entry in self.parsing_output:

            # Message
            logger.info('')
            logger.info('Indexing %s', entry)

            ntot = len(self.parsing_output[entry])
            for cnt, sub_entry in enumerate(self.parsing_output[entry]):

                # Progress bar
                ratio = float(cnt + 1) / float(ntot)
                self._progress_bar(ratio, title="Indexing {0}".format(entry))

                # Get the related subjects
                related_subjects = self.parsing_output[entry][sub_entry].pop(
                    "related_subjects")

                # GenomicMeasure
                egenomicmeasure = self._get_or_create_unique_entity(
                    rql=("Any X Where X is GenomicMeasure, "
                         "X identifier '{0}'".format(
                            self.parsing_output[entry][sub_entry]["identifier"])),
                    entity_name="GenomicMeasure",
                    **self.parsing_output[entry][sub_entry])
                self._set_unique_relation(
                    egenomicmeasure.eid, "related_study", estudy.eid,
                    subjtype='GenomicMeasure')
                self._set_unique_relation(
                    eassessment.eid, "generates", egenomicmeasure.eid,
                    subjtype='Assessment')
                self._set_unique_relation(
                    egenomicmeasure.eid, "in_assessment", eassessment.eid,
                    subjtype='GenomicMeasure')

                # Link this measure with all concerned subjects
                for psc2 in set(related_subjects):

                    # Subject
                    esubject = subject_entities[psc2]
                    self._set_unique_relation(
                        egenomicmeasure.eid, "related_subjects", esubject.eid,
                        subjtype="GenomicMeasure", check_unicity=False)               

                # GenomicPlatform
                if entry == "raw" or entry == "qc":
                    if "wave1" in sub_entry:
                        egenomicplatform = self._get_or_create_unique_entity(
                            rql=("Any X Where X is GenomicPlatform, "
                                 "X identifier 'Illumina610'"),
                            entity_name="GenomicPlatform",
                            identifier="Illumina610")
                    elif "wave2" in sub_entry or "wave3" in sub_entry:
                        egenomicplatform = self._get_or_create_unique_entity(
                            rql=("Any X Where X is GenomicPlatform, "
                                 "X identifier 'Illumina660'"),
                            entity_name="GenomicPlatform",
                            identifier="Illumina660")
                    else:
                        logger.error(
                            self.parsing_output[entry][sub_entry]["filepath"])
                        raise Exception('Unknown platform for %s', sub_entry)
                else:
                    if "1kG" in self.parsing_output[entry][sub_entry]["filepath"]:
                        egenomicplatform = self._get_or_create_unique_entity(
                            rql=("Any X Where X is GenomicPlatform, "
                                 "X identifier '1000_Genomes'"),
                            entity_name="GenomicPlatform",
                            identifier="1000_Genomes")
                    elif "HapMap" in self.parsing_output[entry][sub_entry]["filepath"]:
                        egenomicplatform = self._get_or_create_unique_entity(
                            rql=("Any X Where X is GenomicPlatform, "
                                 "X identifier 'HapMap_r2.3'"),
                            entity_name="GenomicPlatform",
                            identifier="HapMap_r2.3")
                    else:
                        logger.error(
                            self.parsing_output[entry][sub_entry]["filepath"])
                        raise Exception('Unknown platform for {0}'.format(
                            sub_entry))

                # Link to platform
                self._set_unique_relation(
                    egenomicmeasure.eid, "platform", egenomicplatform.eid,
                    subjtype='GenomicMeasure')

                # Send the new entities/relations to the db
                self.store.flush()  

        # Send the new entities to the db
        self.store.flush()

    ###########################################################################
    #   Private Methods
    ###########################################################################

    def _get_subjects_from_fam(self, path_to_file):
        _file = open(path_to_file)
        subject_list = []
        for item in _file.readlines():
            if item:
                subject_list.append(item.split(" ")[0])
        _file.close()
        return subject_list

    def _get_subjects_from_zip(self, path_to_archive):
        """ Get subject concerned by the file in path
        """
        # select .fam file from archive
        zipfile = ZipFile(path_to_archive)
        list_file = zipfile.namelist()
        for item in list_file:
            if ".fam" in item:
                file_name = item
                break
        _buffer = zipfile.read(file_name)
        lines = _buffer.split("\n")
        subject_list = []
        for item in lines:
            if item:
                subject_list.append(item.split(" ")[0])
        
        zipfile.close()
        return subject_list


    def _fam_files(self, members):
        for tarinfo in members:
            if os.path.splitext(tarinfo.name)[1] == ".fam":
                return tarinfo.name

    def _get_subjects_from_tar(self, path_to_archive):
        """ Get subject concerned by the file in path
        """
        # select .fam file from archive
        tar = tarfile.open(path_to_archive)
        _buffer = tar.extractfile(self._fam_files(tar))
        _buffer = _buffer.read()
        lines = _buffer.split("\n")
        subject_list = []
        for item in lines:
            if item:
                subject_list.append(item.split(" ")[0])
        
        tar.close()
        return subject_list

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

    def _get_unique_entity(self, rql, entity_name, *args, **kwargs):
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
            raise Exception("no entry found, please investigate {0}".format(
                rql))
        return entity

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

        # Without unicity constrain
        else:
            self.store.relate(source_eid, relation_name, detination_eid,
                              subjtype=subjtype)

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
