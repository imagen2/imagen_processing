#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

from cubicweb.web.views.urlrewrite import SimpleReqRewriter, rgx


class ImagenWebReqRewriter(SimpleReqRewriter):
    """ Associate a request that generate a view with a specific url.
    """
    rules = [
        (rgx('/license'),
         dict(rql=r'Any X WHERE X is Card, X title "license"')),
        (rgx('/legal'),
         dict(rql=r'Any X WHERE X is Card, X title "legal"')),
    ]
