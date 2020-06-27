import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from users.models import BucketUser


first_names = ['Jiwon', 'Seojoon', 'Minhyuk', 'Joongki', 'Minho', 'Changwook', 'Jongsuk', 'Hyunksik', 'Shinhye', 'Hyekyo', 'Boyoung', 'Taehee']
last_names = ['Kim', 'Choi', 'Park', 'Song', 'Lee', 'Ji', 'Ha', 'Shin', 'Han', 'Son', 'Jang']

def generate_name(name_list):
    i = len(name_list)
    index = random.randint(0,i-1)
    return name_list[index]


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created.')
        #parser.add_argument('first_names'), type=str, help='A txt file that contains a list of first names.')
        #parser.add_argument('last_names'), type=str, help='A txt file that contains a list of last names.')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            first_name = generate_name(first_names)
            last_name = generate_name(last_names)
            username = first_name.lower() + '_' + last_name.lower()
            while User.objects.filter(username=username).exists():
                first_name = generate_name(first_names)
                last_name = generate_name(last_names)
                username = first_name.lower() + '_' + last_name.lower()
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=first_name.lower() + last_name.lower() + '@dc.com',
                password='123')
            bucketuser = BucketUser.objects.get(user=user)
            bucketuser.bio = get_random_string()
            bucketuser.save()
