from django.db import models


class Subject(models.Model):
    """Model to store information about a Subject"""
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Slug")
    #books = models.TextField(verbose_name="Books")
    #movies = models.TextField(verbose_name="Movies")
    #docs = models.TextField(verbose_name="Documentaries")
    #yt_channels = models.TextField(verbose_name="Youtube Channels")
    #websites = models.TextField(verbose_name="Websites")
    #fb_pages = models.TextField(verbose_name="Facebook Pages")
    #insta_pages = models.TextField(verbose_name="Instagram Pages")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Content(models.Model):
    """Model to store content related to a subject"""
    subject = models.ManyToManyField(Subject)
    title = models.CharField(max_length=255, unique=True, verbose_name="Title")
    CONTENT_TYPE_CHOICES = [
        ('book', 'Book'),
        ('movie', 'Movie'),
        ('doc', 'Documentary'),
        ('website', 'Website'),
        ('yt_channel', 'Youtube Channel'),
        ('social_media', 'Social Media'),
        ('other', 'Other'),
    ]
    type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, \
                            default='other', verbose_name="Content Type")
    creator = models.CharField(max_length=255, blank=True, verbose_name="Creator")
    description = models.TextField(blank=True, verbose_name="Description")
    link = models.URLField(blank=True, verbose_name="Link")

    def __str__(self):
        return self.title
