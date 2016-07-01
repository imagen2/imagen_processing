# -*- coding: utf-8 -*-
#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
from cgi import parse_qs

# CW import
from cubicweb.view import View


class DashboardView(View):
    """ View to display subject, time point dashboard under user or centre
    """

    __regid__ = "dashboard-view"
    title = _("Dashboard")

    def call(self, **kwargs):
        # get parameters
        path = self._cw.relative_path()
        if "?" in path:
            path, param = path.split("?", 1)
            kwargs.update(parse_qs(param))
            print kwargs
        # query data
        rql = "Any UP ORDERBY UP DESC WHERE UP is CWUpload,"
        if 'user' in kwargs.keys():
                rql += " UP created_by U, U login '{}'".format(
                    kwargs['user'][0])
        else:
            rql += (" UP upload_fields F, F name 'centre',"
                    " F value = '{}'".format(kwargs['centre'][0]))
        rset = self._cw.execute(rql)

        # compute data
        data = {}
        forms = []
        tps = []
        for entity in rset.entities():
            form = entity.form_name
            forms.append(form)
            sid = entity.get_field_value('sid')
            tp = entity.get_field_value('time_point')
            tps.append(tp)
            status = entity.status
            centre = entity.get_field_value('centre')
            if not sid in data.keys():
                data[sid] = {}
            if not tp in data[sid].keys():
                data[sid][tp] = {}
            if not form in data[sid][tp].keys():
                data[sid][tp][form] = []
            data[sid][tp][form].append(
                (status, centre, entity.dc_creator(), entity.eid))

        forms = list(set(forms))
        forms.sort()
        tps = list(set(tps))
        tps.sort()

        # write title
        self.w(u'<div class="panel-heading">')
        self.w(u'<h1>{}</h1>'.format(kwargs['title'][0]))
        self.w(u'</div>')

        # write dashboard

        self.w(u'<div class="panel-body">')
        self.w(u'<table>')
        self.w(u'<theader><tr>')
        self.w(u"<th rowspan='2'>Subject ID</th>")
        for tp in tps:
            self.w(u"<th colspan='{}'>{}</th>".format(len(forms), tp))
        self.w(u'</tr><tr>')
        for tp in tps:
            for form in forms:
                self.w(u'<th>{}</th>'.format(form))
        self.w(u'</tr></theader>')
        self.w(u'<tbody>')
        for sid in data.keys():
            self.w(u'<tr>')
            self.w(u'<td>{}</td>'.format(sid))
            for tp in tps:
                for form in forms:
                    if tp in data[sid].keys():
                        if form in data[sid][tp].keys():
                            status, centre, user, eid = data[sid][tp][form][0]
                            color = ''
                            if status == 'Quarantine':
                                    color = '#336699'
                            elif status == 'Rejected':
                                color = '#800000'
                            elif status == 'Validated':
                                color = '#008080'
                            else:
                                color = '#FFFFFF'
                            self.w(u"<td style='background-color:{}'>".format(
                                color))

                            for nuple in data[sid][tp][form]:
                                status, centre, user, eid = nuple
                                href = self._cw.build_url(
                                    "view",
                                    rql=("Any U WHERE U is CWUpload"
                                           ", U eid '{}'".format(eid))
                                )
                                icon = ''
                                if status == 'Quarantine':
                                    icon = 'glyphicon-cog'
                                elif status == 'Rejected':
                                    icon = 'glyphicon-remove'
                                elif status == 'Validated':
                                    icon = 'glyphicon-ok'
                                else:
                                    icon = 'glyphicon-question-sign'
                                self.w(
                                    (u"<a href='{}'>"
                                     " <span class='glyphicon {}'"
                                     " title='{} : {}' /><a/>").format(
                                        href, icon, centre, user)
                                )
                            self.w(u'</td>')
                        else:
                            self.w(u'<td/>')
                    else:
                        self.w(u'<td/>')
            self.w(u'</tr>')
        self.w(u'</tbody>')
        self.w(u'</table>')
        self.w(u'</div>')
