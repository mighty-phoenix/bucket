import random
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from users.models import BucketUser
from subjects.models import Subject, Content, List
from subjects.constants import CONTENT_TYPES


user_pks = BucketUser.objects.values_list('pk', flat=True)
subject_pks = Subject.objects.values_list('pk', flat=True)

content_urls = ['youtube', 'imdb', 'goodreads', 'instagram', 'facebook']

def generate_user(user_pks):
    pk = random.choice(user_pks)
    user = BucketUser.objects.get(pk=pk)
    return user

def generate_subject(subject_pks):
    pk = random.choice(subject_pks)
    subject = Subject.objects.get(pk=pk)
    return subject

def generate_type():
    i = len(CONTENT_TYPES)
    index = random.randint(0,i-1)
    return CONTENT_TYPES[index][0]

def generate_content_url(content_urls):
    i = len(content_urls)
    index = random.randint(0,i-1)
    content_url = 'www.' + content_urls[index] + '.com/' + get_random_string()
    return content_url


class Command(BaseCommand):
    help = 'Create random content.'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of contents to be created.')
        #parser.add_argument('file_name', type=str, help='The txt file that contains the Content titles.')

    def handle(self, *args, **kwargs):
        #file_name = kwargs['file_name']
        #with open(f'{file_name}.txt') as file:
            #for row in file:
        total = kwargs['total']
        for i in range(total):
            title = get_random_string()
            type = generate_type()
            creator = get_random_string()
            content_url = generate_content_url(content_urls)

            content = Content(
                title = title,
                type = type,
                creator = creator,
                content_url = content_url
            )
            content.save()

            subject = generate_subject(subject_pks)
            content.subject.add(subject)

            #number_of_bookmarks = random.randint(0,len(user_pks)-1)
            #for i in range(number_of_bookmarks):
            #    user_bookmarked = generate_user(user_pks)
            #    bookmarks = content.bookmarked_by.all()
            #    while not user_bookmarked in bookmarks:
            #        user_bookmarked = generate_user(user_pks)
            #    content.bookmarked_by.add(user_bookmarked)
