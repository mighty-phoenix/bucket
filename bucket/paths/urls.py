from django.conf.urls import include, url

from paths.views import *

urlpatterns = [
    url(r'^$', PathsPage.as_view(), name='paths_page'),
    url(r'^add$', AddPathView.as_view(), name='add_path'),
    url(r'^(?P<slug>[\w-]+)/edit$', EditPathView.as_view(), name='edit_path'),
    url(r'^(?P<slug>[\w-]+)/delete$', DeletePathView.as_view(),
        name='delete_path'),
    url(r'^(?P<slug>[\w-]+)$', ViewPath.as_view(), name='view_path'),
    url(r'^(?P<username>[\w.@+-]+)/user-paths/$', AllUserPathsView.as_view(),
        name='all_user_paths'),
    url(r'^(?P<slug>[\w-]+)/add-to-path/$', AddToPathView.as_view(),
        name='add_to_path'),
    url(r'^(?P<slug>[\w-]+)/remove-from-path/(?P<content_slug>[\w-]+)$',
        RemoveContentFromPathView.as_view(),
        name='remove_from_path'),
]
