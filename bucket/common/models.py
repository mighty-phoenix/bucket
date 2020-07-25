from django.db import models
import tagulous.models
from django.urls import reverse

from subjects.constants import movie_genres, tv_genres, topics


class Tag(tagulous.models.TagModel):
    class TagMeta:
        # Tag options
        initial = list(set(list(movie_genres.values()) + list(tv_genres.values())))
        force_lowercase = True

    def get_absolute_url(self):
        """Absolute URL to a Tag object"""
        return reverse('view_tag', kwargs={'slug': self.slug})


class Topic(tagulous.models.TagModel):
    class TagMeta:
        # Tag options
        initial = topics
        force_lowercase = True

    def get_absolute_url(self):
        """Absolute URL to a Topic object"""
        return reverse('view_topic', kwargs={'slug': self.slug})
