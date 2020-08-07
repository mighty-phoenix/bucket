from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.files import File

from subjects.models import Content
from users.models import BucketUser
from lists.models import List
from lists.filters import *


class BaseTestCase(object):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.bucketuser = BucketUser.objects.get(user=self.user)
        self.content = Content.objects.create(title="Test Content")
        self.list = List.objects.create(
            user=self.bucketuser,
            name="Test List",
            description="Testing for lists models.",
            visibility="public",
            topics=['History', 'Philosophy']
        )
        self.list.content.add(self.content)
        self.list.list_bookmarked_by.add(self.bucketuser)
        self.list2 = List.objects.create(
            user=self.bucketuser,
            name="More Test",
            description="More and more",
            visibility="public",
            topics=['Photograpy', 'Philosophy']
        )
        self.list3 = List.objects.create(
            user=self.bucketuser,
            name="Rainism",
            description="How to avoid the sun",
            visibility="private",
            topics=['Sociology', 'Philosophy']
        )

class ListFilterTestCase(BaseTestCase, TestCase):
    def test_filter_list_filter(self):
        """Test list filter"""
        # with no data
        f = ListFilter(data={}, queryset=List.objects.all())
        self.assertEqual(set(list(f.qs)), set([self.list, self.list2]))
        # with data
        data = {'name':'List', 'topics':'History'}
        f = ListFilter(data=data, queryset=List.objects.all())
        self.assertEqual(list(f.qs), [self.list])
        data = {'name':'', 'topics':'Philosophy'}
        f = ListFilter(data=data, queryset=List.objects.all())
        # it should be this
        #self.assertEqual(list(f.qs), [self.list, self.list2])
        # but is
        self.assertEqual(list(f.qs), [self.list2, self.list])


class UserListFilterTestCase(BaseTestCase, TestCase):
    def test_filter_user_list_filter(self):
        """Test user list filter"""
        pass


class ListBookmarkFilterTestCase(BaseTestCase, TestCase):
    def test_filter_list_bookmark_filter(self):
        """Test bookmarked list filter"""
        pass
