from django.conf.urls import patterns, url

from warmup import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'users/login', views.login, name='login'),
    url(r'users/add', views.add, name='welcome'),
    url(r'TESTAPI/resetFixture', views.TESTAPI_resetfixture),
    url(r'TESTAPI/unitTests', views.TESTAPI_unittests),
    # Examples:
    # url(r'^$', 'hellodjango.views.home', name='home'),
    # url(r'^hellodjango/', include('hellodjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
)
