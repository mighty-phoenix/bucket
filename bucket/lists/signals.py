from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from lists.models import List
from subjects.models import Content


@receiver(m2m_changed, sender=List.content.through,
          dispatch_uid="update_list_image_on_add")
def update_list_image_on_add(sender, **kwargs):
    """Update list image when content is added"""
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    if action == "post_add":
        content = Content.objects.get(pk=list(pk_set)[0])
        if content.image:
            instance.image = content.image
            instance.save()


@receiver(m2m_changed, sender=List.content.through,
          dispatch_uid="update_list_image_on_remove")
def update_list_image_on_remove(sender, **kwargs):
    """Update list image when content is removed"""
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    if action == "post_remove" and len(instance.content.all()) != 0:
        content = Content.objects.get(pk=list(pk_set)[0])
        if instance.image == content.image or not instance.image:
            list_content = instance.content.all()[0]
            instance.image = list_content.image
            instance.save()
