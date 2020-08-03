from django import forms

from common.forms import ModelFormWithHelper
from common.helpers import SubmitCancelFormHelper
from paths.models import Path


class AddPathForm(ModelFormWithHelper):
    """Form to create a Path."""
    class Meta:
        model = Path
        fields = ('goal', 'description', 'topics')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'contents_page' %}"


class EditPathForm(ModelFormWithHelper):
    """Form to edit a path."""
    class Meta:
        model = Path
        fields = ('goal', 'description', 'topics', 'visibility')
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_path' path.slug %}"


class AddContentToPathForm(ModelFormWithHelper):
    """Form to add content to a path.

    # TODO: Remove existing path contents from form options
    """
    class Meta:
        model = Path
        fields = ('content', )
        helper_class = SubmitCancelFormHelper
        helper_cancel_href = "{% url 'view_path' path.slug %}"
