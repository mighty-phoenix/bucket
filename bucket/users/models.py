from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class BucketUser(models.Model):
    """Profile model to store additional information about a user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, verbose_name="Bio")
    profile_picture = models.ImageField(upload_to='users/pictures/',
                                        blank=True,
                                        null=True,
                                        verbose_name="Profile picture")
    profile_picture_thumbnail = ImageSpecField(source='profile_picture',
                                               processors=[ResizeToFill(100, 100)],
                                               options={'quality': 100})

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        """Absolute URL to a BucketUser object"""
        return reverse('user', kwargs={'username': self.user.username})


def user_str(self):
    """String representation of Django User model

    :return: string User name
    """
    firstname = self.first_name
    lastname = self.last_name
    if firstname and lastname:
        return "{0} {1}".format(firstname, lastname)
    else:
        return self.username


# Overriding the string representation of Django User model
User.__str__ = user_str


@receiver(post_save, sender=User)
def create_bucket_user(sender, instance, created, **kwargs):
    """Keep User and BucketUser synchronized. Create a BucketUser instance on
    receiving a signal about new user signup.
    """
    if created:
        if instance is not None:
            bucket_user = BucketUser(user=instance)
            bucket_user.save()
