from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',
        TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^test/(?P<test_1>\w+)/(?P<test_2>\w+)/(?P<test_3>\w+)/$',
        TemplateView.as_view(template_name='base.html'), name='test'),
    url(r'^test/(?P<test_21>\w+)/(?P<test_22>\w+)/(?P<test_23>\w+)/$',
        TemplateView.as_view(template_name='base.html'), name='test2'),
]
