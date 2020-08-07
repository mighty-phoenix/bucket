from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from paths.models import Path
from subjects.models import Content


@receiver(m2m_changed, sender=Path.content.through,
          dispatch_uid="update_path_image_on_add")
def update_path_image_on_add(sender, **kwargs):
    """Update path image when content is added"""
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    if action == "post_add":
        content = Content.objects.get(pk=list(pk_set)[0])
        if content.image:
            instance.image = content.image
            instance.save()


@receiver(m2m_changed, sender=Path.content.through,
          dispatch_uid="update_path_image_on_remove")
def update_path_image_on_remove(sender, **kwargs):
    """Update path image when content is removed"""
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    if action == "post_remove" and len(instance.content.all()) != 0:
        content = Content.objects.get(pk=list(pk_set)[0])
        if instance.image == content.image or not instance.image:
            content = instance.content.all()[0]
            instance.image = content.image
            instance.save()
