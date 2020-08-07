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


class BookmarkContentViewTestCase(BaseTestCase, TestCase):
    def test_view_bookmark_content_view(self):
        """
        Test Bookmark content view for
        * correct http response and template
        * user login
        * user bookmark and unbookmark
        * response for non existent url
        """
        url = reverse("bookmark_content", kwargs={'slug': '123456-test-content'})
        # test response while logged out
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('content/123456-test-content'))
        self.assertEqual(list(self.content.content_bookmarked_by.all()), [])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('content/123456-test-content'))
        self.assertEqual(list(self.content.content_bookmarked_by.all()), [self.bucketuser])

        # Test for non existent url
        nonexistent_url = reverse("bookmark_content", kwargs={'slug': 'bazbaz'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class AllBookmarksViewTestCase(BaseTestCase, TestCase):
    def test_view_all_bookmarks_view(self):
        """
        Test all Bookmarks view for
        * correct http response and template
        * user login
        * correct object list
        """
        url = reverse('all_bookmarks')
        # test response while logged out
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/all_bookmarks.html')

        # test object list
        self.assertContains(response, "Test Content")
        self.assertEqual(len(response.context['bookmark_list']), 1)
        self.content2 = Content.objects.create(title="Content 2",
                                               type=media_types[3][0])
        self.content2.content_bookmarked_by.add(self.bucketuser)
        response = self.client.get(url)
        self.assertContains(response, "Content 2")
        self.assertEqual(len(response.context['bookmark_list']), 2)
        self.content.content_bookmarked_by.remove(self.bucketuser)
        self.content2.content_bookmarked_by.remove(self.bucketuser)
        response = self.client.get(url)
        self.assertEqual(len(response.context['bookmark_list']), 0)
