;
var djangoJSURLReverse,
    djangoJSURLResolve,
    djangoURLReverseAddress = djangoURLReverseAddress,
    djangoURLResolveAddress = djangoURLResolveAddress;

(function ($) {
    'use strict';

    djangoJSURLReverse = function (urlparams, success, error) {
        $.ajax({
            url: djangoURLReverseAddress,
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
            url: djangoURLResolveAddress,
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
