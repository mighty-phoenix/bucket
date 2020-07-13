#from django.shortcuts import render
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

from subjects.constants import CONTENT_TYPES
from subjects.forms import (AddSubjectForm, EditSubjectForm,
                            AddContentForm, EditContentForm)
from subjects.filters import ContentFilter, ContentBookmarkFilter, ContentTagFilter
from subjects.models import Subject, Content
from common.models import Tags
from users.models import BucketUser


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


class ContentView(DetailView):
    """View content page"""
    model = Content
    template_name = "subjects/content.html"

    def get_context_data(self, **kwargs):
        context = super(ContentView, self).get_context_data(**kwargs)
        context['content'] = self.object
        content_bookmarked_by = self.object.bookmarked_by.all()
        context['content_bookmarked_by'] = content_bookmarked_by
        context['number_of_bookmarks'] = content_bookmarked_by.count()
        is_bookmark = False
        is_in_user_list = False
        context['user_lists'] = []
        if self.request.user.is_authenticated:
            user = self.request.user
            bucketuser = get_object_or_404(BucketUser, user=user)
            if self.object.bookmarked_by.filter(id=bucketuser.id).exists():
                is_bookmark = True
            user_lists = bucketuser.list_set.all()
            in_list = []
            for i in range(len(user_lists)):
                if self.object in user_lists[i].content.all():
                    in_list.append(1)
                else:
                    in_list.append(0)
            context['user_lists'] = list(zip(user_lists, in_list))
            if 1 in in_list:
                is_in_user_list = True
        context['is_bookmark'] = is_bookmark
        context['is_in_user_list'] = is_in_user_list
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


class BookmarkContentView(LoginRequiredMixin, RedirectView):
    """Bookmark content"""
    model = Content
    template_name = "subjects/bookmark.html"

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        bucketuser = get_object_or_404(BucketUser, user=user)
        content = get_object_or_404(Content, slug=self.kwargs['slug'])
        if content.bookmarked_by.filter(id=bucketuser.id).exists():
            content.bookmarked_by.remove(bucketuser)
        else:
            content.bookmarked_by.add(bucketuser)
        return reverse('view_content', kwargs={'slug': content.slug})


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
        self.tag = get_object_or_404(Tags, slug=self.kwargs['slug'])
        context['tag'] = self.tag
        return context
