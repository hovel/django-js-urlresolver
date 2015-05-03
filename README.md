Installation
============

Add `js_urlresolver` into INSTALLED_APPS:

    INSTALLED_APPS = (
        ....
        'js_urlresolver',
    )

Add `JS_URLRESOLVER_NAMES = []` into project's settings.py
and fill it with the names of the views you want to reverse/resolve.
DO NOT ADD ALL VIEWS, because it can lead to security problems.
Namespaces are not supported yet.


Include url "database" and resolver script into the main template:

    {% load js_urlresolver staticfiles %}
    <script>
        window.JSURLResolverData = '{% js_urlresolver_data %}'
    </script>
    <script src="{% static 'js_urlresolver/js_urlresolver.js' %}"></script>


Usage
=====

Call `reverse` and `resolve` methods from `window.JSURLResolver` object
(will be created automatically).
`reverse` takes name and kwargs, returns url.
`resolve` takes url, returns array with name and kwargs.

This is example from test project:

    // r'^test/(?P<test_1>\w+)/(?P<test_2>\w+)/(?P<test_3>\w+)/$'

    var urldata = JSURLResolver.resolve(window.location.pathname);
    window.location.href = JSURLResolver.reverse(
        urldata[0], {'test_2': urldata[1]['test_2'] * 2,
                     'test_3': urldata[1]['test_3'] * 2,
                     'test_1': urldata[1]['test_1'] * 2}
    );
