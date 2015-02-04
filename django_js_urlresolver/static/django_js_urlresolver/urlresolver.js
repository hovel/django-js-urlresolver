;
var djangoJSURLReverse,
    djangoJSURLResolve;

(function ($) {
    'use strict';

    djangoJSURLReverse = function (urlparams, success, error) {
        $.ajax({
            url: _django_js_urlresolver_urlreverse_url,  // see urlresolver.html
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

    djangoJSURLResolve = function (rawurl, success, error) {
        $.ajax({
            url: _django_js_urlresolver_urlresolve_url,  // see urlresolver.html
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
