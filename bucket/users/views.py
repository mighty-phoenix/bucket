from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from braces.views import LoginRequiredMixin, MultiplePermissionsRequiredMixin
from django_filters.views import FilterView

from subjects.filters import ContentBookmarkFilter
from subjects.models import Content
from users.mixins import UserMixin
from users.forms import UserForm
from users.models import BucketUser
from lists.views import ViewList
from lists.models import List


class UserView(LoginRequiredMixin, TemplateView):
    """User view"""
    template_name = "users/view_profile.html"

    def get_context_data(self, **kwargs):
        """Supply additional context data for the template"""
        context = super(UserView, self).get_context_data(**kwargs)
        username = context['username']
        bucketuser = get_object_or_404(BucketUser, user__username=username)
        context['bucketuser'] = bucketuser
        context['bookmarked_lists'] = bucketuser.list_bookmark.all()
        # If viewing aanother user's profile, show only public lists
        request_bucketuser = get_object_or_404(BucketUser, user=self.request.user)
        if request_bucketuser == bucketuser:
            context['user_lists'] = bucketuser.list_set.all()
        else:
            context['user_lists'] = bucketuser.list_set.filter(visibility='public')
        return context


class UserProfileView(LoginRequiredMixin, MultiplePermissionsRequiredMixin,
                      UpdateView):
    """User profile update view"""
    template_name = "users/edit_profile.html"
    form_class = UserForm
    model = User
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        """Override dispatch method to add to the view User and BucketUser
        objects, of which the profile is displayed."""
        username = kwargs.get('username')
        self.user = get_object_or_404(User, username=username)
        self.bucketuser = get_object_or_404(BucketUser, user=self.user)
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Get form instance"""
        return self.user

    def get_context_data(self, **kwargs):
        """Supply additional context data for the template"""
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['bucketuser'] = self.bucketuser
        return context

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return self.bucketuser.get_absolute_url()

    def check_permissions(self, request):
        """Check if the request user has any of those permissions:

        * is a superuser
        * is the owner of the profile (can edit it's own profile)
        """
        permissions = []
        permissions.extend([request.user.is_superuser])
        permissions.extend([request.user == self.user])
        return any(permissions)


#https://stackoverflow.com/questions/35796195/how-to-redirect-to-previous-page-in-django-after-post-request
class BookmarkContentView(LoginRequiredMixin, RedirectView):
    """Bookmark content"""
    model = BucketUser

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        bucketuser = get_object_or_404(BucketUser, user=user)
        content = get_object_or_404(Content, slug=self.kwargs['slug'])
        if content in bucketuser.content_bookmark.all():
            bucketuser.content_bookmark.remove(content)
        else:
            bucketuser.content_bookmark.add(content)
        return self.request.GET.get('next', reverse('view_content', kwargs={'slug': content.slug}))


class AllBookmarksView(LoginRequiredMixin, ViewList):
    """View list of all bookmarks"""
    model = List
    template_name = "lists/list.html"

    def get_object(self, queryset=None):
        user = self.request.user
        bucketuser = get_object_or_404(BucketUser, user=user)
        try:
            self.object = List.objects.get(user=bucketuser, name='Bookmarks')
        except List.DoesNotExist:
            self.object = List.objects.create(user=bucketuser, name='Bookmarks')
        return self.object
