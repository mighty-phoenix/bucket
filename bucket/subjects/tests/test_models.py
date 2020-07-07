from django.test import TestCase
from django.contrib.auth.models import User

from subjects.constants import CONTENT_TYPES
from subjects.models import Subject, Content
from users.models import BucketUser

class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='foo', password='foobar')
        self.bucketuser = BucketUser.objects.get(user=self.user)
        self.subject = Subject.objects.create(name="Test Subject",
                                              description="This is a test subject.")
        self.content = Content.objects.create(title="Test Content",
                                              type=CONTENT_TYPES[2],
                                              creator="Foo Bar",
                                              description="Test content description, this is.")
        self.content.subject.add(self.subject)
        self.content.bookmarked_by.add(self.bucketuser)


class SubjectTestCase(BaseTestCase, TestCase):
    def test_str(self):
        """Test Subject object str/unicode representation"""
        self.assertEqual(str(self.subject), "Test Subject")

    def test_slug(self):
        """Test Subject slug"""
        self.assertEqual(self.subject.slug, "test-subject")


class ContentTestCase(BaseTestCase, TestCase):
    def test_str(self):
        """Test Content object str/unicode representation"""
        self.assertEqual(str(self.content), "Test Content")

    def test_slug(self):
        """Test Content slug"""
        self.assertEqual(self.content.slug, "test-content")

    def test_url_text(self):
        """Test the representation of content url"""
        self.assertEqual(self.content.url_text(), "")
        self.content.content_url = "https://www.foobar.com/cool"
        self.assertEqual(self.content.url_text(), "foobar.com/...")
        self.content.content_url = "www.foobar.com/cool"
        self.assertEqual(self.content.url_text(), "foobar.com/...")
        self.content.content_url = "foobar.com/cool"
        self.assertEqual(self.content.url_text(), "foobar.com/...")
        self.content.content_url = ""
        self.assertEqual(self.content.url_text(), "")
