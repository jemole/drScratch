from django.conf.urls import include, url, patterns
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.generic import RedirectView
admin.autodiscover()

urlpatterns = (
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
    #Blog
    url(r'^blog$', RedirectView.as_view(url='https://drscratchblog.wordpress.com')),
    #url(r'^profile', 'DrScratchApp.views.profileSettings',),
    url(r'^showDashboard', 'app.views.showDashboard',),
    url(r'^statistics$', 'app.views.statistics',),
    url(r'^collaborators$', 'app.views.collaborators',),

    #Organizations
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'app.views.reset_password_confirm',name="reset_password_confirm"),
    url(r'^changePwd$', 'app.views.changePwd',),
    url(r'^organizationHash', 'app.views.organizationHash',),
    url(r'^signUpOrganization$', 'app.views.signUpOrganization',),
    url(r'^organization/stats/(\w+)', 'app.views.stats',),
    url(r'^organization/downloads/(\w+)', 'app.views.downloads',),
    url(r'^organization/settings/(\w+)', 'app.views.settings',),
    url(r'^organization/(\w+)', 'app.views.organization',),
    url(r'^loginOrganization$', 'app.views.loginOrganization',),
    url(r'^logoutOrganization$', 'app.views.logoutOrganization',),


    #Coders
    url(r'^coderHash', 'app.views.coderHash',),
    url(r'^signUpCoder$', 'app.views.signUpCoder',),
    url(r'^coder/stats/(\w+)', 'app.views.stats',),
    url(r'^coder/downloads/(\w+)', 'app.views.downloads',),
    url(r'^coder/settings/(\w+)', 'app.views.settings',),
    url(r'^coder/(\w+)', 'app.views.coder',),
    url(r'^loginCoder$', 'app.views.loginCoder',),
    url(r'^logoutCoder$', 'app.views.logoutCoder',),

    #Upload a .CSV
    url(r'^analyzeCSV$', 'app.views.analyzeCSV',),
    
    #Contest: Temporary url
    url(r'^contest$', 'app.views.contest',),

    #Error pages
    #url(r'^500', 'app.views.error500',),
    #url(r'^404', 'app.views.error404',),
    #url(r'learn$', 'app.views.learnUnregistered',),
    url(r'^learn/(\w+)', 'app.views.learn',),
    url(r'^uploadRegistered', 'app.views.uploadRegistered',),
    url(r'^myDashboard', 'app.views.myDashboard',),
    url(r'^myHistoric', 'app.views.myHistoric',),
    url(r'^myProjects', 'app.views.myProjects',),
    url(r'^myRoles', 'app.views.myRoles',),
    url(r'^$', 'app.views.main',),
    url(r'^.*', 'app.views.redirectMain',),

)
