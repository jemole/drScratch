from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

urlpatterns = (
    # Examples:
    # url(r'^$', 'drScratch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
    #url(r'^profile', 'DrScratchApp.views.profileSettings',),
    url(r'^selector', 'app.views.selector',),
    #url(r'^admin/upload_progress/$', 'app.views.upload_progress', name="admin-upload-progress"),
    url(r'^login', 'app.views.loginUser',),
    url(r'^logout', 'app.views.logoutUser',),
    url(r'^500', 'app.views.error500',),
    url(r'^404', 'app.views.error404',),
    url(r'^learn', 'app.views.learn',),
    url(r'^createUser', 'app.views.createUser',),
    url(r'^uploadRegistered', 'app.views.uploadRegistered',),
    url(r'^myDashboard', 'app.views.myDashboard',),
    url(r'^myHistoric', 'app.views.myHistoric',),
    url(r'^myProjects', 'app.views.myProjects',),
    url(r'^myRoles', 'app.views.myRoles',),
    url(r'^$', 'app.views.main',),
    url(r'^.*', 'app.views.redirectMain',),
    
)
