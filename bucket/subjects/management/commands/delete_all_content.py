from django.core.management.base import BaseCommand
from subjects.models import Content


class Command(BaseCommand):
    help = 'Delete all Content.'

    def handle(self, *args, **kwargs):
        all = Content.objects.all()
        for content in all:
            content.delete()
