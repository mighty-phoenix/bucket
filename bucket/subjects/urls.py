from django.conf.urls import include, url

from subjects.views import *

urlpatterns = [
    url(r'^subjects/$', SubjectsList.as_view(), name='list_subjects'),
    url(r'^(?P<slug>[\w-]+)$', SubjectPageView.as_view(), name='view_subject_page'),
    url(r'^$', ContentsPage.as_view(), name='contents_page'),
    url(r'^content/add$', AddContentView.as_view(), name='add_content'),
    url(r'^content/(?P<slug>[\w-]+)/edit$', EditContentView.as_view(), name='edit_content'),
    url(r'^content/(?P<slug>[\w-]+)/delete$', DeleteContentView.as_view(), name='delete_content'),
    url(r'^content/(?P<slug>[\w-]+)$', ContentView.as_view(), name='view_content'),
    url(r'^content/(?P<slug>[\w-]+)/bookmark$', BookmarkContentView.as_view(), name='bookmark_content'),
    url(r'^bookmarks/$', AllBookmarksView.as_view(), name='all_bookmarks'),
]
