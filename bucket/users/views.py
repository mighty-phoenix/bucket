from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from braces.views import LoginRequiredMixin, MultiplePermissionsRequiredMixin

from users.forms import UserForm
from users.models import BucketUser


class UserView(LoginRequiredMixin, TemplateView):
    """User view"""
    template_name = "users/view_profile.html"

    def get_context_data(self, **kwargs):
        """Supply additional context data for the template"""
        context = super(UserView, self).get_context_data(**kwargs)
        username = context['username']
        context['bucketuser'] = get_object_or_404(BucketUser, user__username=username)
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
