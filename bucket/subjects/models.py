from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from bucket.settings import base
from subjects.constants import CONTENT_TYPES


class Subject(models.Model):
    """Model to store information about a Subject"""
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Content(models.Model):
    """Model to store content related to a subject"""
    subject = models.ManyToManyField(Subject)
    title = models.CharField(max_length=255, unique=True, verbose_name="Title")
    type = models.CharField(max_length=20, choices=CONTENT_TYPES, \
                            default='other', verbose_name="Content Type")
    creator = models.CharField(max_length=255, blank=True, verbose_name="Creator")
    image = models.ImageField(upload_to='content_images',
                              blank=True,
                              null=True,
                              verbose_name="Image")
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(100, 150)],
                                     options={'quality': 100})
    description = models.TextField(blank=True, verbose_name="Description")
    link = models.URLField(blank=True, verbose_name="Link")

    def __str__(self):
        return self.title
