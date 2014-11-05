#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

from cubicweb.view import View


class QuestionnaireLongitudinalView(View):
    """ Create a view that summarized the longitudinal material for a subject.
    """
    __regid__ = "questionnaire-longitudinal-measures"
    paginable = False
    div_id = "questionnaire-longitudinal-measures"

    def call(self, rset=None, patient_id="", **kwargs):
        """ Method that will create the subject longitudinal view.

        If no resultset are passed to this method, the current resultset is
        used.

        Parameters
        ----------
        rset: resultset (optional, default None)
            a  cw resultset
        patient_id: string (optional, default None)
            the patient identifier.
        """
        # Get the cw resultset
        rset = rset or self.cw_rset

        # Get the method parameters: if we use 'build_url' method, the data
        # are in the firm dictionary
        patient_id = patient_id or self._cw.form.get("patient_id", "")

        # Get the data from the result set
        questionnaires = {}
        for line_number in range(len(rset.rows)):

            # Get the questionnaire run entity
            qr_entity = rset.get_entity(line_number, 0)

            # Get the questionnaire run timepoint
            timepoint = qr_entity.in_assessment[0].timepoint

            # Get the associated questionnaire/questions
            q_entity = qr_entity.instance_of[0]
            if not q_entity.name in questionnaires:
                questionnaires[q_entity.name] = dict(
                    (entity.text, {}) 
                    for entity in q_entity.reverse_questionnaire)

            # Get the questionnaire run associated answers and fill the
            # 'questionnaires' structure
            answer_entities = qr_entity.reverse_questionnaire_run
            for entity in answer_entities:
                questionnaires[q_entity.name][entity.question[0].text][
                    timepoint] = entity.value

        # Construct the questionnaires plots
        nb_of_plots = 1
        for q_name, q_item in questionnaires.iteritems():
            for question_name, question_item in q_item.iteritems():

                # Get the plot data 
                data = sorted(question_item.items())
                x = [str(p[0]) for p in data]
                values = [p[1] for p in data]

                # Create the highcharts string representation of the data
                sdata = {
                    "x": "['" + "', '".join(x) + "']",
                    "grid": "[" + ", ".join(values) + "]"
                }
    
                # Check if we are dealing with numbers
                control_value = values[0].replace(".", "", 1)
                if control_value.isdigit():

                    # Generate the html code
                    self.wview("highcharts-basic-plot", is_hist=False, data=sdata,
                               tag="hc_container_{0}".format(nb_of_plots),
                               title="{0}-{1}: {2}".format(
                                    q_name, question_name, patient_id))

                    # Increment the plot counter
                    nb_of_plots += 1


            
            



