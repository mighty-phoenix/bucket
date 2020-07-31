import tagulous.models
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils.crypto import get_random_string

from common.constants import visibility
from common.models import Tag, Topic
from subjects.models import Content
from users.models import BucketUser

class List(models.Model):
    """Content lists which can be created for each user."""
    user = models.ForeignKey(BucketUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, verbose_name="Name")
    slug = models.SlugField(max_length=150, unique=True, editable=False, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    content = models.ManyToManyField(Content,
                                     blank=True,
                                     related_name='content',
                                     verbose_name='Content')
    visibility = models.CharField(max_length=150,
                                  choices=visibility,
                                  default='public',
                                  verbose_name="Visibility")
    topics = tagulous.models.TagField(to=Topic, related_name='list_topic')
    list_bookmarked_by = models.ManyToManyField(BucketUser, related_name='list_bookmark')
    image = models.ImageField(upload_to='list_images',
                              blank=True,
                              null=True,
                              verbose_name="Image")
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(100, 150)],
                                     options={'quality': 100})

    class Meta:
        ordering = ['name']

    def __str__(self):
        return "{0} by {1}".format(self.name, self.user)

    def save(self, *args, **kwargs):
        self.slug = add_slug(self)
        super().save(*args, **kwargs)


# https://stackoverflow.com/questions/42429463/django-generating-random-unique-slug-field-for-each-model-object/43256732
def add_slug(obj):
    if not obj.slug: # if there isn't a slug
        obj.slug = get_random_string(8,'0123456789') # create one
        slug_is_wrong = True
        while slug_is_wrong: # keep checking until we have a valid slug
            slug_is_wrong = False
            other_objs_with_slug = type(obj).objects.filter(slug=obj.slug)
            if len(other_objs_with_slug) > 0:
                # if any other objects have current slug
                slug_is_wrong = True
            if slug_is_wrong:
                # create another slug and check it again
                obj.slug = get_random_string(8,'0123456789')
    return obj.slug
