from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from django.test import TestCase, Client

from subjects.constants import CONTENT_TYPES
from subjects.models import Subject, Content
from lists.models import List
from users.models import BucketUser


class BaseTestCase(object):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.bucketuser = BucketUser.objects.get(user=self.user)
        self.content = Content.objects.create(title="Test Content",
                                              type=CONTENT_TYPES[2][0],
                                              creator="Foo Bar",
                                              description="Test content description, this is.")
        self.list = List.objects.create(user=self.bucketuser,
                                        name="Test List")
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
        self.assertEqual(len(response.context['lists']), 1)

        self.user2 = User.objects.create_user(username='bar', password='foobar')
        self.bucketuser2 = BucketUser.objects.get(user=self.user2)
        self.list2 = List.objects.create(user=self.bucketuser2,
                                         name="Baa Baa Black Sheep")
        response = self.client.get(url)
        self.assertContains(response, "Baa Baa Black Sheep")
        self.assertEqual(len(response.context['lists']), 2)


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
        self.assertEqual(response.context['is_bookmark'], False)
        # with user bookmarks
        self.list.bookmarked_by.add(self.bucketuser)
        response = self.client.get(url)
        self.assertEqual(list(response.context['list_bookmarked_by']),
                         [self.bucketuser])
        self.assertEqual(response.context['number_of_bookmarks'], 1)
        self.assertEqual(response.context['is_bookmark'], False)

        # test view while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.context['is_bookmark'], True)
        self.list.bookmarked_by.remove(self.bucketuser)
        response = self.client.get(url)
        self.assertEqual(response.context['is_bookmark'], False)

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
        data = {'name':'Baz', 'description': 'List for testing'}
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
        data = {'name':'Bar', 'description': 'Yada Yada'}
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

        # One list deleted, another list left initialized in BaseTestCase
        self.assertSequenceEqual(List.objects.all(), [self.list])
