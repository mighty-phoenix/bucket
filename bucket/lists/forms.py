from django import forms

from common.forms import ModelFormWithHelper
from common.helpers import SubmitCancelFormHelper
from lists.models import List


class AddListForm(ModelFormWithHelper):
    """Form to create a List."""
    class Meta:
        model = List
        fields = ('name', 'description', 'topics')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'contents_page' %}"


class EditListForm(ModelFormWithHelper):
    """Form to edit a list."""
    class Meta:
        model = List
        fields = ('name', 'description', 'topics', 'visibility')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_list' list.slug %}"


class AddContentToListForm(ModelFormWithHelper):
    """Form to add content to a list.

    # TODO: Remove existing list contents from form options
    """
    class Meta:
        model = List
        fields = ('content', )
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_list' list.slug %}"
