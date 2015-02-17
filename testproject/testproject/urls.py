from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^js_urlresolver/',
        include('js_urlresolver.urls', namespace='js_urlresolver')),
    url(r'^$',
        TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^test/(?P<test_id>\d+)/$',
        TemplateView.as_view(template_name='base.html'), name='test'),
)
