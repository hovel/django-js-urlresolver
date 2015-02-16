Installation
============

Add `js_urlresolver` into INSTALLED_APPS:

    INSTALLED_APPS = (
        ....
        'js_urlresolver',
    )

Add this into project's urls.py:

    url(r'^js_urlresolver/', include('js_urlresolver.urls', namespace='js_urlresolver')),

Include static template into base template right after jQuery (remove
`with autocsrf=True` if you don't want to enable automatic CSRF protection):

    <script src="{% static 'jquery.min.js' %}"></script>
    {% include 'js_urlresolver/js_urlresolver.html' with autocsrf=True %}


Usage
=====

`reverseURL` and `resolveURL` are global functions which make
async query towards `reverse` and `resolve` Django functions. Return nothing,
but run callbacks on success and error.

To use them, add `JS_URLRESOLVER_WHITELIST = []` into project's urls.py and
fill it with the names of the views you want to reverse/resolve.
DO NOT ADD ALL VIEWS, because it can lead to security problems.

```js
var urlparams = {
        viewname: 'name-of-url-to-redirect',
        kwargs: {
            param1: 'value1',
            param2: 'value2'
        }
    };
function success(url) {
    window.location.href = url;
}
function error() {
    alert('Oops...');
}
reverseURL(urlparams, success, error);

// ----------------------------------------- //

var url = window.location.href;
function success(data) {
    console.log(data['viewname']);
    console.log(data['kwargs']);
}
function error() {
    alert('Oops...');
}
resolveURL(url, success, error);
```
