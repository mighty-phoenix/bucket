from django import forms
import django_filters

from subjects.constants import CONTENT_TYPES
from subjects.models import Content
from users.models import BucketUser


class ContentFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label='', lookup_expr='icontains')
    type = django_filters.MultipleChoiceFilter(label='', choices=CONTENT_TYPES,
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Content
        fields = ['type', 'title', ]


class ContentBookmarkFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label='', lookup_expr='icontains')
    type = django_filters.MultipleChoiceFilter(label='', choices=CONTENT_TYPES,
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Content
        fields = ['type', 'title', ]

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        bucketuser = BucketUser.objects.get(user=user)

        return parent.filter(bookmarked_by=bucketuser)
