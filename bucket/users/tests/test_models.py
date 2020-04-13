from django.contrib.auth.models import User, Group
from django.test import TestCase

from users.models import BucketUser


class BucketUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.bucket_user = BucketUser.objects.get(user=self.user)

    def test_create_bucket_user(self):
        """Test creation of BucketUser on new User create"""
        self.assertTrue(1, BucketUser.objects.count())
        self.assertEqual(self.bucket_user.user,
                         BucketUser.objects.get(user=self.user).user)

        self.bucket_user.user.save()
        self.assertTrue(1, BucketUser.objects.count())


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')

    def test_str(self):
        """Test string representation of Django User model"""
        self.assertEqual(str(self.user), 'foo')
        self.user.first_name = "Foo"
        self.user.save()
        self.assertEqual(str(self.user), 'foo')
        self.user.last_name = "Bar"
        self.user.save()
        self.assertEqual(str(self.user), 'Foo Bar')
