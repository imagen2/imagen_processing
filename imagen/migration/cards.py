#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

import os.path as osp

HERE = osp.abspath(osp.dirname(__file__))


###############################################################################
# CARDS AND IMAGES DEFINITIONS 
###############################################################################
HTMLS = {
    u"index": open(osp.join(HERE, "static_pages/index.html")).read().decode("utf8"),
    u"license": open(osp.join(HERE, "static_pages/license.html")).read().decode("utf8"),
    u"legal": open(osp.join(HERE, "static_pages/legal.html")).read().decode("utf8")
}


###############################################################################
# CREATE OR UPDATE FUNCTION 
###############################################################################
def create_or_update_static_cards(session):
    """ Create or update the cards for static pages
    """
    for _id, html in HTMLS.iteritems():
        rset = session.execute("Any X WHERE X is Card, X title '{0}'".format(_id))
        if rset:
            session.execute("SET X content '{0}' WHERE X is Card, X title "
                            "'{1}'".format(html, _id))
        else:
            session.create_entity("Card", content_format=u"text/html",
                                  title=_id, content=html)
