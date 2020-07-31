import django_filters
from django import forms
from django.contrib.auth.models import User

from lists.models import List
from common.models import Topic
from users.models import BucketUser


class ListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    topics = django_filters.ModelMultipleChoiceFilter(queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = List
        fields = ['name', 'topics', ]

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(visibility='public').exclude(name='Bookmarks').exclude(name='Recommendations')


class UserListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    topics = django_filters.ModelMultipleChoiceFilter(queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = List
        fields = ['name', 'topics', ]

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        username = self.request.get_full_path().split('/')[2]
        list_user = User.objects.get(username=username)
        list_bucketuser = BucketUser.objects.get(user=list_user)

        # if viewing another user's lists, include only public lists
        if user == list_user:
            return parent.filter(user=list_bucketuser)
        else:
            return parent.filter(user=list_bucketuser, visibility='public')


class ListBookmarkFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    topics = django_filters.ModelMultipleChoiceFilter(queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = List
        fields = ['name', 'topics', ]

    @property
    def qs(self):
        parent = super().qs
        username = self.request.get_full_path().split('/')[2]
        user = User.objects.get(username=username)
        bucketuser = BucketUser.objects.get(user=user)

        return parent.filter(list_bookmarked_by=bucketuser)
