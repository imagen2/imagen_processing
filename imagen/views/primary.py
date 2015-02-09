#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

from cubicweb.view import EntityStartupView
from cubicweb.web.views.ajaxcontroller import ajaxfunc
import cubes.imagen as cube
import os


@ajaxfunc(output_type='json')
def csv_download(self, qname, timepoint, headers_str):

    rql_all = ("Any SID, QUT, OAV WHERE QR is QuestionnaireRun, "
               "OA r_questionnaire_run QR, OA r_question QU, OA value OAV, "
               "QU r_questionnaire Q, QU text QUT, QR r_concerns S, "
               "S code_in_study SID,QR r_instance_of Q, Q name '{0}', "
               "QR in_assessment A, A timepoint '{1}'".format(qname, timepoint))
    rset_all = self._cw.execute(rql_all)

    subject_rset = {}
    for line in rset_all:
        patient_id = line[0]
        question_text = line[1]
        answer_value = line[2]
        if patient_id not in subject_rset.keys():
            subject_rset[patient_id] = {}
        subject_rset[patient_id][question_text] = answer_value

    buff = ""
    for head in headers_str.split():
            buff += "{0}, ".format(head)
    buff += "\n"

    for subject, value in sorted(subject_rset.iteritems()):
        buff += "{0}, ".format(subject)
        for question, answer in sorted(value.iteritems()):
            if answer and len(str(answer)):
                buff += "{0}, ".format(answer)
            else:
                buff += "-, "
        buff += "\n"

    login = self._cw.session.login
    path = os.path.join(cube.__path__[0], "data", "tmp", '{0}_table_{1}_{2}.csv'
                        .format(login, qname, timepoint))
    _csvFile = open(path, 'wb')
    _csvFile.write(buff)
    _csvFile.close()

    url = self._cw.data_url(path)
    link = {"dl_url": url}

    return link


@ajaxfunc(output_type='json')
def get_db_data(self, jtstartindex, jtpagesize,
                nb_subjects, nb_questions, qname, timepoint):

    rql_all = ("Any SID, QUT, OAV ORDERBY SID LIMIT {2} OFFSET {3} "
               "WHERE QR is QuestionnaireRun, OA r_questionnaire_run QR, "
               "OA r_question QU, OA value OAV, QU r_questionnaire Q, "
               "QU text QUT, QR r_concerns S, S code_in_study SID, "
               "QR r_instance_of Q, Q name '{0}', QR in_assessment A, "
               "A timepoint '{1}'".format(qname, timepoint,
                                          jtpagesize*nb_questions,
                                          jtstartindex*nb_questions))
    rset_all = self._cw.execute(rql_all)

    subject_rset = {}
    for line in rset_all:
        patient_id = line[0]
        question_text = line[1]
        answer_value = line[2]
        if patient_id not in subject_rset.keys():
            subject_rset[patient_id] = {}
        subject_rset[patient_id][question_text] = answer_value

    records = []
    cnt = jtstartindex + 1
    for key, value in sorted(subject_rset.iteritems()):
        subject_dict = {'PatientID': key, 'row': cnt}
        for key1, value1 in value.iteritems():
            subject_dict[key1] = value1
        records.append(subject_dict)
        cnt += 1

    data = {"Result": "OK",
            "Records": records,
            "TotalRecordCount": nb_subjects}

    return data


class QuestionnaireRunsView(EntityStartupView):
    __regid__ = 'questionnaireruns_view'
    title = "QuestionnaireRun"

    def call(self, **kwargs):

        qname = self._cw.form['qname']
        timepoint = self._cw.form['timepoint']

        rql_nb_subjects = "Any COUNT(SID) WHERE QR is QuestionnaireRun, " \
                          "QR r_concerns S, S code_in_study SID, " \
                          "QR r_instance_of Q, Q name '{0}', QR in_assessment A," \
                          " A timepoint '{1}'".format(qname, timepoint)
        nb_subjects_rset = self._cw.execute(rql_nb_subjects)
        nb_subjects = int(nb_subjects_rset[0][0])

        rql_nb_questions = "Any COUNT(QU) WHERE Q is Questionnaire, " \
                           "Q name '{0}', QU r_questionnaire Q".format(qname)
        nb_questions_rset = self._cw.execute(rql_nb_questions)
        nb_questions = int(nb_questions_rset[0][0])

        rql_questions_text = "Any QUT ORDERBY QUT WHERE Q is Questionnaire, " \
                             "QU r_questionnaire Q, QU text QUT, " \
                             "Q name '{0}'".format(qname)
        questions_text_rset = self._cw.execute(rql_questions_text)

        headers_str = ""
        fields_str = "{"
        fields_str += "row:{key:true,title:'row'},"
        fields_str += "PatientID:{title:'PatientID'},"
        headers_str += "PatientID "
        for question_text in questions_text_rset:
                fields_str += "%s:{title:'%s'},"\
                              % (question_text[0], question_text[0])
                headers_str += "%s " % (question_text[0])
        fields_str += "}"

        self._cw.add_js('jtable.2.4.0/jquery.jtable.min.js')
        self._cw.add_css('jtable.2.4.0/themes/lightcolor/blue/jtable.css')
        wait_image_path = os.path.join(cube.__path__[0], "data",
                                       "images", 'please_wait2.gif')
        image_url = self._cw.data_url(wait_image_path)
        html = """<div id='loadingmessage' style='display:none' align="center">
  <img src='""" + image_url + """'/>
</div>"""
        html += '<div style="overflow:auto;height: 100%; width: 140%;">'
        html += """<div id="PatientTableContainer"></div>"""
        html += """<script type="text/javascript">

    $(document).ready(function () {

        $('#PatientTableContainer').jtable({
            title: '""" + str(qname).upper() + """ """ + str(timepoint).upper()\
                + """',
            paging: true,
            pageSize: 10,
            selecting: true,
            multiselect: true,
            toolbar: {
                hoverAnimation: true,
                hoverAnimationDuration: 5,
                hoverAnimationEasing: undefined,
                items: [{
                    icon: '/images/excel.png',
                    text: 'Export to Excel',
                    click: function() {
    $('#loadingmessage').show();
    var post = $.ajax({
    url: 'json?fname=csv_download&arg=' + """ + """'"{0}"'"""\
            .format(str(qname)) + """ + '&arg=' + """ + """'"{0}"'"""\
            .format(str(timepoint)) + """ + '&arg=' + """ + """'"{0}"'"""\
            .format(str(headers_str)) + """,
    data: {json: JSON.stringify({dl_url: "Jose"})} ,
    type: "POST"
});

post.done(function(p){
    window.location = p.dl_url
    $('#loadingmessage').hide();
});

post.fail(function(){
    alert("Error : Download Failed!");
});
}
                }]
            },
            actions: {
                listAction: function (postData, jtParams) {
                    return $.Deferred(function ($dfd) {
                        $.ajax({
                            url: 'json?fname=get_db_data&arg=' + jtParams.jtStartIndex + '&arg=' + jtParams.jtPageSize + '&arg=' + """\
                + str(nb_subjects) + """ + '&arg=' + """ \
                + str(nb_questions) + """ + '&arg=' + """ + """'"{0}"'"""\
            .format(str(qname)) + """ + '&arg=' + """ + """'"{0}"'"""\
            .format(str(timepoint)) + """,
                            type: 'POST',
                            dataType: 'json',
                            data: postData,
                            success: function (data) {
                                $dfd.resolve(data);
                            },
                            error: function () {
                                $dfd.reject();
                            }
                        });
                    });
                },
            },
            fields: """

        html += fields_str

        html += """
        });

        $('#PatientTableContainer').jtable('load');
    });

</script>"""
        html += "</div>"

        self.w(u'{0}'.format(html))


class QuestionnairesView(EntityStartupView):
    __regid__ = 'questionnaires_view'
    title = "Questionnaire"

    def call(self, **kwargs):

        rql = " Any QN WHERE Q is Questionnaire, Q name QN"
        qname_rset = self._cw.execute(rql)
        sorted_qname = sorted(qname_rset)
        headers = ["Questionnaire"]
        timepoints = ["BL", "FU1", "FU2"]
        cell_size = 300
        html = '<div style="height: 400px; width: 100%;">'
        max_size = (len(headers) + 1) * cell_size
        html += ('<div style="height:60px; width: {0}px;">'.format(max_size))
        html += '<table class="table table-bordered" style="width: 100%;">'
        html += "<tr>"
        for head in headers:
            html += ('<td style="width:{1}px;" bgcolor="#428BCA">'
                     '<strong>{0}</strong></td>'.format(head, cell_size))
        html += "</tr>"
        html += "</table>"
        html += "</div>"
        html += ('<div style="height: '
                 '300px; width: {0}px;">'.format(max_size))
        html += ('<table class="table table-bordered" '
                 'style="width: 100%;">')
        for qname in sorted_qname:
            html += ('<tr><td style="width:{1}px"><strong>{0}</strong></a>'
                     '</td>'.format(qname[0], cell_size))
            for timepoint in timepoints:
                html += '<td style="width:{1}px"><a href="{2}">{0}</td>'.format(
                        timepoint, cell_size,
                        self._cw.build_url(vid='questionnaireruns_view',
                                           qname=qname[0],
                                           timepoint=timepoint))
        html += "</table>"
        html += "</div>"
        html += '</div>'

        self.w(u'{0}'.format(html))


def registration_callback(vreg):
    """ Update  primary views
    """
    vreg.register(QuestionnairesView)
    vreg.register(QuestionnaireRunsView)
    vreg.register(get_db_data)
    vreg.register(csv_download)