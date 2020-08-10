import django_filters
from django import forms
from django.db.models import Count
from django.contrib.auth.models import User

from paths.models import Path
from common.models import Topic
from users.models import BucketUser


class PathFilter(django_filters.FilterSet):
    goal = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}), max_length=150)
    topics = django_filters.ModelMultipleChoiceFilter(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Path
        fields = ['goal', 'topics', ]

    @property
    def qs(self):
        parent = super().qs
        qs = parent.filter(visibility='public')
        #qs = qs.annotate(num_bookmarks=Count('list_bookmarked_by')).order_by('num_bookmarks')

        return qs


class UserPathFilter(django_filters.FilterSet):
    goal = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}), max_length=150)
    topics = django_filters.ModelMultipleChoiceFilter(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Path
        fields = ['goal', 'topics', ]

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        username = self.request.get_full_path().split('/')[2]
        path_user = User.objects.get(username=username)
        path_bucketuser = BucketUser.objects.get(user=path_user)
        # if viewing another user's paths, include only public paths
        if user == path_user:
            qs = parent.filter(user=path_bucketuser)
        else:
            qs = parent.filter(user=path_bucketuser, visibility='public')
        #qs = qs.annotate(num_bookmarks=Count('list_bookmarked_by')).order_by('num_bookmarks')

        return qs
