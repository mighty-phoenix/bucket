from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files import File

from lists.models import List
from subjects.models import Content
from users.models import BucketUser


class ListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.bucketuser = BucketUser.objects.get(user=self.user)
        self.content = Content.objects.create(title="Test Content")
        self.list = List.objects.create(
            user=self.bucketuser,
            name="Test List",
            description="Testing for lists models.",
            image=File(file=b""),
            visibility="public",
            topics=['History', 'Philosophy']
        )
        self.list.content.add(self.content)
        self.list.list_bookmarked_by.add(self.bucketuser)


    def test_str(self):
        """Test List object str/unicode representation"""
        self.assertEqual(str(self.list), "Test List by foo")
