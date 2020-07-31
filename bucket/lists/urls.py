from django.conf.urls import include, url

from lists.views import *

urlpatterns = [
    url(r'^$', ListsPage.as_view(), name='lists_page'),
    url(r'^add$', AddListView.as_view(), name='add_list'),
    url(r'^(?P<slug>[\w-]+)/edit$', EditListView.as_view(), name='edit_list'),
    url(r'^(?P<slug>[\w-]+)/delete$', DeleteListView.as_view(),
        name='delete_list'),
    url(r'^(?P<slug>[\w-]+)$', ViewList.as_view(), name='view_list'),
    url(r'^(?P<slug>[\w-]+)/bookmark$', BookmarkListView.as_view(),
        name='bookmark_list'),
    url(r'^(?P<username>[\w.@+-]+)/user-lists/$', AllUserListsView.as_view(),
        name='all_user_lists'),
    url(r'^(?P<username>[\w.@+-]+)/bookmarked-lists/$',
        AllBookmarkedListsView.as_view(), name='all_bookmarked_lists'),
    url(r'^(?P<slug>[\w-]+)/add-to-list/(?P<content_slug>[\w-]+)$',
        AddToListFromContentsPageView.as_view(),
        name='add_to_list_from_contents_page'),
    url(r'^(?P<slug>[\w-]+)/add-to-list/$',
        AddToListFromListPageView.as_view(), name='add_to_list_from_list_page'),
    url(r'^(?P<slug>[\w-]+)/remove-from-list/(?P<content_slug>[\w-]+)$',
        RemoveContentFromListView.as_view(),
        name='remove_from_list'),
]
