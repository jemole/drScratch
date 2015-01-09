from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'DrScratch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
    #url(r'^profile', 'DrScratchApp.views.profileSettings',),
    url(r'^progressBar', 'app.views.progressBar',),
    url(r'^admin/upload_progress/$', 'utils.views.upload_progress', name="admin-upload-progress"),
    url(r'^login', 'app.views.loginUser',),
    url(r'^logout', 'app.views.logoutUser',),
    url(r'^uploadUnregistered', 'app.views.uploadUnregistered',),
    url(r'^uploadRegistered', 'app.views.uploadRegistered',),
    url(r'^myDashboard', 'app.views.myDashboard',),
    url(r'^myHistoric', 'app.views.myHistoric',),
    url(r'^myProjects', 'app.views.myProjects',),
	url(r'^myRoles', 'app.views.myRoles',),
    url(r'^$', 'app.views.main',),
    url(r'^.*', 'app.views.redirectMain'),
    
]
