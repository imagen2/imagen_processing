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
from collections import OrderedDict
from cubicweb.web.views import csvexport
from cubicweb.view import View
import json
import time

class CSVRsetView(csvexport.CSVMixIn, View):
    """dumps raw result set in CSV"""
    __regid__ = 'csvexport-jtable'
    title = _('csv export')

    def call(self):

        qname = self._cw.form['qname']
        timepoint = self._cw.form['timepoint']

        rql_questions_text = "DISTINCT Any QUT ORDERBY QUT WHERE Q is Questionnaire, " \
                     "QU r_questionnaire Q, QU text QUT, " \
                     "Q name '{0}'".format(qname)
        questions_text_rset = self._cw.execute(rql_questions_text)

        questions = []
        header = ["ID"]
        for question in questions_text_rset:
            questions.append(question[0])
        header += questions

        rql = "Any QR, C ORDERBY C WHERE QR is QuestionnaireRun, QR r_concerns S, " \
              "S code_in_study C, QR r_instance_of Q, Q name '{0}', " \
              "QR in_assessment A, A timepoint '{1}'".format(qname, timepoint)
        rset = self._cw.execute(rql)

        # Build the dict that will be dumped in the jtable
        records = []

        for row_nb in range(len(rset)):
            eid = rset[row_nb][0]
            cis = rset[row_nb][1]
            # Start filling the datatable dataset
            dstruct = [cis] + [''] * len(questions_text_rset)


            rql = "Any QN, V Where QR eid '{0}', A is OpenAnswer, " \
                  "A r_questionnaire_run QR, A r_question Q, Q text QN, " \
                  "A value V".format(eid)
            answer_rset = self._cw.execute(rql)

            for qname, answer in answer_rset:

            # Go through all answers
                index = questions.index(qname)
                dstruct[index+1] = answer

            # Store the jtabel formated row
            records.append(dstruct)

        buff = []
        buff.append(header)
        for record in records:
            buff.append(record)

        writer = self.csvwriter()

        for subject_data in buff:
            writer.writerow(subject_data)


@ajaxfunc(output_type='json')
def csv_download(self, qname, timepoint):

    url = self._cw.build_url(vid='csvexport-jtable', qname = qname, timepoint =  timepoint)

    link = {"dl_url": url}

    return link


@ajaxfunc(output_type='json')
def get_db_data(self):
    """
    sEcho: Internal variable.
    iColumns: Number of columns being displayed.
    sColumns: List of column names.
    iDisplayStart: Where to paginate from.
    iDisplayLength: Number of rows that are visible.
    sSearch: String to search globally for.
    bEscapeRegex: Whether search is a regular expression.
    sSearch_(int) : Column-specific search (one each for each column).
    bEscapeRegex_(int) : Whether or not the column-specific searches are regular expression objects.
    iSortingCols: Number of columns to sort by.
    iSortDir: Direction to sort in.
    """

    iDisplayStart = int(self._cw.form['iDisplayStart'])
    iDisplayLength = int(self._cw.form['iDisplayLength'])
    sSearch = self._cw.form['sSearch']
    qname = self._cw.form['qname']
    timepoint = self._cw.form['timepoint']
    sSortDir_0 = self._cw.form['sSortDir_0']
    nb_subjects = int(self._cw.form['nb_subjects'])
    questions = json.loads(self._cw.form['questions'])

    rql = "Any QR, C ORDERBY C {0} WHERE QR is QuestionnaireRun, QR r_concerns S, " \
          "S code_in_study C, S code_in_study ILIKE '%{1}%', QR r_instance_of Q, Q name '{2}', " \
          "QR in_assessment A, A timepoint '{3}'".format(sSortDir_0, sSearch, qname, timepoint)
    rset = self._cw.execute(rql)

    # Build the dict that will be dumped in the datatable
    records = []
    if (iDisplayLength > len(rset)) or (iDisplayLength == -1):
        result_range = range(len(rset))
    else:
        result_range = range(iDisplayStart, min((iDisplayStart + iDisplayLength),len(rset)))

    for row_nb in result_range:
        eid = rset[row_nb][0]
        cis = rset[row_nb][1]
        # Start filling the datatable dataset
        dstruct = [cis] + [''] * len(questions)


        rql = "Any QN, V Where QR eid '{0}', A is OpenAnswer, " \
              "A r_questionnaire_run QR, A r_question Q, Q text QN, " \
              "A value V".format(eid)
        answer_rset = self._cw.execute(rql)

        for qname, answer in answer_rset:
            index = questions.index(qname)
            dstruct[index+1] = answer

        # Store the jtabel formated row
        records.append(dstruct)

    return {
  "iTotalRecords":nb_subjects,
  "iTotalDisplayRecords":len(rset),
  "aaData":records
}


class QuestionnaireRunsView(EntityStartupView):
    __regid__ = 'questionnaireruns_view'
    title = "QuestionnaireRun"

    def call(self, **kwargs):

        qname = self._cw.form['qname']
        timepoint = self._cw.form['timepoint']

        rql_nb_subjects = "DISTINCT Any COUNT(SID) WHERE QR is QuestionnaireRun, " \
                          "QR r_concerns S, S code_in_study SID, " \
                          "QR r_instance_of Q, Q name '{0}', QR in_assessment A," \
                          " A timepoint '{1}'".format(qname, timepoint)
        nb_subjects = self._cw.execute(rql_nb_subjects)[0][0]

        rql_questions_text = "DISTINCT Any QUT ORDERBY QUT WHERE Q is Questionnaire, " \
                             "QU r_questionnaire Q, QU text QUT, " \
                             "Q name '{0}'".format(qname)
        questions_text_rset = self._cw.execute(rql_questions_text)

        questions = []
        for question in questions_text_rset:
            questions.append(question[0])

        aoColumns = [{ "sTitle": "Subject ID" }]
        for question_text in questions:
            aoColumns += [{ "sTitle": question_text }]

        self._cw.add_css('jquery.dataTables.min.css')

        html = "<html>"
        html += "<head>"
        html += "<link rel=\"stylesheet\" type=\"text/css\" href=\"http://www.datatables.net/release-datatables/extensions/TableTools/css/dataTables.tableTools.css\">"
        html += "<link rel=\"stylesheet\" type=\"text/css\" href=\"http://datatables.net/release-datatables/extensions/FixedColumns/css/dataTables.fixedColumns.css\">"
        html += "<script type=\"text/javascript\" charset=\"utf8\" src=\"http://code.jquery.com/jquery-1.11.2.min.js\"></script>"
        html += "<script type=\"text/javascript\" charset=\"utf8\" src=\"http://cdn.datatables.net/1.10.5/js/jquery.dataTables.min.js\"></script>"
        html += "<script type=\"text/javascript\" charset=\"utf8\" src=\"http://www.datatables.net/release-datatables/extensions/TableTools/js/dataTables.tableTools.js\"></script>"
        html += "<script type=\"text/javascript\" charset=\"utf8\" src=\"http://datatables.net/release-datatables/extensions/FixedColumns/js/dataTables.fixedColumns.js\"></script>"
        html += "<script type=\"text/javascript\" charset=\"utf8\" src=\"http://cdn.datatables.net/plug-ins/f2c75b7247b/api/fnSetFilteringDelay.js\"></script>"
        html += "<style>"
        html += "th, td { white-space: nowrap; }"
        html += "div.dataTables_wrapper {"
        html += "width: 800px;"
        html += "margin: 0 auto;"
        html += "}"
        html += "</style>"
        html += "</head>"
        html += "<script>"
        html += "$(document).ready(function() {"
        html += "var table = $('#the_table').dataTable( {"
        html += "\"aoColumnDefs\": ["
        html += "{{ 'bSortable': false, 'aTargets': {0} }}".format(str(range(len(aoColumns))[1:]))
        html += "],"
        html += "\"lengthMenu\": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, \"All\"] ],"
        html += "\"scrollX\": true,"
        html += "\"scrollY\": \"600px\","
        html += "\"scrollCollapse\": true,"
        html += "\"dom\": 'T<\"clear\">lfrtip',"
        html += "\"tableTools\": {"
        html += "\"sRowSelect\": \"multi\","
        html += "\"sSwfPath\": \"http://cdn.datatables.net/tabletools/2.2.2/swf/copy_csv_xls_pdf.swf\","
        html += "\"aButtons\": [ \"copy\", \"print\", \"csv\", {"
        html += "\"sExtends\": \"ajax\", \"sButtonText\": \"CSV - All results\",\"fnAjaxComplete\": function ( XMLHttpRequest, textStatus ) {"
        html += "window.location = XMLHttpRequest.dl_url;"
        html += "},"
        html += "\"sAjaxUrl\": 'ajax?fname=csv_download&arg=' + '\"{0}\"' + '&arg=' + '\"{1}\"'".format(qname, timepoint)
        html += "} ]"
        html += "},"
        html += "\"sServerMethod\": \"POST\","
        html += "\"oLanguage\": {"
        html += "\"sSearch\": \"Subject ID search\""
        html += "},"
        html += "\"pagingType\": \"full_numbers\","
        html += "\"aoColumns\": {0},".format(json.dumps(aoColumns))
        html += "'bProcessing':true,"
        html += "'bServerSide':true,"
        html += "'sAjaxSource':'ajax?fname=get_db_data',"
        html += "\"fnServerParams\": function (aoData) {"
        html += "aoData.push({"
        html += "name: \"qname\","
        html += "value: \"{0}\"".format(qname)
        html += "}, {"
        html += "name: \"timepoint\","
        html += "value: \"{0}\"".format(timepoint)
        html += "}, {"
        html += "name: \"nb_questions\","
        html += "value: \"{0}\"".format(len(questions))
        html += "},{"
        html += "name: \"nb_subjects\","
        html += "value: \"{0}\"".format(nb_subjects)
        html += "}, {"
        html += "name: \"questions\","
        html += "value: '{0}'".format(json.dumps(questions))
        html += "});"
        html += "},"
        html += "} );"
        html += "new $.fn.dataTable.FixedColumns( table );"
        html += "table.fnSetFilteringDelay(2000);"
        html += "} );"
        html += "</script>"
        html += "</head>"
        html += "<body>"
        html += "<div style=\"width:500px\">"
        html += "<table id=\"the_table\">"
        html += "<thead></thead>"
        html += "<tbody>"
        html += "</tbody>"
        html += "</table>"
        html += "</div>"
        html += "</body>"
        html += "</html>"

        # Creat the corrsponding html page
        self.w(unicode(html))


class QuestionnairesView(EntityStartupView):
    __regid__ = 'questionnaires_view'
    title = "Questionnaire"

    def call(self, **kwargs):

        rql = "DISTINCT Any QN ORDERBY QN ASC WHERE Q is Questionnaire, Q name QN"
        qname_rset = self._cw.execute(rql)

        rql = "DISTINCT Any TP ORDERBY TP ASC WHERE A is Assessment, A timepoint TP"
        timepoints_rset =self._cw.execute(rql)

        headers = ["Questionnaire"]
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
        for qname in qname_rset:
            html += ('<tr><td style="width:{1}px"><strong>{0}</strong></a>'
                     '</td>'.format(qname[0], cell_size))
            for timepoint in timepoints_rset:
                html += '<td style="width:{1}px"><a href="{2}">{0}</td>'.format(
                        timepoint[0], cell_size,
                        self._cw.build_url(vid='questionnaireruns_view',
                                           qname=qname[0],
                                           timepoint=timepoint[0]))
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
    vreg.register(CSVRsetView)