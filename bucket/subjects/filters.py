import django_filters
from django import forms
from django.shortcuts import get_object_or_404

from subjects.constants import media_types
from subjects.models import Content
from common.models import Tag, Topic
from users.models import BucketUser


class ContentFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}), max_length=150)
    type = django_filters.MultipleChoiceFilter(label='', choices=media_types,
        widget=forms.CheckboxSelectMultiple)
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    topics = django_filters.ModelMultipleChoiceFilter(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Content
        fields = ['title', 'type', 'tags', 'topics', ]


class ContentBookmarkFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}), max_length=150)
    type = django_filters.MultipleChoiceFilter(label='', choices=media_types,
        widget=forms.CheckboxSelectMultiple)
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    topics = django_filters.ModelMultipleChoiceFilter(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Content
        fields = ['title', 'type', 'tags', 'topics', ]

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        bucketuser = BucketUser.objects.get(user=user)

        return parent.filter(bookmarked_by=bucketuser)


class ContentTagFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}), max_length=150)
    type = django_filters.MultipleChoiceFilter(label='', choices=media_types,
        widget=forms.CheckboxSelectMultiple)
    topics = django_filters.ModelMultipleChoiceFilter(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Content
        fields = ['title', 'type', 'topics', ]

    @property
    def qs(self):
        parent = super().qs
        slug = self.request.get_full_path().split('/')[2]
        tag = get_object_or_404(Tag, slug=slug)

        return parent.filter(tags=tag)


class ContentTopicFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label='', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search'}), max_length=150)
    type = django_filters.MultipleChoiceFilter(label='', choices=media_types,
        widget=forms.CheckboxSelectMultiple)
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Content
        fields = ['title', 'type', 'tags', ]

    @property
    def qs(self):
        parent = super().qs
        slug = self.request.get_full_path().split('/')[2]
        topic = get_object_or_404(Topic, slug=slug)

        return parent.filter(topics=topic)
