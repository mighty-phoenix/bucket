from django.db import models


class Subject(models.Model):
    """Model to store information about a Subject"""
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Slug")
    books = models.TextField(verbose_name="Books")
    movies = models.TextField(verbose_name="Movies")
    docs = models.TextField(verbose_name="Documentaries")
    yt_channels = models.TextField(verbose_name="Youtube Channels")
    websites = models.TextField(verbose_name="Websites")
    fb_pages = models.TextField(verbose_name="Facebook Pages")
    insta_pages = models.TextField(verbose_name="Instagram Pages") 

    def __str__(self):
        return self.name
