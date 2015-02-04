Installation
============

Add `django_js_urlresolver` into INSTALLED_APPS:

    INSTALLED_APPS = (
        ....
        'django_js_urlresolver',
    )

Add this into project's urls.py:

    url(r'^urlresolver/', include('django_js_urlresolver.urls', namespace='django_js_urlresolver')),

Include static template into base template right after jQuery (remove
`with autocsrf=True` if you don't want to enable automatic CSRF protection):

    <script src="{% static 'jquery.min.js' %}"></script>
    {% include 'django_js_urlresolver/urlresolver.html' with autocsrf=True %}


Usage
=====

`djangoJSURLReverse` and `djangoJSURLResolve` are global functions which make
async query towards `reverse` and `resolve` Django functions. Return nothing,
but run callbacks on success and error.

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
djangoJSURLReverse(urlparams, success, error);

// ----------------------------------------- //

var url = window.location.href;
function success(data) {
    console.log(data['viewname']);
    console.log(data['kwargs']);
}
function error() {
    alert('Oops...');
}
djangoJSURLResolve(url, success, error);
```
