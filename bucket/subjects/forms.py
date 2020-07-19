from django import forms

from common.forms import ModelFormWithHelper
from common.helpers import SubmitCancelFormHelper
from subjects.constants import movie_genres
from subjects.models import Subject, Content
from users.models import BucketUser


class AddSubjectForm(ModelFormWithHelper):
    """Form to add new Subject."""
    class Meta:
        model = Subject
        fields = ('name', 'description')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'list_subjects' %}"


class EditSubjectForm(ModelFormWithHelper):
    """Form to edit Subject"""
    class Meta:
        model = Subject
        fields = ('name', 'description')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_subject' subject.slug %}"


class AddContentForm(ModelFormWithHelper):
    """Form to add new Content."""
    class Meta:
        model = Content
        fields = ('title', 'type', 'creator', 'content_url', 'tags')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'contents_page' %}"


class EditContentForm(ModelFormWithHelper):
    """Form to edit details of a Content."""
    class Meta:
        model = Content
        fields = ('title', 'type', 'creator', 'content_url', 'tags')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_content' content.slug %}"


class SearchMovies(forms.Form):
    search = forms.CharField(label='', required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    genre = forms.MultipleChoiceField(label='', choices=list(movie_genres.items()),
        widget=forms.CheckboxSelectMultiple)
