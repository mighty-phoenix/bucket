from django.core.management.base import BaseCommand
from django.utils.text import slugify
from subjects.models import Subject


class Command(BaseCommand):
    help = 'Update and add slug field to all subjects.'

    def handle(self, *args, **kwargs):
        all = Subject.objects.all()
        for subject in all:
            subject.slug = slugify(subject.name)
            subject.save()
