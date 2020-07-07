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
        self.subject = Subject.objects.create(name="Test Subject",
                                              description="This is a test subject.")
        self.content = Content.objects.create(title="Test Content",
                                              type=CONTENT_TYPES[2][0],
                                              creator="Foo Bar",
                                              description="Test content description, this is.")
        self.content.subject.add(self.subject)
        self.content.bookmarked_by.add(self.bucketuser)


class SubjectsListTestCase(BaseTestCase, TestCase):
    def test_view_subjects_list(self):
        """
        Test Subjects list view for
        * correct http response and template
        * correct object list
        """
        url = reverse('list_subjects')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "subjects/subjects_list.html")
        self.assertContains(response, "Test Subject")
        self.assertEqual(len(response.context['subject_list']), 1)

        self.subject2 = Subject.objects.create(
            name="Bar", description="This is another test subject.")
        url = reverse('list_subjects')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "subjects/subjects_list.html")
        self.assertContains(response, "Test Subject")
        self.assertContains(response, "Bar")
        self.assertEqual(len(response.context['subject_list']), 2)


class SubjectsPageViewTestCase(BaseTestCase, TestCase):
    def test_view_subjects_page(self):
        """
        Test Subject view for correct http response
        * correct context data and object list
        * response for non existent url
        """
        url = reverse('view_subject_page', kwargs={'slug': 'test-subject'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/subject_page.html')
        self.assertEqual(response.context['subject'], self.subject)
        self.assertContains(response, "Test Content")
        self.assertEqual(len(response.context['subject_content']), 1)

        self.content2 = Content.objects.create(title="Content 2",
                                               type=CONTENT_TYPES[0][0])
        self.content2.subject.add(self.subject)
        self.content3 = Content.objects.create(title="Content 3",
                                               type=CONTENT_TYPES[3][0])
        response = self.client.get(url)
        self.assertContains(response, "Content 2")
        self.assertNotContains(response, "Content 3")
        self.assertEqual(len(response.context['subject_content']), 2)

        nonexistent_url = reverse('view_subject_page', kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class ContentsPageTestCase(BaseTestCase, TestCase):
    def test_view_contents_page(self):
        """
        Test Contents page view for correct http response
        * correct object list
        * response for non existent url
        """
        url = reverse('contents_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/contents_page.html')

        self.assertContains(response, "Test Content")
        self.assertEqual(len(response.context['contents']), 1)
        self.content2 = Content.objects.create(title="Content 2",
                                               type=CONTENT_TYPES[3][0])
        response = self.client.get(url)
        self.assertContains(response, "Content 2")
        self.assertEqual(len(response.context['contents']), 2)


class ContentViewTestCase(BaseTestCase, TestCase):
    def test_view_content_view(self):
        """
        Test Content view for correct http response
        * correct context data and object list
        * response for non existent url

        Consider cases:
        * with and without login
        * with and without user bookmarks
        * with and without user list
        * with and without content in user list
        """
        url = reverse('view_content', kwargs={'slug': 'test-content'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/content.html')
        self.assertEqual(response.context['content'], self.content)

        # test view while logged out
        self.assertEqual(response.context['is_bookmark'], False)
        self.assertEqual(list(response.context['content_bookmarked_by']),
                         [self.bucketuser])
        self.assertEqual(response.context['number_of_bookmarks'], 1)
        self.assertEqual(response.context['user_lists'], [])
        self.assertEqual(response.context['is_in_user_list'], False)

        # login user
        self.client.login(username='foo', password='foobar')

        # test view with user bookmark
        response = self.client.get(url)
        self.assertEqual(response.context['is_bookmark'], True)
        self.assertEqual(list(response.context['content_bookmarked_by']),
                         [self.bucketuser])
        self.assertEqual(response.context['number_of_bookmarks'], 1)

        self.user2 = User.objects.create(username='bar', password='foobar')
        self.bucketuser2 = BucketUser.objects.get(user=self.user2)
        self.content.bookmarked_by.add(self.bucketuser2)
        response = self.client.get(url)
        self.assertEqual(list(response.context['content_bookmarked_by']),
                         [self.bucketuser, self.bucketuser2])
        self.assertEqual(response.context['number_of_bookmarks'], 2)

        # test view without user bookmark
        self.content.bookmarked_by.remove(self.bucketuser)
        response = self.client.get(url)
        self.assertEqual(response.context['is_bookmark'], False)
        self.content.bookmarked_by.remove(self.bucketuser2)
        response = self.client.get(url)
        self.assertEqual(list(response.context['content_bookmarked_by']), [])
        self.assertEqual(response.context['number_of_bookmarks'], 0)

        # test view with no user list, while logged in
        self.assertEqual(response.context['user_lists'], [])
        self.assertEqual(response.context['is_in_user_list'], False)

        # test view with user list which does not have the content
        self.list = List.objects.create(user=self.bucketuser,
                                        name="Test List")
        response = self.client.get(url)
        self.assertEqual(response.context['user_lists'], [(self.list, 0)])
        self.assertEqual(response.context['is_in_user_list'], False)

        # test view with user list which has the content
        self.list.content.add(self.content)
        response = self.client.get(url)
        self.assertEqual(response.context['user_lists'], [(self.list, 1)])
        self.assertEqual(response.context['is_in_user_list'], True)

        # test for nonexistent url
        nonexistent_url = reverse('view_content', kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class AddContentViewTestCase(BaseTestCase, TestCase):
    def test_get_add_content_view(self):
        """Test GET request to add new content"""
        url = reverse('add_content')
        # test response while logged out
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'subjects/add_content.html')

    def test_post_add_content_view(self):
        """Test POST request to add new content"""
        url = reverse("add_content")
        # test response while logged out
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 403)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        data = {'title': 'FooTest', 'type': CONTENT_TYPES[4][0],
                'creator': 'bar baz', 'content_url': 'www.bartest.com/foo/baz'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        new_content = Content.objects.get(slug='footest')
        self.assertTrue(new_content.title, 'FooTest')


class EditContentViewTestCase(BaseTestCase, TestCase):
    def test_get_edit_content_view(self):
        """Test GET edit content"""
        # test for wrong url
        wrong_url = reverse("edit_content", kwargs={'slug': 'test-contentss'})
        response = self.client.get(wrong_url)
        self.assertEqual(response.status_code, 403)
        # test response while logged out
        url = reverse("edit_content", kwargs={'slug': 'test-content'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "success")
            self.assertTrue(
                'Successfully'
                in message.message)

        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(message.tags, "error")
            self.assertTrue(
                'Something went wrong. Please try again'
                in message.message)
        self.assertTemplateUsed(response, 'subjects/edit_content.html')

    def test_post_edit_content_view(self):
        """Test POST edit content"""
        # test for wrong url
        wrong_url = reverse("edit_content", kwargs={'slug': 'test-contentss'})
        response = self.client.post(wrong_url)
        self.assertEqual(response.status_code, 403)
        # test response while logged out
        url = reverse("edit_content", kwargs={'slug': 'test-content'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        data = {'title': 'FooTest', 'type': CONTENT_TYPES[3][0],
                'creator': 'bar baz', 'content_url': 'www.bartest.com/foo/baz'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/content/footest'))


class DeleteContentViewTestCase(BaseTestCase, TestCase):
    def setUp(self):
        super(DeleteContentViewTestCase, self).setUp()
        self.content2 = Content.objects.create(title="Foo Baz",
                                               type=CONTENT_TYPES[3][0])
        #self.client = Client()

    def test_get_delete_content_view(self):
        """Test GET to confirm deletion of content"""
        url = reverse("delete_content", kwargs={'slug': 'foo-baz'})
        # test response while logged out
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm to delete")

    def test_post_delete_content_view(self):
        """Test POST to delete a content"""
        url = reverse("delete_content", kwargs={'slug': 'foo-baz'})
        # test response while logged out
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        # One content deleted, another content left initialized in BaseTestCase
        self.assertSequenceEqual(Content.objects.all(), [self.content])


class BookmarkContentViewTestCase(BaseTestCase, TestCase):
    def test_view_bookmark_content_view(self):
        """
        Test Bookmark content view for
        * correct http response and template
        * user login
        * user bookmark and unbookmark
        * response for non existent url
        """
        url = reverse("bookmark_content", kwargs={'slug': 'test-content'})
        # test response while logged out
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # test response while logged in
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('content/test-content'))
        self.assertEqual(list(self.content.bookmarked_by.all()), [])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('content/test-content'))
        self.assertEqual(list(self.content.bookmarked_by.all()), [self.bucketuser])

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
        self.assertEqual(response.status_code, 403)
        # test response while logged out
        self.client.login(username='foo', password='foobar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/all_bookmarks.html')

        # test object list
        self.assertContains(response, "Test Content")
        self.assertEqual(len(response.context['bookmark_list']), 1)
        self.content2 = Content.objects.create(title="Content 2",
                                               type=CONTENT_TYPES[3][0])
        self.content2.bookmarked_by.add(self.bucketuser)
        response = self.client.get(url)
        self.assertContains(response, "Content 2")
        self.assertEqual(len(response.context['bookmark_list']), 2)
        self.content.bookmarked_by.remove(self.bucketuser)
        self.content2.bookmarked_by.remove(self.bucketuser)
        response = self.client.get(url)
        self.assertEqual(len(response.context['bookmark_list']), 0)
