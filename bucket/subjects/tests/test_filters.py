from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.files import File

from subjects.constants import media_types
from subjects.models import Content
from subjects.filters import *


class BaseTestCase(object):
    def setUp(self):
        self.content = Content.objects.create(
            title="Test Content",
            url="abc.com",
            content_id="123456",
            type=media_types[2][0],
            image=File(file=b""),
            description="Test content description, this is.",
            tags=['Action', 'Comedy'],
            topics=['Strategy', 'Philosophy']
        )
        self.content2 = Content.objects.create(
            title="Foo Bar",
            url="def.com",
            content_id="lalala",
            type=media_types[0][0],
            image=File(file=b""),
            description="10 minute. La song.",
            tags=['Fantasy', 'Mystery'],
            topics=['Sociology', 'History']
        )
        self.content3 = Content.objects.create(
            title="Foo Baz",
            url="defcon.com",
            content_id="lindaG",
            type=media_types[0][0],
            image=File(file=b""),
            description="ft. Yoon Mi Rae",
            tags=['Fantasy', 'Mystery'],
            topics=['Sociology', 'History']
        )


class ContentFilterTestCase(BaseTestCase, TestCase):
    def test_filter_content_filter(self):
        """Test content filter"""
        # with no data
        f = ContentFilter(data={}, queryset=Content.objects.all())
        self.assertEqual(set(list(f.qs)), set(list(Content.objects.all())))
        # with data
        data = {'title':'foo', 'type':'book', 'tags':'Fantasy',
                'topics':'History'}
        f = ContentFilter(data=data, queryset=Content.objects.all())
        self.assertEqual(list(f.qs), [self.content2, self.content3])


class ContentBookmarkFilterTestCase(BaseTestCase, TestCase):
    def test_filter_content_bookmark_filter(self):
        """Test bookmarked content filter"""
        #self.user = User.objects.create_user(username='foo', password='foobar')
        #self.bucketuser = BucketUser.objects.get(user=self.user)
        #self.bucketuser.content_bookmark.add(self.content)
        #self.bucketuser.content_bookmark.add(self.content2)
        #self.content.content_bookmarked_by.add(self.bucketuser)
        #self.content2.content_bookmarked_by.add(self.bucketuser)
        # with no data
        #f = ContentBookmarkFilter(data={}, queryset=Content.objects.all())
        #self.assertEqual(list(f.qs), [self.content, self.content2])
        # with data
        #data = {'title':'foo', 'type':'book', 'tags':'Fantasy',
        #        'topics':'History'}
        #f = ContentBookmarkFilter(data=data, queryset=Content.objects.all())
        #self.assertEqual(list(f.qs), [self.content2])
        pass


class ContentTagFilterTestCase(BaseTestCase, TestCase):
    def test_filter_content_tag_filter(self):
        """Test tag content filter"""
        # with no data
        #f = ContentTagFilter(data={}, queryset=Content.objects.all())
        #self.assertEqual(list(f.qs), [self.content, self.content2])
        # with data
        #data = {'title':'foo', 'type':'book', 'topics':'History'}
        #f = ContentTagFilter(data=data, queryset=Content.objects.all())
        #self.assertEqual(list(f.qs), [self.content2])
        pass


class ContentTopicFilterTestCase(BaseTestCase, TestCase):
    def test_filter_content_topic_filter(self):
        """Test topic content filter"""
        #f = ContentTopicFilter(data={}, queryset=Content.objects.all())
        #self.assertEqual(list(f.qs), [self.content, self.content2])
        # with data
        #data = {'title':'foo', 'type':'book', 'tags':'Fantasy'}
        #f = ContentTopicFilter(data=data, queryset=Content.objects.all())
        #self.assertEqual(list(f.qs), [self.content2])
        pass
