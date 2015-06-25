from cubicweb.web.views.facets import FacetFilterMixIn


# Use of a cusom JS to freeze filters when one is being processed
FacetFilterMixIn.needs_js = ['cubicweb.ajax.js', 'imagen.cubicweb.facets.js']