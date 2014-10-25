from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'drScratch.views.home', name='home'),
    # url(r'^drScratch/', include('drScratch.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^login', 'app.views.loginUser',),
	url(r'^logout', 'app.views.logoutUser',),
	url(r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'resources'}),
	url(r'^profile', 'app.views.profileSettings',),
	url(r'^idproject/([1-9])/$', 'app.views.idProject',),
	url(r'^analyze', 'app.views.analyzeProject',),
	url(r'^uploadZip', 'app.views.uploadZip',),	
	url(r'^upload', 'app.views.upload_file'),
	#url(r'^dashboard/(.*)$', 'app.views.dashboard',),
	url(r'^mydashboard', 'app.views.mydashboard',),
	url(r'^historic', 'app.views.myHistoric',),
	url(r'^myprojects', 'app.views.myProjects',),
	url(r'^rules', 'app.views.defineRules',),
	url(r'^$', 'app.views.main'),
	

)
