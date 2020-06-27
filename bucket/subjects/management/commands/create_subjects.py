from django.core.management.base import BaseCommand
from subjects.models import Subject

subjects = [
    'Mathematics', 'Economics', 'Politics', 'Literary Arts', 'Photography', 'Physics', 'Biology', 'Chemistry'
]


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for i in subjects:
            name = i
            slug = i.lower().replace(' ','_')
            if not Subject.objects.filter(slug=slug).exists():
                Subject.objects.create(name=name, slug=slug)
