from django.conf.urls import include, url

from subjects.views import *

urlpatterns = [
    url(r'^subjects/$', SubjectsList.as_view(), name='list_subjects'),
    url(r'^(?P<slug>[\w-]+)$', SubjectPageView.as_view(), name='view_subject_page'),
    url(r'^$', ContentsPage.as_view(), name='contents_page'),
    url(r'^search/$', SearchExternalDataView.as_view(), name='search_external_data'),
    url(r'^movies/$', MoviesPageView.as_view(), name='movies_page'),
    url(r'^tv-shows/$', TVShowsPageView.as_view(), name='tvshows_page'),
    url(r'^books/$', BooksPageView.as_view(), name='books_page'),
    url(r'^youtube/$', YoutubePageView.as_view(), name='youtube_page'),
    url(r'^add-to-database/(?P<type>[\w-]+)/(?P<id>[\w-]+)$', AddToDatabaseView.as_view(), name='add_to_database'),
    url(r'^content/add$', AddContentView.as_view(), name='add_content'),
    url(r'^content/(?P<slug>[\w-]+)/edit$', EditContentView.as_view(), name='edit_content'),
    url(r'^content/(?P<slug>[\w-]+)/delete$', DeleteContentView.as_view(), name='delete_content'),
    url(r'^content/(?P<slug>[\w-]+)$', ContentView.as_view(), name='view_content'),
    url(r'^tags/(?P<slug>[\w-]+)/$', ViewTagContent.as_view(), name='view_tag'),
    url(r'^topics/(?P<slug>[\w-]+)/$', ViewTopicContent.as_view(), name='view_topic')
]
