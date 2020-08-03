from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve

from common.views import ContactView, AboutUsView, Logout

urlpatterns = [
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^about-us/$', AboutUsView.as_view(), name='about-us'),
    url(r'', include('subjects.urls')),
    url(r'^list/', include('lists.urls')),
    url(r'^path/', include('paths.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/', Logout.as_view(), name='logout'),
    url(r'^accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    ]
