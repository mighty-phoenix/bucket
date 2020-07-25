from django.db import models
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from urllib.parse import urlparse
import tagulous.models

from subjects.constants import media_types
from common.models import Tag, Topic
from users.models import BucketUser


class Subject(models.Model):
    """Model to store information about a Subject"""
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=150, unique=True, editable=False, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Content(models.Model):
    """Model to store content related to a subject"""
    subject = models.ManyToManyField(Subject, blank=True, related_name='content')
    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=150, unique=True, editable=False, verbose_name="Slug")
    url = models.URLField(blank=True, null=True, default='', verbose_name="URL")
    type = models.CharField(max_length=150,
                            choices=media_types,
                            default='other',
                            verbose_name="Type")
    creator = models.CharField(max_length=255, blank=True, verbose_name="Creator")
    image = models.ImageField(upload_to='content_images',
                              blank=True,
                              null=True,
                              verbose_name="Image")
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(100, 150)],
                                     options={'quality': 100})
    description = models.TextField(blank=True, verbose_name="Description")
    bookmarked_by = models.ManyToManyField(BucketUser,
                                           blank=True,
                                           related_name='content_bookmark',
                                           verbose_name='Bookmarked By')
    tags = tagulous.models.TagField(to=Tag, related_name='content_tag')
    topics = tagulous.models.TagField(to=Topic, related_name='topic')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def url_text(self):
        if self.content_url and '//' not in self.content_url:
            self.content_url = '%s%s' % ('https://', self.content_url)
        parsed_url = urlparse(self.content_url)
        if parsed_url.hostname:
            return parsed_url.hostname.replace("www.", "") + "/..."
        else:
            return ""
