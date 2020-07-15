import django_filters
from django import forms

from lists.models import List
from common.models import Tag
from users.models import BucketUser


class ListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = List
        fields = ['name', 'tags', ]


class UserListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = List
        fields = ['name', 'tags', ]

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        bucketuser = BucketUser.objects.get(user=user)

        return parent.filter(user=bucketuser)


class ListBookmarkFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = List
        fields = ['name', 'tags', ]

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        bucketuser = BucketUser.objects.get(user=user)

        return parent.filter(bookmarked_by=bucketuser)
