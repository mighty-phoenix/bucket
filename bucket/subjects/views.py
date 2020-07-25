import os
import requests
import tmdbsimple as tmdb
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from braces.views import FormValidMessageMixin, FormInvalidMessageMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django_filters.views import FilterView

from subjects.constants import movie_genres, tv_genres
from subjects.forms import (AddSubjectForm, EditSubjectForm, AddContentForm,
                            EditContentForm, SearchMovies, SearchTVShows,
                            SearchBooks, SearchYoutube)
from subjects.filters import (ContentFilter, ContentBookmarkFilter,
                              ContentTagFilter, ContentTopicFilter)
from subjects.models import Subject, Content
from common.models import Tag
from users.models import BucketUser


tmdb.API_KEY = os.environ['TMDB_API_KEY']


class SubjectsList(ListView):
    """List all subjects"""
    model = Subject
    template_name = "subjects/subjects_list.html"

    def get_context_data(self, **kwargs):
        context = super(SubjectsList, self).get_context_data(**kwargs)
        context['subject_list'] = Subject.objects.order_by('name')
        return context


class SubjectPageView(ListView):
    """View a subject's page, which contains a list of all content associated
       with that subject.

       ## TODO: Change filtering to django-filters
    """
    model = Content
    template_name = "subjects/subject_page.html"
    context_object_name = 'subject_content'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        self.subject = get_object_or_404(Subject, slug=self.kwargs['slug'])
        qs = Content.objects.filter(subject=self.subject).order_by('title')
        #subject_content = filter_and_search_queryset(qs,self.request)
        return subject_content

    def get_context_data(self, **kwargs):
        context = super(SubjectPageView, self).get_context_data(**kwargs)
        context['subject'] = self.subject
        return context


class ContentsPage(FilterView):
    """List all content"""
    model = Content
    template_name = "subjects/contents_page.html"
    filterset_class = ContentFilter
    #paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(FilterView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            context['bucketuser'] = get_object_or_404(BucketUser, user=user)
        return context


#https://github.com/coderIlluminatus/django-tmdb/blob/master/movies/views.py
class MoviesPageView(FormView):
    template_name = 'subjects/movies_page.html'
    form_class = SearchMovies

    def get_success_url(self):
        return reverse('movies_page')

    def get_context_data(self, **kwargs):
        context = super(MoviesPageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            context['bucketuser'] = get_object_or_404(BucketUser, user=user)
        context['genres'] = movie_genres
        search = self.request.GET.get('search')
        genre = self.request.GET.getlist('genre')
        if search != '' and search is not None:
            movies = tmdb.Search().movie(query=search)['results']
            genre = [ int(i) for i in genre ]
            movies = [movie for movie in movies if set(genre) == set(genre).intersection(movie['genre_ids'])]
            context['movies'] = sorted(movies, key=lambda x: x['popularity'], reverse=True)
        else:
            genre = ', '.join(genre)
            movies = tmdb.Discover().movie(sort_by='popularity.desc', with_genres=genre)['results']
            context['movies'] = movies
        return context


class TVShowsPageView(FormView):
    template_name = 'subjects/tvshows_page.html'
    form_class = SearchTVShows

    def get_success_url(self):
        return reverse('tvshows_page')

    def get_context_data(self, **kwargs):
        context = super(TVShowsPageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            context['bucketuser'] = get_object_or_404(BucketUser, user=user)
        context['genres'] = tv_genres
        search = self.request.GET.get('search')
        genre = self.request.GET.getlist('genre')
        if search != '' and search is not None:
            tvshows = tmdb.Search().tv(query=search)['results']
            genre = [ int(i) for i in genre ]
            tvshows = [show for show in tvshows if set(genre) == set(genre).intersection(show['genre_ids'])]
            context['tvshows'] = sorted(tvshows, key=lambda x: x['popularity'], reverse=True)
        else:
            genre = ', '.join(genre)
            tvshows = tmdb.Discover().tv(sort_by='popularity.desc', with_genres=genre)['results']
            context['tvshows'] = tvshows
        return context


#https://openlibrary.org/developers/api
#https://github.com/internetarchive/openlibrary-client
class BooksPageView(FormView):
    template_name = 'subjects/books_page.html'
    form_class = SearchBooks

    def get_success_url(self):
        return reverse('books_page')

    def get_context_data(self, **kwargs):
        context = super(BooksPageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            context['bucketuser'] = get_object_or_404(BucketUser, user=user)
        search = self.request.GET.get('search')
        if search != '' and search is not None:
            url = 'http://openlibrary.org/search.json?title=' + search
            books = requests.get(url).json()['docs']
            context['books'] = books
        return context


class YoutubePageView(FormView):
    template_name = 'subjects/youtube_page.html'
    form_class = SearchYoutube

    def get_success_url(self):
        return reverse('youtube_page')

    def get_context_data(self, **kwargs):
        context = super(YoutubePageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            context['bucketuser'] = get_object_or_404(BucketUser, user=user)
        search = self.request.GET.get('search')
        if search != '' and search is not None:
            url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q=' \
                  + search \
                  + '&key=AIzaSyA3ghYFni1exM2g8QBdoDX3_jod4e_fJK8'
            videos = requests.get(url).json()['items']
            print(videos)
            context['videos'] = videos
        return context


class ContentView(DetailView):
    """View content page"""
    model = Content
    template_name = "subjects/content.html"

    def get_context_data(self, **kwargs):
        context = super(ContentView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            bucketuser = get_object_or_404(BucketUser, user=user)
            context['bucketuser'] = bucketuser
        context['content'] = self.object
        context['number_of_bookmarks'] = self.object.bookmarked_by.all().count()
        return context


class AddContentView(LoginRequiredMixin, CreateView):
    """Add new content"""
    model = Content
    template_name = "subjects/add_content.html"
    form_class = AddContentForm

    def get_success_url(self):
        """Redirect to content page."""
        messages.add_message(self.request, messages.SUCCESS, "Successfully added")
        return reverse("view_content", kwargs={"slug": self.object.slug})


class EditContentView(LoginRequiredMixin, UpdateView):
    """Update details of a content."""
    model = Content
    template_name = "subjects/edit_content.html"
    form_class = EditContentForm

    def get_success_url(self):
        """Redirect to content page."""
        messages.add_message(self.request, messages.INFO, "Info updated")
        return reverse("view_content", kwargs={"slug": self.object.slug})


class DeleteContentView(LoginRequiredMixin, DeleteView):
    """Delete a content."""
    model = Content
    template_name = "subjects/confirm_delete_content.html"

    def get_success_url(self):
        """Redirect to user profile in case of successful deletion"""
        bucketuser = get_object_or_404(BucketUser, user=self.request.user)
        messages.add_message(self.request, messages.WARNING, "Successfully deleted")
        return bucketuser.get_absolute_url()


#https://stackoverflow.com/questions/35796195/how-to-redirect-to-previous-page-in-django-after-post-request
class BookmarkContentView(LoginRequiredMixin, RedirectView):
    """Bookmark content"""
    model = Content
    template_name = "subjects/bookmark.html"

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        bucketuser = get_object_or_404(BucketUser, user=user)
        content = get_object_or_404(Content, slug=self.kwargs['slug'])
        if bucketuser in content.bookmarked_by.all():
            content.bookmarked_by.remove(bucketuser)
        else:
            content.bookmarked_by.add(bucketuser)
        return self.request.GET.get('next', reverse('view_content', kwargs={'slug': content.slug}))


class AllBookmarksView(LoginRequiredMixin, FilterView):
    """View list of all bookmarks"""
    model = Content
    template_name = "subjects/all_bookmarks.html"
    filterset_class = ContentBookmarkFilter
    #paginate_by = 10


class ViewTagContent(FilterView):
    """View all content of a tag"""
    model = Content
    template_name = "subjects/tag_content.html"
    filterset_class = ContentTagFilter

    def get_context_data(self, **kwargs):
        context = super(ViewTagContent, self).get_context_data(**kwargs)
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        context['tag'] = self.tag
        return context


class ViewTopicContent(FilterView):
    """View all content of a topic"""
    model = Content
    template_name = "subjects/topic_content.html"
    filterset_class = ContentTopicFilter

    def get_context_data(self, **kwargs):
        context = super(ViewTopicContent, self).get_context_data(**kwargs)
        self.topic = get_object_or_404(Topic, slug=self.kwargs['slug'])
        context['topic'] = self.topic
        return context
