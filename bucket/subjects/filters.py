import django_filters
from django import forms
from django.shortcuts import get_object_or_404

from subjects.constants import CONTENT_TYPES
from subjects.models import Content
from common.models import Tags
from users.models import BucketUser


class ContentFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    type = django_filters.MultipleChoiceFilter(label='', choices=CONTENT_TYPES,
        widget=forms.CheckboxSelectMultiple)
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tags.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Content
        fields = ['title', 'type', 'tags', ]


class ContentBookmarkFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    type = django_filters.MultipleChoiceFilter(label='', choices=CONTENT_TYPES,
        widget=forms.CheckboxSelectMultiple)
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tags.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Content
        fields = ['title', 'type', 'tags', ]

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        bucketuser = BucketUser.objects.get(user=user)

        return parent.filter(bookmarked_by=bucketuser)


class ContentTagFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    type = django_filters.MultipleChoiceFilter(label='', choices=CONTENT_TYPES,
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Content
        fields = ['title', 'type', ]

    @property
    def qs(self):
        parent = super().qs
        slug = self.request.get_full_path().split('/')[2]
        tag = get_object_or_404(Tags, slug=slug)

        return parent.filter(tags=tag)
