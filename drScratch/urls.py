from django.conf.urls import include, url, patterns
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = (
    # Examples:
    # url(r'^$', 'drScratch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
    #url(r'^profile', 'DrScratchApp.views.profileSettings',),
    url(r'^selector', 'app.views.selector',),
    #url(r'^login', 'app.views.loginUser',),
    #url(r'^logout', 'app.views.logoutUser',),
    url(r'^users$', 'app.views.signUpUser',),
    url(r'^collaborators$', 'app.views.collaborators',),
    url(r'^organizationHash', 'app.views.organizationHash',),
    url(r'^organization$', 'app.views.signUpOrganization',),
    url(r'^organization/(\w+)', 'app.views.organization',),
    url(r'^loginOrganization$', 'app.views.loginOrganization',),
    url(r'^logoutOrganization$', 'app.views.logoutOrganization',),
    #url(r'^500', 'app.views.error500',),
    #url(r'^404', 'app.views.error404',),
    url(r'learn$', 'app.views.learnUnregistered',),
    url(r'^learn/(\w+)', 'app.views.learn',),
    url(r'^createUserHash', 'app.views.createUserHash',),
    url(r'^uploadRegistered', 'app.views.uploadRegistered',),
    url(r'^myDashboard', 'app.views.myDashboard',),
    url(r'^myHistoric', 'app.views.myHistoric',),
    url(r'^myProjects', 'app.views.myProjects',),
    url(r'^myRoles', 'app.views.myRoles',),
    url(r'^$', 'app.views.main',),
    url(r'^.*', 'app.views.redirectMain',),
    
)
