from django.db import models
import tagulous.models
from django.urls import reverse


class Tags(tagulous.models.TagModel):
    class TagMeta:
        # Tag options
        initial = "technology, entrepreneurship, self-development, self-growth"
        force_lowercase = True

    def get_absolute_url(self):
        """Absolute URL to a Tag object"""
        return reverse('view_tag', kwargs={'slug': self.slug})
