# -*- coding: utf-8 -*-
# copyright NSAp, all rights reserved.
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

"""cubicweb-imagen schema"""

from cubicweb.schemas.base import CWUser
from cubicweb.schema import RRQLExpression, ERQLExpression
from yams.buildobjs import (
    SubjectRelation, EntityType, String, RelationDefinition)

from cubes.medicalexp.schema  import (Assessment, Subject, ExternalResource,
    ScoreValue, Device, Center, Study)
from cubes.questionnaire.schema import (
    QuestionnaireRun, Questionnaire, Question, Answer)
from cubes.neuroimaging.schema import Scan, DMRIData, PETData, MRIData
from cubes.genomics.schema import GenomicMeasure

from cubes.neuroimaging.schema import SCAN_DATA

from yams.schema import RelationSchema


###############################################################################
# Modification of the schema
###############################################################################

# Add entity to store some generic scores
class OpenAnswer(EntityType):
    identifier = String(required=True, indexed=True, maxsize=64, unique=True)
    value = String(required=True)
    question = SubjectRelation('Question', cardinality='1*', inlined=True,
        composite='object')
    questionnaire_run = SubjectRelation('QuestionnaireRun', cardinality='1*',
        inlined=True, composite='object')

# Add code_in_study to Subject entity
Subject.add_relation(String(maxsize=64, fulltextindexed=True),
                     name="code_in_study")

# Add chromset to Genomicmeasure
GenomicMeasure.add_relation(String(maxsize=64, fulltextindexed=True),
                            name="chromset")
# Replace valid attribute of Scan entity
Scan.remove_relation(name="valid")
Scan.add_relation(String(maxsize=64), name="valid")

# Remove identifier unicity constrain
QuestionnaireRun.remove_relation(name="identifier")
QuestionnaireRun.add_relation(String(required=True, indexed=True, maxsize=64),
                              name="identifier")

# To be consistent add an FMRIData and PROCESSINGData entity
SCAN_DATA += ('FMRIData', 'PROCESSINGData',)


class FMRIData(EntityType):
    voxel_res_x = Float(required=True, indexed=True)
    voxel_res_y = Float(required=True, indexed=True)
    voxel_res_z = Float(required=True, indexed=True)
    fov_x = Float(indexed=True)
    fov_y = Float(indexed=True)
    tr = Float(required=True, indexed=True)
    te = Float(required=True, indexed=True)


class PROCESSINGData(EntityType):
    pass

# Raplace inline relation for massive insertion
is_inline = True
ExternalResource.remove_relation(name="related_study")
ExternalResource.add_relation(SubjectRelation("Study", cardinality="1*",
    composite="subject", inlined=is_inline), name="r_related_study")
Assessment.remove_relation(name="related_study")
Assessment.add_relation(SubjectRelation("Study", cardinality="1*",
    composite="subject", inlined=is_inline), name="r_related_study")
QuestionnaireRun.remove_relation(name="instance_of")
QuestionnaireRun.add_relation(SubjectRelation("Questionnaire", cardinality="1*",
    composite="subject", inlined=is_inline), name="r_instance_of")
QuestionnaireRun.remove_relation(name="related_study")
QuestionnaireRun.add_relation(SubjectRelation("Study", cardinality="1*",
    composite="subject", inlined=is_inline), name="r_related_study")
QuestionnaireRun.remove_relation(name="concerns")
QuestionnaireRun.add_relation(SubjectRelation("Subject", cardinality="1*",
    composite="subject", inlined=is_inline), name="r_concerns")
QuestionnaireRun.remove_relation(name="uses_device")
QuestionnaireRun.add_relation(SubjectRelation("Device", cardinality="?*",
    inlined=is_inline), name="r_uses_device")
Question.remove_relation(name="questionnaire")
Question.add_relation(SubjectRelation("Questionnaire", cardinality="1*",
    composite="subject", inlined=is_inline), name="r_questionnaire")
Scan.remove_relation(name="concerns")
Scan.add_relation(SubjectRelation("Subject", cardinality="1*",
    composite="subject", inlined=is_inline), name="r_concerns")
Scan.remove_relation(name="has_data")
Scan.add_relation(SubjectRelation(SCAN_DATA, cardinality='?1', 
    composite='subject', inlined=is_inline), name="r_has_data")
Scan.remove_relation(name="uses_device")
Scan.add_relation(SubjectRelation("Device", cardinality="?*",
    inlined=is_inline), name="r_uses_device")
ScoreValue.remove_relation(name="measure")
ScoreValue.add_relation(SubjectRelation("Scan", cardinality="?*",
    composite="subject", inlined=False), name="r_measure")
OpenAnswer.remove_relation(name="questionnaire_run")
OpenAnswer.add_relation(SubjectRelation("QuestionnaireRun", cardinality="1*",
    composite="subject", inlined=is_inline), name="r_questionnaire_run")
OpenAnswer.remove_relation(name="question")
OpenAnswer.add_relation(SubjectRelation("Question", cardinality="1*",
    composite="subject", inlined=is_inline), name="r_question")
GenomicMeasure.add_relation(SubjectRelation("Subject", cardinality="**", inlined=False), name="related_subjects")

# Add Assessment/CWGroup relations
class can_read(RelationDefinition):
    subject = "CWGroup"
    object = "Assessment"
    cardinality = "**"


class can_update(RelationDefinition):
    subject = "CWGroup"
    object = "Assessment"
    cardinality = "**"


# Add Assessment/Entities relation
class in_assessment(RelationDefinition):
    subject = ("Scan", "FMRIData", "DMRIData", "PETData", "MRIData", 
               "PROCESSINGData", "ExternalResource", "QuestionnaireRun",
               "Questionnaire", "Question", "OpenAnswer", "ScoreValue",
               "GenomicMeasure")
    object = "Assessment"
    cardinality = "1*"
    inlined = True


###############################################################################
# Set permissions
###############################################################################

ENTITIES = [
    Scan, FMRIData, DMRIData, PETData, MRIData, PROCESSINGData, ExternalResource,
    QuestionnaireRun, Questionnaire, Question, OpenAnswer, ScoreValue,
    GenomicMeasure]


DEFAULT_PERMISSIONS = {
    "read": ("managers", "users"),
    "add": ("managers",),
    "update": ("managers",),
    "delete": ("managers",),
}


ASSESSMENT_PERMISSIONS = {
    "read": (
        "managers",
        ERQLExpression("U in_group G, G can_read X")),
    "add": (
        "managers",
        ERQLExpression("U in_group G, G can_update X")),
    "update": (
        "managers",
        ERQLExpression("U in_group G, G can_update X")),
    "delete": (
        "managers",
        ERQLExpression("U in_group G, G can_update X")),
}


RELATION_PERMISSIONS = {
    "read": (
        "managers",
        "users"),
    "add": (
        "managers",
        RRQLExpression("S in_assessment A, U in_group G, G can_update A")),
    "delete": (
        "managers",
        RRQLExpression("S in_assessment A, U in_group G, G can_update A"))
}


ENTITY_PERMISSIONS = {
    "read": (
        "managers",
        ERQLExpression("X in_assessment A, U in_group G, G can_read A")),
    "add": (
        "managers",
        ERQLExpression("X in_assessment A, U in_group G, G can_update A")),
    "update": (
        "managers",
        ERQLExpression("X in_assessment A, U in_group G, G can_update A")),
    "delete": (
        "managers",
        ERQLExpression("X in_assessment A, U in_group G, G can_update A")),
}


# Set the assessment entity permissions
Assessment.set_permissions(ASSESSMENT_PERMISSIONS)

# Set the subject/center/study entities permissions
Subject.set_permissions(DEFAULT_PERMISSIONS)
Center.set_permissions(DEFAULT_PERMISSIONS)
Study.set_permissions(DEFAULT_PERMISSIONS)
Device.set_permissions(DEFAULT_PERMISSIONS)

# Set the permissions on the used entities only
for entity in ENTITIES:
    entity.__permissions__ = ENTITY_PERMISSIONS

# Update the entities list to set relation permissions
ENTITIES.extend([Assessment, Subject, Center, Study, Device])

# Set the permissions on the ised entities relations only
for entity in ENTITIES:

    # Get the subject relations
    for relation in entity.__relations__:
        if relation.__class__ is SubjectRelation:
            relation.__permissions__ = RELATION_PERMISSIONS
