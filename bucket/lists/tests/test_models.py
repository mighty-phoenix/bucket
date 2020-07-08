from django.test import TestCase
from django.contrib.auth.models import User

from lists.models import List
from users.models import BucketUser


class ListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.bucketuser = BucketUser.objects.get(user=self.user)
        self.list = List.objects.create(user=self.bucketuser,
                                        name="Test List")

    def test_str(self):
        """Test List object str/unicode representation"""
        self.assertEqual(str(self.list), "Test List")
