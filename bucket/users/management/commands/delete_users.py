import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from users.models import BucketUser


class Command(BaseCommand):
    help = 'Delete random users'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str, help='Usernames to delete.')


    def handle(self, *args, **kwargs):
        usernames = kwargs['username']
        for i in usernames:
            try:
                bucketuser = BucketUser.objects.get(username=i)
                bucketuser.delete()
                self.stdout.write('User "%s" deleted' % (bucketuser.username))
            except User.DoesNotExist:
                self.stdout.write('User with username "%s" does not exist.' % i)
