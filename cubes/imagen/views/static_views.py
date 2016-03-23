# -*- coding: utf-8 -*-
# copyright 2014-2016 CEA, all rights reserved.
# contact http://i2bm.cea.fr/drf/i2bm/NeuroSpin -- mailto:imagendatabase@cea.fr
#
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.

from cubicweb.view import EntityStartupView
from cubicweb.web.views.baseviews import NullView


class QC_central(EntityStartupView):
    __regid__ = 'QC_central'
    title = "QC central"

    def call(self, **kwargs):

        self._cw.add_js("pdfobject.js")

        self.w(u'<div class="panel panel-warning">')
        self.w(u'<div class="panel-heading">')
        self.w(u'<h2 class="panel-title">WORK IN PROGRESS</h2>')
        self.w(u'</div>')
        self.w(u'<div class="panel-body">')
        self.w(u"This page will gather all information about all quality"
               "that will be performed on the data. For each of them, the "
               "following details will be given:")
        self.w(u"<ul>")
        self.w(u"<li> How are QC outcomes displayed in the database </li>")
        self.w(u"<li> What is the meaning of each score </li>")
        self.w(u"<li> Who performed the QCs </li>")
        self.w(u"<li> When was the QCs performed </li>")
        self.w(u"<li> The tools and algorithms used for QCs </li>")
        self.w(u"<li> ... </li>")
        self.w(u"</ul>")
        self.w(u'</div>')
        self.w(u'</div>')
        self.w(u'</script>')


class Doc_smri(EntityStartupView):
    __regid__ = "doc_MRIData"
    title = "sMRI documentation"

    def call(self, **kwargs):
        self.w(u"<h1><center><strong>structural MRI documentaion</strong>"
               "<center></h1>")
        self.w(u"<h2>  T1 ADNI MPRAGE </h2>")
        self.w(u"Sed fruatur sane hoc solacio atque hanc insignem ignominiam, "
               "quoniam uni praeter se inusta sit, putet esse leviorem, dum "
               "modo, cuius exemplo se consolatur, eius exitum expectet, "
               "praesertim cum in Albucio nec Pisonis libidines nec audacia "
               "Gabini fuerit ac tamen hac una plaga conciderit, ignominia "
               "senatus.")


class Doc_fmri(NullView):
    __regid__ = "doc_FMRIData"
    title = "fMRI documentation"
    templatable = False

    def call(self, **kwargs):

        page = u"""
        <!DOCTYPE html>
        <html xmlns:cubicweb="http://www.cubicweb.org" lang="en">
        <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=8" />
        """

        page += '<link rel="shortcut icon" href="{0}"/>'.format(
            self._cw.data_url("favicon.ico"))
        page += '<title>fMRI documentation (Imagen Database)</title>'
        page += '<script type="text/javascript" src="{0}"></script>'.format(
            self._cw.data_url("pdfobject.js"))
        page += "</head><body>"

        self.w(page)
        self.w(u"<p>It appears you don't have Adobe Reader or PDF support in "
               'this web browser. <a href="{0}">Click here to download '
               'the PDF</a></p>'.format(self._cw.data_url('EPI_doc.pdf')))
        self.w(u"</body>")
        self.w(u'<footer id="pagefooter" role="contentinfo">'
               '<a href="http://www.imagen-europe.com/">Imagen</a> | '
               '<a href="http://i2bm.cea.fr/drf/i2bm/NeuroSpin/">NeuroSpin</a>'
               '</footer>')
        self.w(u'</html>')

        # JAVASCRIPTS
        self.w(u'<script type="text/javascript">')

        self.w(u'var pdfOpen_params_popup = {'
               'navpanes: 1,'
               'page: 1'
               '};')

        self.w(u'var pdfAttributes_popup = {{'
               'url: "{0}",'
               'pdfOpenParams: pdfOpen_params_popup'
               '}};'.format(self._cw.data_url('EPI_doc.pdf')))

        self.w(u'window.onload = function (){')
        self.w(u'var doc_popup = new PDFObject(pdfAttributes_popup);'
               'doc_popup.embed();'
               '};')
        self.w(u'</script>')


def registration_callback(vreg):
    vreg.register(QC_central)
    vreg.register(Doc_smri)
    vreg.register(Doc_fmri)
