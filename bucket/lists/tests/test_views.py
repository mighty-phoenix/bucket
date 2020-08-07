from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from django.test import TestCase, Client
from django.core.files import File

from subjects.models import Content
from lists.models import List
from users.models import BucketUser


class BaseTestCase(object):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.bucketuser = BucketUser.objects.get(user=self.user)
        self.content = Content.objects.create(title="Foo",
                                              image=File(file=b""))
        self.list = List.objects.create(
            user=self.bucketuser,
            name="Test List",
            description="Testing for lists models.",
            topics=['History', 'Philosophy']
        )
        self.list.content.add(self.content)
        self.slug = self.list.slug


class ListsPageTestCase(BaseTestCase, TestCase):
    def test_view_lists_page(self):
        """Test Lists page view for correct http response"""
        url = reverse('lists_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/lists_page.html')
        self.assertContains(response, "Test List")
        self.assertEqual(len(response.context['filter'].qs), 1)

        self.user2 = User.objects.create_user(username='bar', password='foobar')
        self.bucketuser2 = BucketUser.objects.get(user=self.user2)
        self.list2 = List.objects.create(user=self.bucketuser2,
                                         name="Lee Hyori")
        url = reverse('lists_page')
        response = self.client.get(url)
        self.assertContains(response, "Lee Hyori")
        self.assertEqual(len(response.context['filter'].qs), 2)


class ViewListTestCase(BaseTestCase, TestCase):
    def test_view_list_view(self):
        """
        Test view List for correct http response
        * correct context data and object list
        * response for non existent url

        Consider cases:
        * with and without login
        * with and without bookmarks
        """
        url = reverse('view_list', kwargs={'slug': self.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(response.context['list'], self.list)
        self.assertEqual(list(response.context['list_content']), [self.content])
        self.assertEqual(response.context['number_of_items'], 1)

        # without user bookmarks
        self.assertEqual(list(response.context['list_bookmarked_by']), [])
        self.assertEqual(response.context['number_of_bookmarks'], 0)
        #self.assertEqual(response.context['is_bookmark'], False)
        # with user bookmarks
        self.list.list_bookmarked_by.add(self.bucketuser)
        response = self.client.get(url)
        self.assertEqual(list(response.context['list_bookmarked_by']),
                         [self.bucketuser])
        self.assertEqual(response.context['number_of_bookmarks'], 1)
        #self.assertEqual(response.context['is_bookmark'], False)

        # test view while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        #self.assertEqual(response.context['is_bookmark'], True)
        self.list.list_bookmarked_by.remove(self.bucketuser)
        response = self.client.get(url)
        #self.assertEqual(response.context['is_bookmark'], False)

        # test for nonexistent url
        nonexistent_url = reverse('view_list', kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class AddListViewTestCase(BaseTestCase, TestCase):
    def test_get_add_list_view(self):
        """Test GET request to add new list"""
        url = reverse('add_list')
        # test response while logged out
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'List created'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'lists/add_list.html')

    def test_post_add_list_view(self):
        """Test POST request to add new list"""
        url = reverse("add_list")
        # test response while logged out
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 302)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        data = {'name':'Baz', 'description': 'List for testing',
                'topics':'Entertainment'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        new_list = List.objects.get(name='Baz', user=self.bucketuser)
        self.assertEqual(new_list.description, 'List for testing')


class EditListViewTestCase(BaseTestCase, TestCase):
    def test_get_edit_list_view(self):
        """Test GET edit list"""
        # test for wrong url
        wrong_url = reverse("edit_list", kwargs={'slug': 'test-list'})
        response = self.client.get(wrong_url)
        self.assertEqual(response.status_code, 403)
        # test response while logged out
        url = reverse("edit_list", kwargs={'slug': self.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "info")
            self.assertTrue(
                'List updated'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'lists/edit_list.html')

        # test edit other user's list
        self.user2 = User.objects.create_user(username='bar', password='foobar')
        self.bucketuser2 = BucketUser.objects.get(user=self.user2)
        self.list3 = List.objects.create(user=self.bucketuser2,
                                         name="Bar")
        url = reverse("edit_list", kwargs={'slug': self.list3.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_post_edit_list_view(self):
        """Test POST edit list"""
        # test for wrong url
        wrong_url = reverse("edit_list", kwargs={'slug': 'test-list'})
        response = self.client.post(wrong_url)
        self.assertEqual(response.status_code, 403)
        # test response while logged out
        url = reverse("edit_list", kwargs={'slug': self.slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        data = {'name':'Bar', 'description':'Yada Yada',
                'topics':'Entertainment', 'visibility':'private'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)


class DeleteListViewTestCase(BaseTestCase, TestCase):
    def setUp(self):
        super(DeleteListViewTestCase, self).setUp()
        self.list2 = List.objects.create(user=self.bucketuser,
                                         name="Baz")

    def test_get_delete_list_view(self):
        """Test GET to confirm deletion of list"""
        url = reverse("delete_list", kwargs={'slug': self.list2.slug})
        # test response while logged out
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm to delete")

        # test delete other user's list
        self.user2 = User.objects.create_user(username='bar', password='foobar')
        self.bucketuser2 = BucketUser.objects.get(user=self.user2)
        self.list3 = List.objects.create(user=self.bucketuser2,
                                         name="Bar")
        url = reverse("delete_list", kwargs={'slug': self.list3.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_post_delete_list_view(self):
        """Test POST to delete a list"""
        url = reverse("delete_list", kwargs={'slug': self.list2.slug})
        # test response while logged out
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        # One list deleted, three lists left initialized in BaseTestCase
        # including the default created Bookmarks and Recommendations
        self.assertEqual(List.objects.all().count(), 3)


class BookmarkListViewTestCase(BaseTestCase, TestCase):
    def test_view_bookmark_list_view(self):
        """Test Bookmark list view for
        * correct http response and template
        * user login
        * user bookmark and unbookmark
        * response for non existent url
        """
        url = reverse("bookmark_list", kwargs={'slug': self.slug})
        # test response while logged out
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith(self.slug))
        self.assertEqual(list(self.list.list_bookmarked_by.all()), [self.bucketuser])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith(self.slug))
        self.assertEqual(list(self.list.list_bookmarked_by.all()), [])

        # Test for non existent url
        nonexistent_url = reverse("bookmark_list", kwargs={'slug': 'bazbaz'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


'''
class AllUserListsViewTestCase(BaseTestCase, TestCase):
    def test_view_all_user_lists_view(self):
        """
        Test all user lists view for
        * correct http response and template
        * user login
        * correct object list
        """
        url = reverse('all_user_lists', kwargs={'username': self.user.username})
        # test response while logged out
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/all_bookmarked_lists.html')

        # test object list
        self.assertContains(response, "Test List")
        self.assertEqual(len(response.context['filter'].qs), 1)
        self.list2 = Content.objects.create(user=self.bucketuser,
                                            name="GaraGaraGo")
        self.list2.list_bookmarked_by.add(self.bucketuser)
        response = self.client.get(url)
        self.assertContains(response, "GaraGaraGo")
        self.assertEqual(len(response.context['filter'].qs), 2)
        self.list.list_bookmarked_by.remove(self.bucketuser)
        self.list2.list_bookmarked_by.remove(self.bucketuser)
        response = self.client.get(url)
        self.assertEqual(len(response.context['filter'].qs), 0)
'''


class AllBookmarkedListsViewTestCase(BaseTestCase, TestCase):
    def test_view_all_bookmarked_lists_view(self):
        """
        Test all bookmarked lists view for
        * correct http response and template
        * user login
        * correct object list
        """
        url = reverse('all_bookmarked_lists', kwargs={'username': self.user.username})
        self.list.list_bookmarked_by.add(self.bucketuser)
        # test response while logged out
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/all_bookmarked_lists.html')

        # test object list
        self.assertContains(response, "Test List")
        self.assertEqual(len(response.context['filter'].qs), 1)
        self.list2 = List.objects.create(user=self.bucketuser,
                                            name="GaraGaraGo")
        self.list2.list_bookmarked_by.add(self.bucketuser)
        response = self.client.get(url)
        self.assertContains(response, "GaraGaraGo")
        self.assertEqual(len(response.context['filter'].qs), 2)
        self.list.list_bookmarked_by.remove(self.bucketuser)
        self.list2.list_bookmarked_by.remove(self.bucketuser)
        response = self.client.get(url)
        self.assertEqual(len(response.context['filter'].qs), 0)
