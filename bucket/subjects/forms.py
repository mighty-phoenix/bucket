from django import forms

from common.forms import ModelFormWithHelper
from common.helpers import SubmitCancelFormHelper
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
        fields = ('title', 'type', 'creator', 'content_url')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'contents_page' %}"


class EditContentForm(ModelFormWithHelper):
    """Form to edit details of a Content."""
    class Meta:
        model = Content
        fields = ('title', 'type', 'creator', 'content_url')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_content' content.slug %}"
