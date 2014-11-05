#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


from cubicweb.web.views.baseviews import NullView


class WelcomePage(NullView):
    __regid__ = 'welcome'

    def call(self, **kwargs):

        # Write principal title
        self.w(u'<br>')
        self.w(u'<center>')
        self.w(u'<h1>')
        self.w(u'Imagen datasets - Image assessments figures')
        self.w(u'</h1>')
        self.w(u'</center>')

        try:
            self.w(u'<br>')

            # Get information file
            date, dic = get_figures("/volatile/test.txt")
            self.w(u'<h2>{0}</h2>'.format(date))

            # Create table header
            self.w(u'<table class="table table-striped">')
            self.w(u'<tr><th><center>Centre</center></th>'
                   '<th><center>Baseline subjects</center></th>'
                   '<th><center>Follow-Up 2 Subjects</center<</th></tr>')
            for entry in dic:
                # Fill the table
                self.w(u'<tr><td><center>{0}</center>'
                       '</td><td><center>{1}</center>'
                       '</td><td><center>{2}</center></td></tr>'.format(
                    entry,
                    dic[entry][0],
                    dic[entry][1]))
            self.w(u'</table>')
            self.w(u'<br>')
        except:
            self.w(u'Sorry, no figures available ...')
            pass


# public method (can be used somewhere else)
def get_figures(path):
    """ Parse file and return dictionary:
        {center:[BL_figure, FU2_figure]}
    """
    _buffer = open(path)
    # get last line (most recent one)
    line = _buffer.readlines()[-1]
    out = {}
    [date, info] = line.split(" ")
    for center_stat in info.split(".")[:-1]:
        out[center_stat.split(":")[0]] = center_stat.split(":")[1].split(",")
    return date, out


# Factory
def registration_callback(vreg):
    vreg.register(WelcomePage)
