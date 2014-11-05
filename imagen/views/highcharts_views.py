#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

from cubicweb.view import View
import numpy


###############################################################################
# Pie Charts
###############################################################################

class HighChartsBasicPieView(View):
    """ Create a basic pie chart using highcharts.
    """
    __regid__ = "highcharts-basic-pie"
    paginable = False
    div_id = "highcharts-basic-pie"

    def rset_to_data(self, rset):
        """ Method that format the rset parameters for highcharts pie chart.

        We only consider the first element of each resultset row to construct the 
        highcharts formated parameter.

        Parameters
        ----------
        rset: resultset (mandatory)
            a  cw resultset

        Returns
        -------
        sdata: string
            the highcharts formated parameter
        """
        # Get the first element of each resultset row
        data = {}
        nb_of_elements = 0.
        for element in rset.rows:
            title = element[0]
            if title not in data:
                data[title] = 1.
            else:
                data[title] += 1.
            nb_of_elements += 1.

        # Transform/convert (expect percents) the data       
        data = [[key, value / nb_of_elements * 100.]
                 for key, value in data.iteritems()]

        # Create the highcharts string representation of the data
        sdata = '['
        for key, value in data:
            sdata += '["{0}", {1}], '.format(key, value)
        sdata += ']'

        return sdata
        
    def call(self, rset=None, title="", **kwargs):
        """ Method that will create a basic pie chart from a cw resultset.

        If no resultset are passed to this method, the current resultset is
        used.

        Parameters
        ----------
        rset: resultset (optional, default None)
            a  cw resultset
        title: string (optional, default None)
            the name of the chart.
        """
        # Get the cw resultset
        rset = rset or self.cw_rset

        # Get the title
        title = title or self._cw.form.get("title", "")

        # Get the highcharts string representation of the data
        data = self.rset_to_data(rset)

        # Add some js resources
        self._cw.add_js(
            ("highcharts-4.0.4/js/highcharts.js", 
             "highcharts-4.0.4/js/modules/exporting.js")
        )

        # Generate the script
        # > headers
        self.w(u'<script type="text/javascript">' )
        self.w(u'$(function () { $("#hc_container").highcharts({')
        # > configure credit
        self.w(u'credits : {enabled : false}, ')
        # > configure chart
        self.w(u'chart: {plotBackgroundColor: null, plotBorderWidth: 1, '
               'plotShadow: false}, ' )
        # > configure title
        self.w(u'title: {{text: "{0}"}}, '.format(title))
        # > configure tooltip
        self.w(u'tooltip: {pointFormat: "{series.name}: '
               '<b>{point.percentage:.1f}%</b>" }, ')
        # > configure plot
        self.w(u'plotOptions: {' )
        self.w(u'pie: {allowPointSelect: true, cursor: "pointer", dataLabels: {'
               'enabled: true, format: "<b>{point.name}</b>: '
               '{point.percentage:.1f} %", style: {color: (Highcharts.theme && '
               'Highcharts.theme.contrastTextColor) || "black"}}}' )
        self.w(u'}, ')
        # > configure series
        self.w(u'series: [{{type: "pie", name: "Browser share", data: {0}}}] '.format(data))
        # > close headers
        self.w(u'}); ')
        self.w(u'}); ')
        self.w(u'</script>' )

        # Add a container in the body to display the pie chart
        self.w(u'<div id="hc_container" style="min-width: 310px; height: 400px; '
                'max-width: 600px; margin: 0 auto"></div>')


###############################################################################
# Tables
###############################################################################

class HighChartsRelationSummaryView(View):
    """ Create a basic table view that summarized an entity relation.
    """
    __regid__ = "highcharts-relation-summary-view"
    paginable = False
    div_id = "highcharts-relation-summary-view"  

    def rset_to_data(self, rset, relation, subject_attr, object_attr):
        """ Method that format the rset parameters for highcharts table view.

        We only consider the first entity of each resultset row to construct the 
        highcharts formated parameters.
        The object entities are related to the subject entities with the
        'relation' link.
        The columns corresspond to the subject entity 'subject_attr' attributes.
        The lines corresspond to the object entity 'object_attr' attributes.

        Parameters
        ----------
        rset: resultset (mandatory)
            a  cw resultset
        relation: str (mandatory)
            the relation to follow.
        subject_attr: str (mandatory)
            the subject attribute.
        object_attr: str (mandatory)
            the object attribute.

        Returns
        -------
        fdata: dict
            the highcharts formated parameters: 'x' contains the x labels,
            'y' contains the y labels and 'grid' the table values and positions.
        """
        # Get the first element of each resultset row
        data = {}
        for line_number in range(len(rset.rows)):

            # Get the subject/object entities
            subject_entity = rset.get_entity(line_number, 0)
            object_entities = eval("subject_entity.{0}".format(relation))

            # Get the subject/object attributes
            col_name = eval("subject_entity.{0}".format(subject_attr))
            line_names = [eval("entity.{0}".format(object_attr))
                          for entity in object_entities]

            # Organize the data
            if not col_name in data:
                data[col_name] = {}
            for line_name in line_names:
                if not line_name in data[col_name]:
                    data[col_name][line_name] = 1
                else:
                    data[col_name][line_name] += 1

        # Create the highcharts string representation of the data
        sdata = {
            "x": [],
            "y": [],
            "grid": []
        }
        # > find all unique y labels
        all_y_labels = []
        for x_label, item in data.iteritems():
            all_y_labels.extend(item.keys())
        all_y_labels = set(all_y_labels)
        # > create the x,y-labels and corresponding table item
        x_count = 0
        for x_label, item in data.iteritems():
            sdata["x"].append(x_label)
            y_count = 0
            for y_label in all_y_labels:
                if y_label in item:
                    nb_of_elements = item[y_label]
                else:
                    nb_of_elements = 0
                sdata["grid"].append("[{0}, {1}, {2}]".format(
                    x_count, y_count, nb_of_elements))
                y_count += 1
            x_count += 1
        # > format the data outputs
        sdata["x"] = "['" + "', '".join(sdata["x"]) + "']"
        sdata["y"] = "['" + "', '".join(all_y_labels) + "']"
        sdata["grid"] = "[" + ", ".join(sdata["grid"]) + "]"

        return sdata
        
    def call(self, relation=None, subject_attr=None, object_attr=None, 
             rset=None, title="", **kwargs):
        """ Method that will create a table view from a cw resultset.

        If no resultset are passed to this method, the current resultset is
        used.

        Parameters
        ----------
        relation: str (optional, default None)
            the relation to follow.
        subject_attr: str (optional, default None)
            the subject attribute that will be used to create the table columns.
        object_attr: str (optional, default None)
            the object attribute that will be used to create the table lines.
        rset: resultset (optional, default None)
            a  cw resultset
        title: string (optional, default None)
            the name of the chart.
        """
        # Get the cw resultset
        rset = rset or self.cw_rset

        # Get the method parameters: if we use 'build_url' method, the data
        # are in the firm dictionary
        title = title or self._cw.form.get("title", "")
        relation = relation or self._cw.form.get("relation", None)
        subject_attr = subject_attr or self._cw.form.get("subject_attr", None)
        object_attr = object_attr or self._cw.form.get("object_attr", None)

        # Check that we have all the required information
        if relation is None or subject_attr is None or object_attr is None:
            self.w(u'<a>Wrong input arguments in HighChartsRelationSummaryView '
                    'class.</a>')
            return

        # Get the highcharts string representation of the data
        data = self.rset_to_data(rset, relation, subject_attr, object_attr)

        # Add some js resources
        self._cw.add_js(
            ("highcharts-4.0.4/js/highcharts.js", 
             "highcharts-4.0.4/js/modules/heatmap.js",
             "highcharts-4.0.4/js/modules/exporting.js")
        )

        # Generate the script
        # > headers
        self.w(u'<script type="text/javascript">' )
        self.w(u'$(function () { $("#hc_container").highcharts({')
        # > configure credit
        self.w(u'credits : {enabled : false}, ')
        # > configure chart
        self.w(u'chart: {type: "heatmap", marginTop: 40, marginBottom: 40}, ' )
        # > configure title
        self.w(u'title: {{text: "{0}"}}, '.format(title))
        # > configure axis
        self.w(u'xAxis: {{categories: {0}}}, '.format(data["x"]))
        self.w(u'yAxis: {{categories: {0}, title: null}}, '.format(data["y"]))
        self.w(u'colorAxis: {min: 0, minColor: "#FFFFFF", '
                'maxColor: Highcharts.getOptions().colors[0]}, ')
        self.w(u'legend: {align: "right", layout: "vertical", margin: 0, '
                'verticalAlign: "top", y: 25, symbolHeight: 320}, ')
        # > configure tooltip
        self.w(u'tooltip: {{formatter: function () {{return "<b>" + '
                'this.series.xAxis.categories[this.point.x] + '
                '"</b> {0} <br><b>" + this.point.value + '
                '"</b> items <br><b>" + this.series.yAxis.categories['
                'this.point.y] + "</b>";}}}}, '.format(relation))
        # > configure series
        self.w(u'series: [{{name: "Number of item per timepoint", borderWidth: 1, '
                'data: {0}, dataLabels: {{enabled: true, color: "black", style: '
                '{{textShadow: "none", HcTextStroke: null}}}}}}]'.format(data["grid"]))
        # > close headers
        self.w(u'}); ')
        self.w(u'}); ')
        self.w(u'</script>' )

        # Add a container in the body to display the pie chart. Try to estimate
        # the cell size
        width = 100 + len(data["x"]) * 20
        height = len(data["y"]) * 5
        self.w(u'<div style="max-height:700px; overflow: auto; '
                'max-width: 800px;"> ')
        self.w(u'<div id="hc_container" style="width: {0}px; '
                'height: {1}px; margin: 0 auto"></div>'.format(width, height))
        self.w(u'</div>')


###############################################################################
# Plot
###############################################################################

class HighChartsBasicPlotView(View):
    """ Create a basic plot using highcharts.
    """
    __regid__ = "highcharts-basic-plot"
    paginable = False
    div_id = "highcharts-basic-plot"

    def rset_to_hist(self, rset):
        """ Method that format the rset parameters for highcharts plot.

        We only consider the first element of each resultset row to construct the 
        highcharts formated parameter.

        Parameters
        ----------
        rset: resultset (mandatory)
            a  cw resultset

        Returns
        -------
        sdata: string
            the highcharts formated parameter
        """
        # Get the first element of each resultset row
        data = []
        for element in rset.rows:
            data.append(float(element[0]))

        # Create the histogram with numpy
        hist, bin_edges = numpy.histogram(data, density=True, bins=20)
        bin_center = ["%.1f" % ((bin_edges[i] + bin_edges[i+1]) / 2.)
                      for i in range(len(bin_edges) - 1)]
        hist = [str(value) for value in hist]

        # Create the highcharts string representation of the data
        sdata = {
            "x": "['" + "', '".join(bin_center) + "']",
            "grid": "[" + ", ".join(hist) + "]"
        }

        return sdata
        
    def call(self, rset=None, title="", value_suffix="", is_hist=False,
             y_label="", data=None, tag="hc_container", **kwargs):
        """ Method that will create a basic plot from a cw resultset.

        If no resultset are passed to this method, the current resultset is
        used.

        Parameters
        ----------
        rset: resultset (optional, default None)
            a  cw resultset
        title: string (optional, default None)
            the name of the chart.
        value_suffix: str (optional)
            the units of what we measure.
        is_hist: bool (optional, default False)
            consider the rset as an input of a simple plot or an histogram plot.
        y_label: str (optional)
            the label of the y axis.
        data: dict (optional, default None)
            the highcharts string representation of the data. If set, do not 
            generate the data from the rset, so the 'is_hist' option has no
            effect.
        tag: str (optional, default 'hc_container')
            the html div identifier.
        """
        # Get the cw resultset
        rset = rset or self.cw_rset

        # Get the method parameters: if we use 'build_url' method, the data
        # are in the firm dictionary
        title = title or self._cw.form.get("title", "")
        value_suffix = value_suffix or self._cw.form.get("value_suffix", "")
        is_hist = is_hist or self._cw.form.get("is_hist", False)
        data = data or self._cw.form.get("data", None)

        # Get the highcharts string representation of the data
        if data is None:
            if is_hist:
                value_suffix = "Probability"
                y_label = "Probability"
                data = self.rset_to_hist(rset)
            else:
                raise NotImplementedError
                #data = self.rset_to_data(rset)

        # Add some js resources
        self._cw.add_js(
            ("highcharts-4.0.4/js/highcharts.js", 
             "highcharts-4.0.4/js/modules/exporting.js")
        )

        # Generate the script
        # > headers
        self.w(u'<script type="text/javascript">' )
        self.w(u'$(function () {{ $("#{0}").highcharts({{'.format(tag))
        # > configure credit
        self.w(u'credits : {enabled : false}, ')
        # > configure title
        self.w(u'title: {{text: "{0}"}}, '.format(title))
        # > configure axis
        self.w(u'xAxis: {{categories: {0}}}, '.format(data["x"]))
        self.w(u'yAxis: {{title: {{text: "{0}"}}}}, '.format(y_label))
        # > configure tooltip
        self.w(u'tooltip: {{valueSuffix: " {0}"}}, '.format(value_suffix))
        # > configure legend
        self.w(u'legend: {layout: "vertical", align: "right", verticalAlign: '
                '"middle", borderWidth: 0}, ')
        # > configure series
        self.w(u'series: [{{name: "{0}", data: {1}}}] '.format(title, data["grid"]))
        # > close headers
        self.w(u'}); ')
        self.w(u'}); ')
        self.w(u'</script>' )

        # Add a container in the body to display the pie chart
        self.w(u'<div id="{0}" style="min-width: 310px; height: 400px; '
                'max-width: 600px; margin: 0 auto"></div>'.format(tag))
