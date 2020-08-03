from django.shortcuts import get_object_or_404
from django.views.generic.base import ContextMixin

from lists.models import List
from users.models import BucketUser


class UserListsMixin(ContextMixin):
    """Add bucketuser and user lists to context"""

    def get_context_data(self, **kwargs):
        context = super(UserListsMixin, self).get_context_data(**kwargs)
        context['user_lists'] = []
        if self.request.user.is_authenticated:
            user = self.request.user
            bucketuser = get_object_or_404(BucketUser, user=user)
            context['bucketuser'] = bucketuser
            context['user_lists'] = List.objects.filter(user=bucketuser).exclude(name='Bookmarks')
        return context


class UserMixin(ContextMixin):
    """Add bucketuser to context"""

    def get_context_data(self, **kwargs):
        context = super(UserMixin, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            context['bucketuser'] = get_object_or_404(BucketUser, user=user)
        return context
