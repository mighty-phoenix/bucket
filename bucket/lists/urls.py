from django.conf.urls import include, url

from lists.views import *

urlpatterns = [
    url(r'^all$', ListsPage.as_view(), name='lists_page'),
    url(r'^add$', AddListView.as_view(), name='add_list'),
    url(r'^(?P<slug>[\w-]+)/edit$', EditListView.as_view(), name='edit_list'),
    url(r'^(?P<slug>[\w-]+)/delete$', DeleteListView.as_view(), name='delete_list'),
    url(r'^(?P<slug>[\w-]+)$', ViewList.as_view(), name='view_list'),
    url(r'^(?P<slug>[\w-]+)/bookmark$', BookmarkListView.as_view(), name='bookmark_list'),
    url(r'^user-lists/$', AllUserListsView.as_view(), name='all_user_lists'),
    url(r'^bookmarked-lists/$', AllBookmarkedListsView.as_view(), name='all_bookmarked_lists'),
    url(r'^(?P<slug>[\w-]+)/add-to-list/(?P<content_slug>[\w-]+)$', AddToListView.as_view(), name='add_to_list'),
]
