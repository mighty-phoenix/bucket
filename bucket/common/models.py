import tagulous.models
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from subjects.constants import movie_genres, tv_genres, topics
from common.constants import status, visibility
from users.models import BucketUser


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


class Bookmark(models.Model):
    user = models.ForeignKey(BucketUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date added')
    status = models.CharField(max_length=150,
                              choices=status,
                              default='completed',
                              verbose_name="Status")
    notes = models.TextField(blank=True, verbose_name="Notes")
    visibility = models.CharField(max_length=150,
                                  choices=visibility,
                                  default='public',
                                  verbose_name="Visibility")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
