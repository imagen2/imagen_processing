from cubicweb.web.views.facets import FacetFilterMixIn

## Hide filter component while filtering

FacetFilterMixIn._generate_form = FacetFilterMixIn.generate_form

def generate_form(self, w, rset, divid, vid, vidargs=None, mainvar=None,
                  paginate=False, cssclass='', hiddens=None, **kwargs):

        FacetFilterMixIn._generate_form(self, w, rset, divid, vid, vidargs=None,
                                        mainvar=None, paginate=False,
                                        cssclass='', hiddens=None, **kwargs)

        html = "<script>"
        html += "function onFacetFiltering(event, divid /* ... */) {"
        html += "$('#facet_filterbox').hide();"
        html += "showFacetLoading(divid);"
        html += "}"
        html += ("function onFacetContentLoaded"
                 "(event, divid, rql, vid, extraparams) {")
        html += "$('#facetLoading').hide();"
        html += "$('#facet_filterbox').show();"
        html += "}"
        html += "</script>"

        w(u'{0}'.format(html))

FacetFilterMixIn.generate_form = generate_form