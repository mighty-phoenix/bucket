from django import forms

from common.forms import ModelFormWithHelper
from common.helpers import SubmitCancelFormHelper
from lists.models import List


class AddListForm(ModelFormWithHelper):
    """Form to create a List."""
    class Meta:
        model = List
        fields = ('name', 'description', 'content', 'tags')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'contents_page' %}"


class EditListForm(ModelFormWithHelper):
    """Form to edit and add content to a list."""
    class Meta:
        model = List
        fields = ('name', 'description', 'content', 'tags')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_list' list.slug %}"
