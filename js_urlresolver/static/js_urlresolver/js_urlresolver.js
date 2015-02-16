;
var reverseURL,
    resolveURL;

(function ($) {
    'use strict';

    reverseURL = function (urlparams, success, error) {
        $.ajax({
            url: _js_urlresolver_reverse,  // see js_urlresolver.html
            type: 'POST',
            data: JSON.stringify(urlparams),
            dataType: 'json',
            success: function (data) {
                if (typeof success != 'undefined') success(data['resolved']);
            },
            error: function () {
                if (typeof error != 'undefined') error();
            }
        })
    };

    resolveURL = function (rawurl, success, error) {
        $.ajax({
            url: _js_urlresolver_resolve,  // see js_urlresolver.html
            type: 'POST',
            data: JSON.stringify({url: rawurl}),
            dataType: 'json',
            success: function (data) {
                if (typeof success != 'undefined') success(data);
            },
            error: function () {
                if (typeof error != 'undefined') error();
            }
        })
    };
})(jQuery);
