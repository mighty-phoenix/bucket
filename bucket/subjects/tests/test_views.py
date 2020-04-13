from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client

from subjects.models import Subject


class SubjectViewBaseTestCase(object):
    def setUp(self):
        self.subject = Subject.objects.create(name='Test Subject', slug='baz',
                                              books='Foo, Bar', movies='Bar, Foo',
                                              docs='doc Foo', yt_channels='FooVlogs',
                                              websites='Bar.com', fb_pages='Baz',
                                              insta_pages='Foo, Baz')


class SubjectViewTestCase(SubjectViewBaseTestCase, TestCase):
    def test_view_subject_view(self):
        """Test Subject view for correct http response"""
        url = reverse('view_subject', kwargs={'slug': 'baz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subject/subject.html')
        self.assertEqual(response.context['subject'], self.subject)

        nonexistent_url = reverse('view_subject', kwargs={'slug': 'bar'})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class SubjectsListViewTestCase(SubjectViewBaseTestCase, TestCase):
    def test_view_subjects_list_view(self):
        """Test Subjects list view for correct http response and
        all subjects in a list"""
        url = reverse('list_subjects')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "subject/subjects_list.html")
        self.assertContains(response, "Test Subject")
        self.assertEqual(len(response.context['subject_list']), 1)

        self.subject2 = Subject.objects.create(
            name='Bar', slug='bar', books='Foo, Bar', movies='Bar, Foo',
            docs='doc Foo', yt_channels='FooVlogs', websites='Bar.com',
            fb_pages='Baz', insta_pages='Foo, Baz')
        url = reverse('list_subjects')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "subject/subjects_list.html")
        self.assertContains(response, "Test Subject")
        self.assertContains(response, "Bar")
        self.assertEqual(len(response.context['subject_list']), 2)
