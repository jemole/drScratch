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
    url(r'^progressBar', 'DrScratchApp.views.progressBar',),
    url(r'^admin/upload_progress/$', 'utils.views.upload_progress', name="admin-upload-progress"),
    url(r'^login', 'DrScratchApp.views.loginUser',),
    url(r'^logout', 'DrScratchApp.views.logoutUser',),
    url(r'^uploadUnregistered', 'DrScratchApp.views.uploadUnregistered',),
    url(r'^uploadRegistered', 'DrScratchApp.views.uploadRegistered',),
    url(r'^myDashboard', 'DrScratchApp.views.myDashboard',),
    url(r'^myHistoric', 'DrScratchApp.views.myHistoric',),
    url(r'^myProjects', 'DrScratchApp.views.myProjects',),
	url(r'^myRoles', 'DrScratchApp.views.myRoles',),
    url(r'^$', 'DrScratchApp.views.main',),
    url(r'^.*', 'DrScratchApp.views.redirectMain'),
    
]
