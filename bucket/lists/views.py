from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django_filters.views import FilterView

from lists.forms import AddListForm, EditListForm
from lists.filters import ListFilter, UserListFilter, ListBookmarkFilter
from lists.models import List
from subjects.models import Content
from users.models import BucketUser


class ListsPage(FilterView):
    """Show all lists"""
    model = List
    template_name = "lists/lists_page.html"
    filterset_class = ListFilter
    #paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(FilterView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            context['bucketuser'] = get_object_or_404(BucketUser, user=user)
        return context


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
        if self.request.user.is_authenticated:
            user = self.request.user
            bucketuser = get_object_or_404(BucketUser, user=user)
            context['bucketuser'] = bucketuser
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


class EditListView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Update a list."""
    model = List
    template_name = "lists/edit_list.html"
    form_class = EditListForm
    raise_exception = True

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

    def check_permissions(self, request):
        """Check if the request user has the permission to edit the list."""
        self.list = get_object_or_404(List, slug=self.kwargs['slug'])
        bucketuser = get_object_or_404(BucketUser, user=request.user)
        return bucketuser == self.list.user


class DeleteListView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete a list."""
    model = List
    template_name = "lists/confirm_delete_list.html"
    raise_exception = True

    def get_success_url(self):
        """Redirect to user profile in case of successful deletion"""
        messages.add_message(self.request, messages.WARNING, "List deleted")
        return reverse("all_user_lists")

    def check_permissions(self, request):
        """Check if the request user has the permission to delete the list."""
        self.list = get_object_or_404(List, slug=self.kwargs['slug'])
        bucketuser = get_object_or_404(BucketUser, user=request.user)
        return bucketuser == self.list.user


class BookmarkListView(LoginRequiredMixin, RedirectView):
    """Bookmark a list"""
    model = List
    template_name = "lists/bookmark.html"

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        bucketuser = get_object_or_404(BucketUser, user=user)
        list = get_object_or_404(List, slug=self.kwargs['slug'])
        if bucketuser in list.bookmarked_by.all():
            list.bookmarked_by.remove(bucketuser)
        else:
            list.bookmarked_by.add(bucketuser)
        return self.request.GET.get('next', reverse('view_list', kwargs={'slug': list.slug}))


class AllUserListsView(LoginRequiredMixin, FilterView):
    """View all lists created by the user."""
    model = List
    template_name = "lists/all_user_lists.html"
    filterset_class = UserListFilter
    #paginate_by = 10


class AllBookmarkedListsView(LoginRequiredMixin, FilterView):
    """View all lists bookmarked by the user."""
    model = List
    template_name = "lists/all_bookmarked_lists.html"
    filterset_class = ListBookmarkFilter
    #paginate_by = 10


class AddToListView(LoginRequiredMixin, RedirectView):
    """Add a content to a user list"""
    model = List
    template_name = "lists/add_to_list.html"

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        bucketuser = get_object_or_404(BucketUser, user=user)
        list = List.objects.get(slug=self.kwargs['slug'], user=bucketuser)
        content = get_object_or_404(Content, slug=self.kwargs['content_slug'])
        if content in list.content.all():
            list.content.remove(content)
        else:
            list.content.add(content)
        return self.request.GET.get('next', reverse('view_list', kwargs={'slug': list.slug}))
