from django.test import TestCase
from django.core.files import File

from subjects.constants import media_types
from subjects.models import Subject, Content

class BaseTestCase(object):
    def setUp(self):
        self.subject = Subject.objects.create(
            name="Test Subject",
            description="This is a test subject."
        )
        self.content = Content.objects.create(
            title="Test Content",
            content_id="123456",
            type=media_types[2][0],
            image=File(file=b""),
            description="Test content description, this is.",
            tags=['Action', 'Comedy'],
            topics=['Strategy', 'Philosophy']
        )
        self.content.subject.add(self.subject)


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
        self.assertEqual(self.content.slug, "123456-test-content")

    def test_url_text(self):
        """Test the representation of content url"""
        self.assertEqual(self.content.url_text(), "")
        self.content.url = "https://www.foobar.com/cool"
        self.assertEqual(self.content.url_text(), "foobar.com/...")
        self.content.url = "www.foobar.com/cool"
        self.assertEqual(self.content.url_text(), "foobar.com/...")
        self.content.url = "foobar.com/cool"
        self.assertEqual(self.content.url_text(), "foobar.com/...")
        self.content.url = ""
        self.assertEqual(self.content.url_text(), "")
