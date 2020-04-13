from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client

from users.models import BucketUser


class UserViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.bucket_user = BucketUser.objects.get(user=self.user)
        self.client = Client()

    def test_user_view(self):
        """Test UserView as a logged-in user"""
        user_url = reverse('user', kwargs={
            'username': self.bucket_user.user.username})
        response = self.client.get(user_url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='foo', password='foobar')
        response = self.client.get(user_url)
        self.assertEqual(response.status_code, 200)
        nonexistent_user_url = reverse('user', kwargs={'username': 'bar'})
        response = self.client.get(nonexistent_user_url)
        self.assertEqual(response.status_code, 404)

    def test_user_profile_panel(self):
        """Test profile panel from UserView"""
        self.client.login(username='foo', password='foobar')
        user_url = reverse('user', kwargs={
            'username': self.bucket_user.user.username})
        response = self.client.get(user_url)
        self.assertContains(response, 'Edit profile')
        self.assertTemplateUsed(response, 'users/view_profile.html')
        self.assertTemplateUsed(response, 'users/snippets/profile.html')

        new_user = User.objects.create_user(username='bar', password='foobar')
        new_user_url = reverse('user', kwargs={'username': new_user.username})
        response = self.client.get(new_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Edit profile')


class UserProfileViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.bucket_user = BucketUser.objects.get(user=self.user)
        self.client = Client()

    def test_get_user_profile_view(self):
        """Test GET user profile"""
        # Get profile as non logged-in user
        profile_url = reverse('user_profile', kwargs={'username': 'foo'})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 403)
        # Get your own profile as a logged-in user
        self.client.login(username='foo', password='foobar')
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        # Get view profile of nonexistent profile
        bar_profile_url = reverse('user_profile', kwargs={'username': 'bar'})
        response = self.client.get(bar_profile_url)
        self.assertEqual(response.status_code, 404)
        # Get view profile of other user
        user = User.objects.create_user(username='bar', password='foobar')
        bucketuser = BucketUser.objects.get(user=user)
        response = self.client.get(bar_profile_url)
        self.assertEqual(response.status_code, 403)
        # Get view profile as superuser
        self.user.is_superuser = True
        self.user.save()
        response = self.client.get(bar_profile_url)
        self.assertEqual(response.status_code, 200)

    def test_post_user_profile_view(self):
        """Test POST user profile"""
        self.client.login(username='foo', password='foobar')
        profile_url = reverse('user_profile', kwargs={'username': 'foo'})
        response = self.client.post(profile_url, data={'first_name': 'Foo'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/users/foo/'))
        user = User.objects.get(username='foo')
        self.assertEqual(user.first_name, 'Foo')

        bar_profile_url = reverse('user_profile', kwargs={'username': 'bar'})
        response = self.client.post(bar_profile_url, data={})
        self.assertEqual(response.status_code, 404)

        self.user.is_superuser = True
        self.user.save()
        user = User.objects.create_user(username='bar', password='foobar')
        bucketuser = BucketUser.objects.get(user=user)
        response = self.client.post(bar_profile_url,
                                    data={'first_name': 'Bar'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/users/bar/'))
        user = User.objects.get(username='bar')
        self.assertEqual(user.first_name, 'Bar')

    def test_user_profile_view_templates(self):
        """Test the usage of templates and content in UserProfileView"""
        profile_url = reverse('user_profile', kwargs={'username': 'foo'})
        self.client.login(username='foo', password='foobar')
        response = self.client.get(profile_url)
        self.assertTemplateUsed(response, 'users/edit_profile.html')
        self.assertContains(response, "Edit my profile")
        self.assertContains(response, "/users/foo/")

        self.user.is_superuser = True
        self.user.save()
        User.objects.create_user(username='bar', password='foobar')
        bar_profile_url = reverse('user_profile', kwargs={'username': 'bar'})
        response = self.client.get(bar_profile_url)

        self.assertContains(response, "Edit my profile")
        self.assertContains(response, "/users/bar/")
