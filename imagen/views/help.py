#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# CW import
from cubicweb.web.views.baseviews import NullView


class HelpPage(NullView):
    __regid__ = "help"

    def call(self, **kwargs):

        content = u"""
            <div class="container">
                <div class="span7">
                  <p>This website and data served are still in beta (V0.2).</p>
                  <p>Comments are welcome (<a href="mailto:imagendatabase@cea.fr">imagendatabase@cea.fr</a>).</p>
                  <p>The core of our system is based on the <a href="http://www.cubicweb.org/">CubicWeb</a> framework chosen because it brings:
                  <ul>
	                <li>&bull; tools to hold together complex/heterogeneous data,</li>
                    <li>&bull; a versatile engine driven by the data model,</li>
                    <li>&bull; a semantic query language <a href="http://docs.cubicweb.org/annexes/rql/language">RQL</a> (equivalent to but simpler than W3C's <a href="http://www.w3.org/standards/techs/sparql#w3c_all">SPARQL</a>)</li>
                    <li>&bull; a common mechanism for visualising/exporting data</li>
                  </ul>
                  </p>
                </div>
                <!-- Image -->
                <div class="span7">
                  <p>Feel free to play with it!</p>
                </div>
            </div>

            <div class="panel panel-info">
            <div class="panel-heading">
            <div class="panel-title" data-toggle="collapse" data-target="#about_data">
            <button type="button" class="btn btn-link">
            <h4><strong>About the Data</strong></h4></button>
            <span class="caret"></span>
            </div>
            </div>

            <div class="panel-body">
            <div id="about_data" class="collapse">
            <div class="container">
                <div class="span7">
                  <p>The current site and the data it serves are still in beta version 0.2.
                  It comprises raw images for BL and FU2.
                  BL raw images are the ones currently available from the Imagen XNAT serveur.
                  FU2 raw images are the ones that were successfully sent to NeuroSpin during the second
                  follow-up; more FU2 raw images are to come soon as they will be available.</p>

                  <p>In version 0.1, all known subjects in the study (enrollment of subjects only occurs
                  during BL) are indexed, but no DICOM images, questionnaires or scores are available.
                  Questionnaires and scores will be released in upcoming versions.</p>

                  <p>In version 0.2, genetics have been added. Questionnaires and scores will
                  be released in upcoming versions.</p>

                  <p>This beta version exhibits some capabilities of the final renovated version.
                  In particular :
                    <ul>
                        <li>&bull; navigation according to natural pivotal concepts (subjects, exams),</li>
                        <li>&bull; faceting functions that enables to refine intuitively the current request,</li>
                        <li>&bull; statistics functions in the context of the view,</li>
                        <li>&bull; access to the <strong>data download</strong> mechanisms,</li>
                        <li>&bull; access rights are operating and enforced.</li>
                    </ul>
                  </p>

                  <p><strong>Please use Chrome or Firefox to browse Imagen&nbsp;V2 server
                  and SFTP clients such as WinSCP or FileZilla to retrieve requested data.</strong></p>
                </div>
            </div>
            </div>
            </div>
            </div>



            <div class="panel panel-info">
            <div class="panel-heading">
            <div class="panel-title" data-toggle="collapse" data-target="#download">
            <button type="button" class="btn btn-link">
            <h4><strong>Download the data</strong></h4></button>
            <span class="caret"></span>
            </div>
            </div>

            <div class="panel-body">
            <div id="download" class="collapse">
            <div class="container">
                  <p>This is one of the most innovative contributions in the version
                  of the server. The download request is processed so that it results
                  in an easy-to-fetch item on an SFTP file server. Common acces-rights
                  are used for this SFTP server and the Imagen&nbsp;V2 server.</p>
                    <p><strong>"I want to retrieve all ADNI_MPRAGE data from the project"</strong></p>
                    <p>Use your browser to connect the Imagen&nbsp;V2 server:</p>
                    <ul>
                        <li>&bull; push the Scans button,</li>
                        <li>&bull; use faceting to select ADNI_MPRAGE (refine with the
                        time tag if you wish with BL or FU2),</li>
                        <li>&bull; push the "Save search" button,</li>
                        <li>&bull; you will be directed towards a rather technical
                        page (we will refine it later). Just enter the name of your
                        request in the name box and leave the remaing alone.
                        Press validate. That's it!</li>
                        <li>&bull; the server processed your download request and
                        return to the page your were previously navigating,</li>
                    </ul>
                    <br>
                    <p><strong>Use your FileZilla client to connect the SFTP server.<br>
                    <div class="panel-body">
                        Configuration: </p></strong>
                        <dl class="dl-horizontal">
                            <dt>host</dt><dd>imagen2.cea.fr</dd>
                            <dt>protocol</dt><dd>SFTP - SSH File Transfer Protocol</dd>
                            <dt>authentication</dt><dd>regular</dd>
                            <dt>id/pwd</dt><dd>the same id and passwd you use for the
                            Imagen&nbsp;V2 server</dd><br>
                        </dl>
                        <div id="images-box">
                            <div class="holder">
                                <div id="image-1" class="image-lightbox">
                                    <span class="close"><a href="#">X</a></span>
                                    <img src="{0}" alt="Configure FileZilla">
                                    <a class="expand" href="#image-1"></a>
                                </div>
                            </div>
                            <div class="holder">
                                <div id="image-2" class="image-lightbox">
                                    <span class="close"><a href="#">X</a></span>
                                    <img src="{1}" alt="Navigate with FileZilla">
                                    <a class="expand" href="#image-2"></a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <br>
                        <center><strong>then push "connect"</strong></center>
                    <br>
                    <br>
                    <p>You are connected to your user specific area where your request
                    are stored for <strong>two weeks</strong>.<br> You can navigate and select whole or
                    part of the available data following the path "/home/user/rql_download/imagen".
                    You should find one entry for each request in this directory.
                    Each request/entry contains a file named RESULT_REQUEST.json or
                    RESULT_REQUEST.csv and the data itself.</p>
                    <p>Then as usual for an sftp site, select the local directory
                    where you will receive the data and start the transfer. If you
                    made a very general request, you may be rapidly flooded with data.</p>
                    <p>In the current version, the structure of the received data may seem a bit messy.
                    This should be fixed in future version.</p>
            </div>
            </div>
            </div>
            </div>


            <div class="panel panel-info">
            <div class="panel-heading">
            <div class="panel-title" data-toggle="collapse" data-target="#play">
            <button type="button" class="btn btn-link">
            <h4><strong>Play with the RQL request language</strong></h4></button>
            <span class="caret"></span>
            </div>
            </div>

            <div class="panel-body">
            <div id="play" class="collapse">
            <div class="container">
                <div class="span7">
                  <p>One of the reasons we choose CubicWeb is its semantic query
                  language. The following examples may appear frustrating, because
                  they require to understand some syntax (see <a href="http://docs.cubicweb.org/annexes/rql/language">RQL language</a>)
                  and the model of the data. Nevertheless, you should be able to feel
                  its interest through the following.
                  </p>
                  <p>Find the research box in the bar at the top of the page,
                  cut and paste the query examples thereafter (the part in the blue frames)
                  </p>
                </div>

                <!-- About subjects -->
                <div class="span7">
                  <p><strong>"All the subjects of the database"</strong></p>
                    <div class="panel panel-info">
                    <div class="panel-heading">
                    <p>Any S WHERE S is Subject</p>
                    </div>
                    </div>
                    <p>You may now press the "Save Search" button and save this specific download request.</p>
                </div>

                <!-- About handedness -->
                <div class="span7">
                  <p><strong>"All the subjects of the database with right or left-handedness"</strong></p>
                    <div class="panel panel-info">
                    <div class="panel-heading">
                    <p>Any S WHERE S is Subject, S handedness IN ("right", "left")</p>
                    </div>
                    </div>
                    <p>You may now press the "Save Search" button and save this specific download request.</p>
                </div>

                <!-- About acquisition centre and data type-->
                <div class="span7">
                  <p><strong>"All DTI scans from Nottingham"</strong></p>
                    <div class="panel panel-info">
                    <div class="panel-heading">
                    <p>Any S, P, C WHERE P is Subject, S is Scan, A is Assessment, P concerned_by A, C holds A, C name 'NOTTINGHAM', A uses S, S type 'DTI'</p>
                    </div>
                    </div>
                    <p>You may now press the "Save Search" button and save this specific download request.</p>
                </div>
            </div>
            </div>
            </div>
            </div>


            <div class="panel panel-info">
            <div class="panel-heading">
            <div class="panel-title" data-toggle="collapse" data-target="#roadmap">
            <button type="button" class="btn btn-link">
            <h4><strong>See the roadmap</strong></h4></button>
            <span class="caret"></span>
            </div>
            </div>

            <div class="panel-body">
            <div id="roadmap" class="collapse">
            <div class="container">
                <div class="span7">
                <p>Provisional roadmap:
                    <ul>
                        <li>&bull; 0.1: initial version</li>
                        <li>&bull; 0.2: introduction of new raw data with restricted
                        access policies (genetics, imputed genetics,
                        gene-expresssion, methylation). Helpers to customize the download mechanisms,</li>
                        <li>&bull; 0.3: questionnaires and score,</li>
                        <li>&bull; 0.4: (to be defined),</li>
                    </ul>
                  </p>
                </div>
            </div>
            </div>
            </div>
            </div>
""".format(self._cw.data_url("images/SetupFZ.png"),
           self._cw.data_url("images/NavFZ.png"))
        self.w(content)


def registration_callback(vreg):
    vreg.register(HelpPage)
