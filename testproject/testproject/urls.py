from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',
        TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^test/(?P<test_1>\w+)/(?P<test_2>\w+)/(?P<test_3>\w+)/$',
        TemplateView.as_view(template_name='base.html'), name='test'),
)
