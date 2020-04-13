from django.test import TestCase

from common.templatetags.verbose_name import verbose_name
from users.models import BucketUser


class TemplateTagsTestCase(TestCase):
    def test_verbose_names(self):
        """Test verbose_name template tag"""
        self.assertEqual(verbose_name(BucketUser, "homepage_url"), "Homepage")
