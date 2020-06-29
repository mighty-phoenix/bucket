from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User

from lists.forms import *
from lists.models import List
from subjects.models import Content
from users.models import BucketUser


class ListsPage(ListView):
    """Show all lists"""
    model = List
    template_name = "lists/lists_page.html"
    context_object_name = 'lists'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        lists = List.objects.all().order_by('name')
        return lists


class ViewList(DetailView):
    """View all content in a list."""
    model = List
    template_name = "lists/list.html"

    def get_context_data(self, **kwargs):
        context = super(ViewList, self).get_context_data(**kwargs)
        context['list'] = self.object
        list_content = self.object.content.all()
        context['list_content'] = list_content
        context['number_of_items'] = list_content.count()
        list_bookmarked_by = self.object.bookmarked_by.all()
        context['list_bookmarked_by'] = list_bookmarked_by
        context['number_of_bookmarks'] = list_bookmarked_by.count()
        is_bookmark = False
        if self.request.user.is_authenticated:
            user = self.request.user
            bucketuser = get_object_or_404(BucketUser, user=user)
            if self.object.bookmarked_by.filter(id=bucketuser.id).exists():
                is_bookmark = True
        context['is_bookmark'] = is_bookmark
        return context


class AddListView(LoginRequiredMixin, CreateView):
    """Create a new List"""
    model = List
    template_name = "lists/add_list.html"
    form_class = AddListForm

    def get_success_url(self):
        """Redirect to list page."""
        messages.add_message(self.request, messages.SUCCESS, "List created")
        return reverse("view_list", kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        """Add user to the instance."""
        bucketuser = get_object_or_404(BucketUser, user=self.request.user)
        form.instance.user = bucketuser
        return super().form_valid(form)


class EditListView(LoginRequiredMixin, UpdateView):
    """Update a list."""
    model = List
    template_name = "lists/edit_list.html"
    form_class = EditListForm

    def get_success_url(self):
        """Redirect to list page."""
        messages.add_message(self.request, messages.INFO, "List updated")
        return reverse("view_list", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add user to the context."""
        context = super(EditListView, self).get_context_data(**kwargs)
        bucketuser = get_object_or_404(BucketUser, user=self.request.user)
        context['user'] = bucketuser
        return context


class DeleteListView(LoginRequiredMixin, DeleteView):
    """Delete a list."""
    model = List
    template_name = "lists/confirm_delete_list.html"

    def get_success_url(self):
        """Redirect to user profile in case of successful deletion"""
        bucketuser = get_object_or_404(BucketUser, user=self.request.user)
        messages.add_message(self.request, messages.WARNING, "List deleted")
        return bucketuser.get_absolute_url()


class BookmarkListView(LoginRequiredMixin, RedirectView):
    """Bookmark a list"""
    model = Content
    template_name = "lists/bookmark.html"

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        bucketuser = get_object_or_404(BucketUser, user=user)
        list = get_object_or_404(List, slug=self.kwargs['slug'])
        if list.bookmarked_by.filter(id=bucketuser.id).exists():
            list.bookmarked_by.remove(bucketuser)
        else:
            list.bookmarked_by.add(bucketuser)
        return reverse('view_list', kwargs={'slug': list.slug})


class AllUserListsView(LoginRequiredMixin, ListView):
    """View all lists created by the user."""
    model = List
    template_name = "lists/all_user_lists.html"
    context_object_name = 'user_lists'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        bucketuser = get_object_or_404(BucketUser, user=self.request.user)
        user_lists = bucketuser.list_set.all().order_by('name')
        return user_lists


class AllBookmarkedListsView(LoginRequiredMixin, ListView):
    """View all lists bookmarked by the user."""
    model = List
    template_name = "lists/all_bookmarked_lists.html"
    context_object_name = 'bookmarked_lists'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        bucketuser = get_object_or_404(BucketUser, user=self.request.user)
        user_lists = bucketuser.list_bookmark.all().order_by('name')
        return user_lists


class AddToListView(LoginRequiredMixin, RedirectView):
    """Add a content to a user list"""
    model = List
    template_name = "lists/add_to_list.html"

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        bucketuser = get_object_or_404(BucketUser, user=user)
        content = get_object_or_404(Content, title=self.kwargs['slug'])
        if content.bookmarked_by.filter(id=bucketuser.id).exists():
            content.bookmarked_by.remove(bucketuser)
        else:
            content.bookmarked_by.add(bucketuser)
        return reverse('view_content', kwargs={'slug': content.slug})
