;(function () {
    if (typeof window.JSURLResolverData != 'string') {
        console.error('JSURLResolver is not installed properly');
    }

    window.JSURLResolver = new function () {
        var self = this;
        self.data = JSON.parse(window.JSURLResolverData || '{}');
        delete window.JSURLResolverData;

        self.reverse = function (name, kwargs) {
            var urldata = self.data[name];
            if (typeof urldata == 'undefined') {
                return null;
            }
            var url = urldata.replace_pattern;
            for (var i = 0; i < urldata.kwargs.length; i++) {
                var kwarg = urldata.kwargs[i];
                url = url.replace('%(' + kwarg + ')s', kwargs[kwarg]);
            }
            var testRegex = new RegExp(urldata.test_pattern);
            if (testRegex.test(url)) {
                return url;
            }
            return null;
        };

        self.resolve = function (url) {
            for (var name in self.data) {
                if (self.data.hasOwnProperty(name)) {
                    var urldata = self.data[name],
                        testRegex = new RegExp(urldata.test_pattern),
                        matches = url.match(testRegex);
                    if (matches !== null) {
                        var filledKwargs = {};
                        if (urldata.kwargs.length > 0) {
                            for (var i = 0; i < urldata.kwargs.length; i++) {
                                filledKwargs[urldata.kwargs[i]] = matches[i + 1];
                            }
                        }
                        return [name, filledKwargs];
                    }
                }
            }
            return [null, null];
        };
    };
})();
