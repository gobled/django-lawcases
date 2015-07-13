from django.conf.urls import patterns, include, url
from lawcases.apps.public.views import upload, index, view_cases, search, view_case, download, view_staff
from lawcases.apps.public.views import view_clients, view_client, dashboard
from lawcases.apps.core.views import add_client
from lawcases.apps.core.views import add_case, add_entry, add_payment, add_keydate, add_file
from lawcases.apps.core.views import add_staff, add_group
from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cases.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
   
    url(r'^cases/search/$', search),
    url(r'^cases/upload/$', upload),
    url(r'^cases/add/$', add_case),
    url(r'^cases/add/(?P<model_id>\d+)/$', add_case),
    
    url(r'^cases/(?P<case_id>\d+)/$', view_case),
    url(r'^cases/page/(?P<page>\d+)/$', view_cases),
    url(r'^cases/', view_cases),
    
    
    url(r'^files/(?P<model_id>\d+)/$', add_file),
    url(r'^files/add/$', add_file),
    
    url(r'^keydates/(?P<keydate_id>\d+)/$', add_keydate),
    url(r'^keydates/add/$', add_keydate),
    url(r'^keydates/add/(?P<case_id>\d+)/$', add_keydate),
    
    url(r'^entries/(?P<entry_id>\d+)/$', add_entry),
    url(r'^entries/add/$', add_entry),
    url(r'^entries/add/(?P<case_id>\d+)/$', add_entry),
    
    url(r'^payments/(?P<payment_id>\d+)/$', add_payment),
    url(r'^payments/add/$', add_payment),
    url(r'^payments/add/(?P<case_id>\d+)/$', add_payment),
    
    url(r'^clients/add/', add_client),
    url(r'^clients/(?P<client_id>\d+)/$', view_client),
    url(r'^clients/page/(?P<page>\d+)/$', view_clients),
    url(r'^clients/', view_clients),
	
    url(r'^staff/$', view_staff),
    url(r'^staff/(?P<user_id>\d+)/$', add_staff),
    url(r'^staff/add/$', add_staff),
    
    #url(r'^groups/(?P<user_id>\d+)/$', view_groups),
    url(r'^groups/add/$', add_group),
    
    url(r'^documents(?P<path>.*)$', download),
    # url(r'^cases/(?P<page>\d+)/$', view_cases),
    # url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    url(r'^logout', logout),
    url(r'^login$', login),
    url(r'^dashboard', dashboard),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    
)
