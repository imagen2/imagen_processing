#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import pygraphviz as pgv
import os


def create_schema(out_folder, fields, relations, text_font="sans-serif",
                  node_text_size=12) :
    """ Create a simple view of the database schema
    """
    # Create the graph element
    graph = pgv.AGraph(strict=False, directed=True, rankdir='LR',
                       overlap=False)

    # Insert the entity/table elements
    for entity, attributes in fields.iteritems() :
        graph.add_node(entity, style="filled", fillcolor='blue',
                       fontcolor="white", fontsize=node_text_size,
                       fontname=text_font,
                       label=entity + "|" + "|".join(attributes),
                       shape='Mrecord')

    # Set the relations between entities/tables
    for entity, relations in relations.iteritems():
        for node, relation, direction in relations:
            if direction:
                graph.add_edge(node, entity, label=relation)
            else:
                graph.add_edge(entity, node, label=relation)


    # Save the plot
    graph.draw(os.path.join(out_folder,"schema.png"), prog='dot')


def main(out_folder="/home/ag239446/tmp"):

    # Text description of each entity and associated attributes
    fields = {
        "Center": ("identifier", "city"),
        "Study": ("name",),
        "Device": ("name", "manufacturer", "model"),
        "Subject": ("identifier", "code_in_study", "gender", "handedness"),
        "Questionnaire": ("identifier", "name", "type", "test_version",
            "language"),
        "QuestionnaireRun": ("identifier", "user_ident", "iteration",
            "completed"),
        "Question": ("identifier", "text"),
        "OpenAnswer": ("value",),
        "Assessment": ("identifier", "age_of_subject"),
        "ExternalResource": ("name", "filepath"),
        "ScoreValue": ("text", "value"),
        "Scan": ("identifier", "format", "filepath", "label", "type", "valid",
                 "description", "position_acquisition"),
        "DMRIData": ("voxel_res_x", "voxel_res_y", "voxel_res_z", "fov_x",
                     "fov_y", "tr", "te"),
        "MRIData": ("voxel_res_x", "voxel_res_y", "voxel_res_z", "fov_x",
                    "fov_y", "tr", "te"),
        "FMRIData": ("voxel_res_x", "voxel_res_y", "voxel_res_z", "fov_x",
                     "fov_y", "tr", "te"),
        "PROCESSINGData": (),
    }

    # Text description of the relation between entities
    relations = {
        "Center": [],
        "Study": [],
        "Questionnaire": [],
        "Question": [("Questionnaire", "questionnaire", False)],
        "Subject": [("Study", "related_studies", False)],
        "Assessment": [("Subject", "concerned_by", True),
                       ("Center", "holds", True), 
                       ("Study","related_study", False)],
        "QuestionnaireRun": [("Assessment", "uses", True),
                             ("Questionnaire", "instance_of", False),
                             ("Subject", "concerns", False),
                             ("Study", "related_study", False)],
        "OpenAnswer": [("Question", "question", False),
                       ("QuestionnaireRun", "questionnaire_run", False) ],
        "ExternalResource" : [("Assessment", "external_resources", True),
                              ("QuestionnaireRun", "external_resources", True),
                              ("Study", "related_study", False),
                              ("Scan", "external_resources", True)],
        "Scan" : [("Subject", "concerns", False),
                  ("Assessment", "uses", True), 
                  ("Study", "related_study", False),
                  ("DMRIData", "has_data", False),
                  ("MRIData", "has_data", False),
                  ("FMRIData", "has_data", False),
                  ("ScoreValue", "measure", False),
                  ("PROCESSINGData", "has_data", False),
                  ("Device", "uses_device", False)],
    }

    create_schema(out_folder, fields, relations)


if __name__=="__main__":
    main()
    
