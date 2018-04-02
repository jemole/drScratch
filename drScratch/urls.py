from django.conf.urls import include, url, patterns
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.generic import RedirectView
admin.autodiscover()

urlpatterns = (
    url(r'^admin/', include(admin.site.urls)),

    #Statics
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', 
                                {'document_root' : settings.MEDIA_ROOT}),
    url(r'^(.*)/static/(?P<path>.*)$', 'django.views.static.serve', 
                                {'document_root' : settings.MEDIA_ROOT}),

    #Statistics
    url(r'^statistics$', 'app.views.statistics',),

    #Collaborators
    url(r'^collaborators$', 'app.views.collaborators',),

    #Contest: Temporary url
    url(r'^contest$', 'app.views.contest',),

    #Blog
    url(r'^blog$', 
        RedirectView.as_view(url='https://drscratchblog.wordpress.com')),

    #Dashboards
    url(r'^show_dashboard', 'app.views.show_dashboard',),
    url(r'^download_certificate', 'app.views.download_certificate',),

    #Translation
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^blocks$', 'app.views.blocks'),

    #Organizations
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'app.views.reset_password_confirm',name="reset_password_confirm"),
    url(r'^change_pwd$', 'app.views.change_pwd',),
    #url(r'^organization_hash', 'app.views.organization_hash',),
    url(r'^sign_up_organization$', 'app.views.sign_up_organization',),
    url(r'^organization/stats/(\w+)', 'app.views.stats',),
    url(r'^organization/downloads/(.*)', 'app.views.downloads',),
    url(r'^organization/settings/(\w+)', 'app.views.settings',),
    url(r'^organization/(.*)', 'app.views.organization',),
    url(r'^login_organization$', 'app.views.login_organization',),
    url(r'^logout_organization$', 'app.views.logout_organization',),


    #Coders
    url(r'^coder_hash', 'app.views.coder_hash',),
    url(r'^sign_up_coder$', 'app.views.sign_up_coder',),
    url(r'^coder/stats/(\w+)', 'app.views.stats',),
    url(r'^coder/downloads/(.*)', 'app.views.downloads',),
    url(r'^coder/settings/(\w+)', 'app.views.settings',),
    url(r'^coder/(.*)', 'app.views.coder',),
    url(r'^login_coder$', 'app.views.login_coder',),
    url(r'^logout_coder$', 'app.views.logout_coder',),

    #Upload a .CSV
    url(r'^analyze_CSV$', 'app.views.analyze_CSV',),

    #Plugins
    url(r'^plugin/(.*)', 'app.views.plugin',),

    #Discuss
    url(r'^discuss$', 'app.views.discuss',),

    #Ajax
    url(r'search_email/$', 'app.views.search_email',),
    url(r'search_username/$', 'app.views.search_username',),
    url(r'search_hashkey/$', 'app.views.search_hashkey',),


    #Error pages
    #url(r'^500', 'app.views.error500',),
    #url(r'^404', 'app.views.error404',),

    #Learn
    url(r'^learn/(\w+)', 'app.views.learn',),
    url(r'^$', 'app.views.main',),
    url(r'^.*', 'app.views.redirect_main',),

)
