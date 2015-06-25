/** filter form, aka facets, javascript functions
 *
 *  :organization: Logilab
 *  :copyright: 2003-2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
 *  :contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
 */

var SELECTED_IMG = DATA_URL + 'black-check.png';
var UNSELECTED_IMG = DATA_URL + 'no-check-no-border.png';
var UNSELECTED_BORDER_IMG = DATA_URL + 'black-uncheck.png';

function copyParam(origparams, newparams, param) {
    var index = $.inArray(param, origparams[0]);
    if (index > - 1) {
        newparams[param] = origparams[1][index];
    }
}


function facetFormContent($form) {
    var names = [];
    var values = [];
    $form.find('.facet').each(function() {
        var facetName = $(this).find('.facetTitle').attr('cubicweb:facetName');
        // FacetVocabularyWidget
        $(this).find('.facetValueSelected').each(function(x) {
            names.push(facetName);
            values.push(this.getAttribute('cubicweb:value'));
        });
        // FacetStringWidget (e.g. has-text)
        $(this).find('input:text').each(function(){
            names.push(this.name);
            values.push(this.value);
        });
    });
    // pick up hidden inputs (required metadata inputs such as 'facets'
    // but also RangeWidgets)
    $form.find('input[type="hidden"]').each(function() {
        names.push(this.name);
        values.push(this.value);
    });
    // And / Or operators
    $form.find('select option[selected]').each(function() {
        names.push(this.parentNode.name);
        values.push(this.value);
    });
    return [names, values];
}


// XXX deprecate vidargs once TableView is gone
function buildRQL(divid, vid, paginate, vidargs) {
    $(CubicWeb).trigger('facets-content-loading', [divid, vid, paginate, vidargs]);
    var $form = $('#' + divid + 'Form');
    var zipped = facetFormContent($form);
    zipped[0].push('facetargs');
    zipped[1].push(vidargs);
    var d = loadRemote(AJAX_BASE_URL, ajaxFuncArgs('filter_build_rql', null, zipped[0], zipped[1]));
    d.addCallback(function(result) {
        var rql = result[0];
        var $bkLink = $('#facetBkLink');
        if ($bkLink.length) {
            var bkPath = 'view?rql=' + encodeURIComponent(rql);
            if (vid) {
                bkPath += '&vid=' + encodeURIComponent(vid);
            }
            var bkUrl = $bkLink.attr('cubicweb:target') + '&path=' + encodeURIComponent(bkPath);
            $bkLink.attr('href', bkUrl);
        }
        var $focusLink = $('#focusLink');
        if ($focusLink.length) {
            var url = baseuri()+ 'view?rql=' + encodeURIComponent(rql);
            if (vid) {
                url += '&vid=' + encodeURIComponent(vid);
            }
            $focusLink.attr('href', url);
        }
        var toupdate = result[1];
        var extraparams = vidargs;
        if (paginate) { extraparams['paginate'] = '1'; } // XXX in vidargs
        // copy some parameters
        // XXX cleanup vid/divid mess
        // if vid argument is specified , the one specified in form params will
        // be overriden by replacePageChunk
        copyParam(zipped, extraparams, 'vid');
        extraparams['divid'] = divid;
        copyParam(zipped, extraparams, 'divid');
        copyParam(zipped, extraparams, 'subvid'); // XXX deprecate once TableView is gone
        copyParam(zipped, extraparams, 'fromformfilter');
        // paginate used to know if the filter box is acting, in which case we
        // want to reload action box to match current selection (we don't want
        // this from a table filter)
        extraparams['rql'] = rql;
        if (vid) { // XXX see copyParam above. Need cleanup
            extraparams['vid'] = vid;
        }
        d = $('#' + divid).loadxhtml(AJAX_BASE_URL, ajaxFuncArgs('view', extraparams),
                                     null, 'swap');
        d.addCallback(function() {
            // XXX rql/vid in extraparams
            $(CubicWeb).trigger('facets-content-loaded', [divid, rql, vid, extraparams]);
        });
        if (paginate) {
            // FIXME the edit box might not be displayed in which case we don't
            // know where to put the potential new one, just skip this case for
            // now
            var $node = $('#edit_box');
            if ($node.length) {
                $node.loadxhtml(AJAX_BASE_URL, ajaxFuncArgs('render', {
                    'rql': rql
                },
                'ctxcomponents', 'edit_box'), 'GET', 'swap');
            }
            $node = $('#breadcrumbs');
            if ($node.length) {
                $node.loadxhtml(AJAX_BASE_URL, ajaxFuncArgs('render', {
                    'rql': rql
                },
                'ctxcomponents', 'breadcrumbs'));
            }
        }
        var mainvar = null;
        var index = $.inArray('mainvar', zipped[0]);
        if (index > - 1) {
            mainvar = zipped[1][index];
        }

        var d = loadRemote(AJAX_BASE_URL, ajaxFuncArgs('filter_select_content', null, toupdate, rql, mainvar));
        d.addCallback(function(updateMap) {
            for (facetName in updateMap) {
                var values = updateMap[facetName];
                // XXX fine with jquery 1.6
                //$form.find('div[cubicweb\\:facetName="' + facetName + '"] ~ div .facetCheckBox').each(function() {
                $form.find('div').filter(function () {return $(this).attr('cubicweb:facetName') == facetName}).parent().find('.facetCheckBox').each(function() {
                    var value = this.getAttribute('cubicweb:value');
                    if ($.inArray(value, values) == -1) {
                        if (!$(this).hasClass('facetValueDisabled')) {
                            $(this).addClass('facetValueDisabled');
                        }
                    } else {
                        if ($(this).hasClass('facetValueDisabled')) {
                            $(this).removeClass('facetValueDisabled');
                        }
                    }
                });
            }
        });
    });
}


function initFacetBoxEvents(root) {
    // facetargs : (divid, vid, paginate, extraargs)
    root = root || document;
    $(root).find('form').each(function() {
        var form = $(this);
        // NOTE: don't evaluate facetargs here but in callbacks since its value
        //       may changes and we must send its value when the callback is
        //       called, not when the page is initialized
        var facetargs = form.attr('cubicweb:facetargs');
        if (facetargs != undefined && !form.attr('cubicweb:initialized')) {
            form.attr('cubicweb:initialized', '1');
            var jsfacetargs = cw.evalJSON(form.attr('cubicweb:facetargs'));
            form.submit(function() {
                buildRQL.apply(null, jsfacetargs);
                return false;
            });
            var divid = jsfacetargs[0];
            if ($('#'+divid).length) {
                var $loadingDiv = $(DIV({id:'facetLoading'},
                                        facetLoadingMsg));
                $($('#'+divid).get(0).parentNode).append($loadingDiv);
            }
            form.find('div.facet').each(function() {
                var $facet = $(this);
                $facet.find('div.facetCheckBox').each(function(i) {
                    this.setAttribute('cubicweb:idx', i);
                });
                $facet.find('div.facetCheckBox').click(function() {
                    var $this = $(this);
                    // NOTE : add test on the facet operator (i.e. OR, AND)
                    // if ($this.hasClass('facetValueDisabled')){
                    //          return
                    // }
                    if ($this.hasClass('facetValueSelected')) {
                        facetCheckBoxUnselect($this);
                    } else {
                        facetCheckBoxSelect($this);
                    }
                    facetCheckBoxReorder($facet);
                    buildRQL.apply(null, jsfacetargs);
                });
                $facet.find('select.facetOperator').change(function() {
                    var nbselected = $facet.find('div.facetValueSelected').length;
                    if (nbselected >= 2) {
                        buildRQL.apply(null, jsfacetargs);
                    }
                });
                $facet.find('div.facetTitle.hideFacetBody').click(function() {
                    $facet.find('div.facetBody').toggleClass('hidden').toggleClass('opened');
                    $(this).toggleClass('opened');

                });

            });
        }
    });
}

// facetCheckBoxSelect: select the given facet checkbox item (.facetValue
// class)
function facetCheckBoxSelect($item) {
    $item.addClass('facetValueSelected');
    $item.find('img').attr('src', SELECTED_IMG).attr('alt', (_("selected")));
}

// facetCheckBoxUnselect: unselect the given facet checkbox item (.facetValue
// class)
function facetCheckBoxUnselect($item) {
    $item.removeClass('facetValueSelected');
    $item.find('img').each(function(i) {
        if (this.getAttribute('cubicweb:unselimg')) {
            this.setAttribute('src', UNSELECTED_BORDER_IMG);
        }
        else {
            this.setAttribute('src', UNSELECTED_IMG);
        }
        this.setAttribute('alt', (_("not selected")));
    });
}

// facetCheckBoxReorder: reorder all items according to cubicweb:idx attribute
function facetCheckBoxReorder($facet) {
    var sortfunc = function (a, b) {
        // convert from string to integer
        a = +a.getAttribute("cubicweb:idx");
        b = +b.getAttribute("cubicweb:idx");
        // compare
        if (a > b) {
            return 1;
        } else if (a < b) {
            return -1;
        } else {
            return 0;
        }
    };
    var $items = $facet.find('.facetValue.facetValueSelected')
    $items.sort(sortfunc);
    $facet.find('.facetBody').append($items);
    var $items = $facet.find('.facetValue:not(.facetValueSelected)')
    $items.sort(sortfunc);
    $facet.find('.facetBody').append($items);
    $facet.find('.facetBody').animate({scrollTop: 0}, '');
}

// trigger this function on document ready event if you provide some kind of
// persistent search (eg crih)
function reorderFacetsItems(root) {
    root = root || document;
    $(root).find('form').each(function() {
        var form = $(this);
        if (form.attr('cubicweb:facetargs')) {
            form.find('div.facet').each(function() {
                var facet = $(this);
                var lastSelected = null;
                facet.find('div.facetCheckBox').each(function(i) {
                    var $this = $(this);
                    if ($this.hasClass('facetValueSelected')) {
                        if (lastSelected) {
                            lastSelected.after(this);
                        } else {
                            var parent = this.parentNode;
                            $(parent).prepend(this);
                        }
                        lastSelected = $this;
                    }
                });
            });
        }
    });
}

// change css class of facets that have a value selected
function updateFacetTitles() {
    $('.facet').each(function() {
        var $divTitle = $(this).find('.facetTitle');
        var facetSelected = $(this).find('.facetValueSelected');
        if (facetSelected.length) {
            $divTitle.addClass('facetTitleSelected');
        } else {
            $divTitle.removeClass('facetTitleSelected');
        }
    });
}

// we need to differenciate cases where initFacetBoxEvents is called with one
// argument or without any argument. If we use `initFacetBoxEvents` as the
// direct callback on the jQuery.ready event, jQuery will pass some argument of
// his, so we use this small anonymous function instead.
$(document).ready(function() {
    initFacetBoxEvents();
    $(cw).bind('facets-content-loaded', onFacetContentLoaded);
    $(cw).bind('facets-content-loading', onFacetFiltering);
    $(cw).bind('facets-content-loading', updateFacetTitles);
});

function showFacetLoading(parentid) {
    var loadingWidth = 200; // px
    var loadingHeight = 100; // px
    var $msg = $('#facetLoading');
    var $parent = $('#' + parentid);
    var leftPos = $parent.offset().left + ($parent.width() - loadingWidth) / 2;
    $parent.fadeTo('normal', 0.2);
    $msg.css('left', leftPos).show();
}

function onFacetFiltering(event, divid /* ... */) {
    $('#facet_filterbox').hide();
    showFacetLoading(divid);
}

function onFacetContentLoaded(event, divid, rql, vid, extraparams) {
    $('#facetLoading').hide();
    $('#facet_filterbox').show();
}

$(document).ready(function () {
    if ($('div.facetBody').length) {
        var $loadingDiv = $(DIV({id:'facetLoading'},
                                facetLoadingMsg));
        $('body').append($loadingDiv);
    }
});