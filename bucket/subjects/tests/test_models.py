from django.test import TestCase

from subjects.models import Subject


class SubjectTestCase(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Test Subject", slug="baz",
                                              books="Foo, Bar", movies="Bar, Foo",
                                              docs="doc Foo", yt_channels="FooVlogs",
                                              websites="Bar.com", fb_pages="Baz",
                                              insta_pages="Foo, Baz")

    def test_str(self):
        """Test Subject object str/unicode representation"""
        self.assertEqual(str(self.subject), "Test Subject")


