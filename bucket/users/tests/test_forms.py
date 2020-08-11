from django.contrib.auth.models import User
from django.test import TestCase

from users.forms import UserForm, BucketUserForm
from users.models import BucketUser


class UserFormsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.bucket_user = BucketUser.objects.get(user=self.user)

    def test_user_form(self):
        """Test the combined User and BucketUser form"""
        form = UserForm(instance=self.user)
        self.assertEqual(type(form.bucket_user_form), BucketUserForm)
        data = {'first_name': 'Foo',
                'last_name': 'Bar',
                'bio': 'about me'}
        form = UserForm(data=data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.user.first_name, 'Foo')
        self.assertEqual(self.user.last_name, 'Bar')
        bucket_user = BucketUser.objects.get(user=self.user)
        self.assertEqual(bucket_user.bio, 'about me')
