from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver

from lists.models import List
from subjects.models import Content
from users.models import BucketUser


@receiver(post_save, sender=BucketUser, dispatch_uid="create_default_lists")
def create_default_lists(sender, instance, created, **kwargs):
    """Create default lists for BucketUser on signup"""
    if created:
        bookmarks = List.objects.create(user=instance, name='Bookmarks')
        recommendations = List.objects.create(user=instance, name='Recommendations')
        instance.save()


@receiver(m2m_changed, sender=BucketUser.content_bookmark.through,
          dispatch_uid="bookmark_content")
def bookmark_content(sender, **kwargs):
    """Add Content to Bookmarks list when content is bookmarked"""
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    if action == "pre_add":
        content = Content.objects.get(pk=list(pk_set)[0])
        try:
            bookmark_list = List.objects.get(user=instance, name='Bookmarks')
        except List.DoesNotExist:
            bookmark_list = List.objects.create(user=instance, name='Bookmarks')
        bookmark_list.content.add(content)


@receiver(m2m_changed, sender=BucketUser.content_bookmark.through,
          dispatch_uid="unbookmark_content")
def unbookmark_content(sender, **kwargs):
    """Remove Content from Bookmarks list"""
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    if action == "pre_remove":
        content = Content.objects.get(pk=list(pk_set)[0])
        bookmark_list = List.objects.get(user=instance, name='Bookmarks')
        bookmark_list.content.remove(content)


@receiver(post_delete, sender=List, dispatch_uid="delete_bookmarks_list")
def delete_bookmarks_list(sender, instance, **kwargs):
    """Remove all bookmarks of user when Bookmarks list is deleted"""
    bucketuser = instance.user
    BucketUser.content_bookmark.through.objects.filter(user=bucketuser).delete()
