from django.core.management.base import BaseCommand
from subjects.models import Content


class Command(BaseCommand):
    help = 'Update and add slug field to all Content.'

    def handle(self, *args, **kwargs):
        all = Content.objects.all()
        for content in all:
            content.slug = content.title.replace(" ","_")
            content.save()
