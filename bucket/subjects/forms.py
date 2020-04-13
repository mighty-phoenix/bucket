from django import forms

from common.forms import ModelFormWithHelper
from common.helpers import SubmitCancelFormHelper
from subjects.models import Subject
from users.models import BucketUser


class AddSubjectForm(ModelFormWithHelper):
    """Form to add new Subject."""
    class Meta:
        model = Subject
        fields = ('name', 'slug', 'books', 'movies', 'docs', 'yt_channels', 'websites', 'fb_pages', 'insta_pages')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'list_subjects' %}"


class EditSubjectForm(ModelFormWithHelper):
    """Form to edit Subject"""
    class Meta:
        model = Subject
        fields = ('name', 'slug', 'books', 'movies', 'docs', 'yt_channels', 'websites', 'fb_pages', 'insta_pages')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_subject' subject.slug %}"
