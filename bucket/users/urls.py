from django.conf.urls import url

from users.views import *


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/bookmark$', BookmarkContentView.as_view(), name='bookmark_content'),
    url(r'^(?P<username>[\w.@+-]+)/bookmarks/$', AllBookmarksView.as_view(), name='all_bookmarks'),
    url(r'^(?P<username>[\w.@+-]+)/$', UserView.as_view(), name='user'),
    url(r'^(?P<username>[\w.@+-]+)/profile/$', UserProfileView.as_view(),
        name='user_profile'),
]
