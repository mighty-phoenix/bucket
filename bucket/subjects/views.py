import os
import io
import requests
import tmdbsimple as tmdb
from PIL import Image
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.core.files.base import ContentFile
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from braces.views import FormValidMessageMixin, FormInvalidMessageMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django_filters.views import FilterView

from users.mixins import UserListsMixin
from subjects.constants import movie_genres, tv_genres
from subjects.forms import (AddSubjectForm, EditSubjectForm, AddContentForm,
                            EditContentForm, SearchMovies, SearchTVShows,
                            SearchBooks, SearchYoutube, SearchExternalDataForm)
from subjects.filters import (ContentFilter, ContentTagFilter,
                              ContentTopicFilter)
from subjects.models import Subject, Content
from common.models import Tag, Topic
from users.models import BucketUser
from lists.models import List


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
        return qs

    def get_context_data(self, **kwargs):
        context = super(SubjectPageView, self).get_context_data(**kwargs)
        context['subject'] = self.subject
        return context


class HomePage(FilterView):
    """Home page"""
    model = Content
    template_name = "subjects/homepage.html"
    filterset_class = ContentFilter

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['movies'] = Content.objects.filter(type='movie')
        context['books'] = Content.objects.filter(type='book')
        context['tv_shows'] = Content.objects.filter(type='tv')
        return context


class ContentsPage(UserListsMixin, FilterView):
    """List all content"""
    model = Content
    template_name = "subjects/contents_page.html"
    filterset_class = ContentFilter
    #paginate_by = 10


class ContentView(UserListsMixin, DetailView):
    """View content page"""
    model = Content
    template_name = "subjects/content.html"

    def get_context_data(self, **kwargs):
        context = super(ContentView, self).get_context_data(**kwargs)
        context['content'] = self.object
        context['number_of_bookmarks'] = self.object.content_bookmarked_by.all().count()
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


class ViewTagContent(UserListsMixin, FilterView):
    """View all content of a tag"""
    model = Content
    template_name = "subjects/tag_content.html"
    filterset_class = ContentTagFilter

    def get_context_data(self, **kwargs):
        context = super(ViewTagContent, self).get_context_data(**kwargs)
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        context['tag'] = self.tag
        return context


class ViewTopicContent(UserListsMixin, FilterView):
    """View all content of a topic"""
    model = Content
    template_name = "subjects/topic_content.html"
    filterset_class = ContentTopicFilter

    def get_context_data(self, **kwargs):
        context = super(ViewTopicContent, self).get_context_data(**kwargs)
        self.topic = get_object_or_404(Topic, slug=self.kwargs['slug'])
        context['topic'] = self.topic
        return context


class SearchExternalDataView(UserListsMixin, FormView):
    template_name = 'subjects/search_external_data.html'
    form_class = SearchExternalDataForm

    def get_success_url(self):
        return reverse('search_external_data')

    def get_context_data(self, **kwargs):
        context = super(SearchExternalDataView, self).get_context_data(**kwargs)
        search = self.request.GET.get('global_search')
        type = self.request.GET.get('media_type')
        context['type'] = type
        if search != '' and search is not None:
            if type == 'movie':
                movie_genres.update(tv_genres)
                context['genres'] = movie_genres
                movies = tmdb.Search().movie(query=search)['results']
                context['contents'] = sorted(movies, key=lambda x: x['popularity'], reverse=True)
            elif type == 'tv':
                movie_genres.update(tv_genres)
                context['genres'] = movie_genres
                tvshows = tmdb.Search().tv(query=search)['results']
                context['contents'] = sorted(tvshows, key=lambda x: x['popularity'], reverse=True)
            elif type == 'book':
                url = 'http://openlibrary.org/search.json?q=' + search
                books = requests.get(url).json()['docs']
                context['contents'] = books
        return context


def get_django_file_from_image_url(url):
    # get image from URL
    response = requests.get(url)
    image = io.BytesIO(response.content)
    # get PIL image
    pil_image = Image.open(image)
    # convert PIL image to django file
    fobject = io.BytesIO()
    pil_image.save(fobject, format="JPEG")
    return ContentFile(fobject.getvalue())


class AddToDatabaseView(LoginRequiredMixin, RedirectView):
    """Add data from external database to our database

    # TODO: Add description for books
    # TODO: Consider pre-downloading entire book database from openlibrary
    """
    model = Content

    def get_redirect_url(self, *args, **kwargs):
        id = self.kwargs['id']
        type = self.kwargs['type']
        new_content = None
        if type == "movie" and not Content.objects.filter(type='movie', content_id=id).exists():
            # get movie data from tmdb
            movie = tmdb.Movies(id=id).info()
            # create a new Content object
            new_content = Content.objects.create(
                title=movie['title'],
                url='https://www.imdb.com/title/' + movie['imdb_id'],
                content_id=id,
                type='movie',
                description=movie['overview']
            )
            # add tags
            new_content.tags = [genre['name'] for genre in movie['genres']]
            # add image
            #https://timmyomahony.com/blog/upload-and-validate-image-from-url-in-django
            if movie['poster_path']:
                image_url = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2' + movie['poster_path']
                django_file = get_django_file_from_image_url(image_url)
                new_content.image.save(f'{new_content.slug}.jpg', django_file)
        elif type == "tv" and not Content.objects.filter(type='tv', content_id=id).exists():
            # get tv show data from tmdb
            tvshow = tmdb.TV(id=id).info(append_to_response='videos')
            # create a new Content object
            new_content = Content.objects.create(
                title=tvshow['name'],
                content_id=id,
                type='tv',
                description=tvshow['overview']
            )
            # add url
            if tvshow['videos']['results']:
                new_content.url='https://www.youtube.com/watch?v=' + tvshow['videos']['results'][0]['key']
            # add tags
            new_content.tags = [genre['name'] for genre in tvshow['genres']]
            # add image
            #https://timmyomahony.com/blog/upload-and-validate-image-from-url-in-django
            if tvshow['poster_path']:
                image_url = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2' + tvshow['poster_path']
                django_file = get_django_file_from_image_url(image_url)
                new_content.image.save(f'{new_content.slug}.jpg', django_file)
        elif type == "book" and not Content.objects.filter(type='book', content_id=id).exists():
            # get book data from openlibrary
            olid = 'OLID:' + id
            url = 'https://openlibrary.org/api/books?bibkeys=' + olid + '&jscmd=details&format=json'
            book = requests.get(url).json()[olid]
            # create a new Content object
            new_content = Content.objects.create(
                title=book['details']['title'],
                content_id=id,
                url=book['preview_url'],
                type='book',
            )
            # add description
            try:
                description = book['details']['description']
                if isinstance(description, dict):
                    new_content.description = description['value']
                else:
                    new_content.description = description
            except:
                pass
            # add image
            #https://timmyomahony.com/blog/upload-and-validate-image-from-url-in-django
            image_url = 'https://covers.openlibrary.org/b/olid/' + id + '-M.jpg?default=false'
            django_file = get_django_file_from_image_url(image_url)
            new_content.image.save(f'{new_content.slug}.jpg', django_file)
        if new_content:
            return reverse('view_content', kwargs={"slug": new_content.slug})
        else:
            content = Content.objects.filter(type=type, content_id=id)[0]
            return reverse('view_content', kwargs={"slug": content.slug})


#https://github.com/coderIlluminatus/django-tmdb/blob/master/movies/views.py
class MoviesPageView(UserListsMixin, FormView):
    template_name = 'subjects/movies_page.html'
    form_class = SearchMovies

    def get_success_url(self):
        return reverse('movies_page')

    def get_context_data(self, **kwargs):
        context = super(MoviesPageView, self).get_context_data(**kwargs)
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


class TVShowsPageView(UserListsMixin, FormView):
    template_name = 'subjects/tvshows_page.html'
    form_class = SearchTVShows

    def get_success_url(self):
        return reverse('tvshows_page')

    def get_context_data(self, **kwargs):
        context = super(TVShowsPageView, self).get_context_data(**kwargs)
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
class BooksPageView(UserListsMixin, FormView):
    template_name = 'subjects/books_page.html'
    form_class = SearchBooks

    def get_success_url(self):
        return reverse('books_page')

    def get_context_data(self, **kwargs):
        context = super(BooksPageView, self).get_context_data(**kwargs)
        search = self.request.GET.get('search')
        if search != '' and search is not None:
            url = 'http://openlibrary.org/search.json?title=' + search
            books = requests.get(url).json()['docs']
            context['books'] = books
        return context


"""
class YoutubePageView(UserListsMixin, FormView):
    template_name = 'subjects/youtube_page.html'
    form_class = SearchYoutube

    def get_success_url(self):
        return reverse('youtube_page')

    def get_context_data(self, **kwargs):
        context = super(YoutubePageView, self).get_context_data(**kwargs)
        search = self.request.GET.get('search')
        if search != '' and search is not None:
            url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q=' \
                  + search + '&key=' + YOUTUBE_API_KEY
            videos = requests.get(url).json()['items']
            context['videos'] = videos
        return context
"""
