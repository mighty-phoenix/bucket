from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django_filters.views import FilterView

from paths.forms import AddPathForm, EditPathForm, AddContentToPathForm
from paths.filters import PathFilter, UserPathFilter
from paths.models import Path, PathContent
from subjects.models import Content
from users.mixins import UserMixin
from users.models import BucketUser


class PathsPage(UserMixin, FilterView):
    """Show all paths"""
    model = Path
    template_name = "paths/paths_page.html"
    filterset_class = PathFilter
    #paginate_by = 10


class ViewPath(UserMixin, DetailView):
    """View all content in a path."""
    model = Path
    template_name = "paths/path.html"

    def get_context_data(self, **kwargs):
        context = super(ViewPath, self).get_context_data(**kwargs)
        context['path'] = self.object
        context['path_user'] = self.object.user
        path_content = PathContent.objects.filter(path=self.object)
        context['path_content'] = path_content
        context['number_of_items'] = path_content.count()
        number_completed = PathContent.objects.filter(path=self.object,
            completed=True).count()
        number_total = path_content.count()
        if number_total > 0:
            context['percent_complete'] = number_completed*100.0 / number_total
        return context


class AddPathView(LoginRequiredMixin, CreateView):
    """Create a new Path"""
    model = Path
    template_name = "paths/add_path.html"
    form_class = AddPathForm

    def get_success_url(self):
        """Redirect to path page."""
        messages.add_message(self.request, messages.SUCCESS, "Path created")
        return reverse("view_path", kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        """Add user to the instance."""
        bucketuser = get_object_or_404(BucketUser, user=self.request.user)
        form.instance.user = bucketuser
        return super().form_valid(form)


class EditPathView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Update a path."""
    model = Path
    template_name = "paths/edit_path.html"
    form_class = EditPathForm
    raise_exception = True

    def get_success_url(self):
        """Redirect to path page."""
        messages.add_message(self.request, messages.INFO, "Path updated")
        return reverse("view_path", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add user to the context."""
        context = super(EditPathView, self).get_context_data(**kwargs)
        bucketuser = get_object_or_404(BucketUser, user=self.request.user)
        context['user'] = bucketuser
        return context

    def check_permissions(self, request):
        """Check if the request user has the permission to edit the path."""
        self.path = get_object_or_404(Path, slug=self.kwargs['slug'])
        bucketuser = get_object_or_404(BucketUser, user=request.user)
        return bucketuser == self.path.user


class DeletePathView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete a path."""
    model = Path
    template_name = "paths/confirm_delete_path.html"
    raise_exception = True

    def get_success_url(self):
        """Redirect to user profile in case of successful deletion"""
        messages.add_message(self.request, messages.WARNING, "Path deleted")
        return reverse("all_user_paths")

    def check_permissions(self, request):
        """Check if the request user has the permission to delete the path."""
        self.path = get_object_or_404(Path, slug=self.kwargs['slug'])
        bucketuser = get_object_or_404(BucketUser, user=request.user)
        return bucketuser == self.path.user


class AllUserPathsView(LoginRequiredMixin, FilterView):
    """View all paths created by the user."""
    model = Path
    template_name = "paths/all_user_paths.html"
    filterset_class = UserPathFilter
    #paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(AllUserPathsView, self).get_context_data(**kwargs)
        path_user = get_object_or_404(User, username=self.kwargs['username'])
        context['path_user'] = get_object_or_404(BucketUser, user=path_user)
        context['bucketuser'] = get_object_or_404(BucketUser,
                                                  user=self.request.user)
        return context


class AddToPathView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Add a content to a user path from the path's page

    # TODO: Remove existing path contents from form options
    """
    model = Path
    template_name = "paths/add_to_path.html"
    form_class = AddContentToPathForm

    def get_success_url(self):
        """Redirect to path page."""
        messages.add_message(self.request, messages.INFO, "Path updated")
        return reverse("view_path", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(AddToPathView, self).get_context_data(**kwargs)
        path = get_object_or_404(Path, slug=self.kwargs['slug'])
        context['path_contents'] = path.content.all()
        return context

    def check_permissions(self, request):
        """Check if the request user has the permission to edit the path."""
        path = get_object_or_404(Path, slug=self.kwargs['slug'])
        bucketuser = get_object_or_404(BucketUser, user=request.user)
        return bucketuser == path.user


class RemoveContentFromPathView(LoginRequiredMixin, PermissionRequiredMixin,
                                RedirectView):
    """Remove content from path"""
    model = Path

    def get_redirect_url(self, *args, **kwargs):
        path = get_object_or_404(Path, slug=self.kwargs['slug'])
        content = get_object_or_404(Content, slug=self.kwargs['content_slug'])
        path.content.remove(content)
        return self.request.GET.get('next', reverse('view_path',
            kwargs={'slug': path.slug}))

    def check_permissions(self, request):
        """Check if the request user has the permission to remove content
        from the path."""
        path = get_object_or_404(Path, slug=self.kwargs['slug'])
        bucketuser = get_object_or_404(BucketUser, user=request.user)
        return bucketuser == path.user


class MarkCompletedView(LoginRequiredMixin, PermissionRequiredMixin,
                        RedirectView):
    """Mark path content as completed"""
    model = Path

    def get_redirect_url(self, *args, **kwargs):
        path = Path.objects.get(slug=self.kwargs['slug'])
        content = get_object_or_404(Content, slug=self.kwargs['content_slug'])
        path_content = PathContent.objects.get(path=path, content=content)
        if path_content.completed:
            path_content.completed = False
        else:
            path_content.completed = True
        path_content.save()
        return self.request.GET.get('next', reverse('view_path',
            kwargs={'slug': path.slug}))

    def check_permissions(self, request):
        """Check if the request user has the permission to mark path content
        as completed."""
        self.path = get_object_or_404(Path, slug=self.kwargs['slug'])
        bucketuser = get_object_or_404(BucketUser, user=request.user)
        return bucketuser == self.path.user
