from django import forms

from common.forms import ModelFormWithHelper
from common.helpers import SubmitCancelFormHelper
from subjects.constants import media_types, movie_genres, tv_genres
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
        fields = ('title', 'type', 'description', 'url', 'tags', 'topics')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'contents_page' %}"


class EditContentForm(ModelFormWithHelper):
    """Form to edit details of a Content."""
    class Meta:
        model = Content
        fields = ('title', 'type', 'description', 'url', 'tags', 'topics')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_content' content.slug %}"


class SearchExternalDataForm(forms.Form):
    global_search = forms.CharField(label='', required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    media_type = forms.ChoiceField(label='', choices=media_types)


class SearchMovies(forms.Form):
    search = forms.CharField(label='', required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    genre = forms.MultipleChoiceField(label='', choices=list(movie_genres.items()),
        widget=forms.CheckboxSelectMultiple)


class SearchTVShows(forms.Form):
    search = forms.CharField(label='', required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    genre = forms.MultipleChoiceField(label='', choices=list(tv_genres.items()),
        widget=forms.CheckboxSelectMultiple)


class SearchBooks(forms.Form):
    search = forms.CharField(label='', required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))


class SearchYoutube(forms.Form):
    search = forms.CharField(label='', required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
