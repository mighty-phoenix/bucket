from django.test import TestCase

from subjects.forms import AddSubjectForm, EditSubjectForm
from subjects.models import Subject


class SubjectFormTestCaseBase:
    def setUp(self):
        self.subject = Subject.objects.create(name='Test Subject', slug='baz',
                                              books='Foo, Bar', movies='Bar, Foo',
                                              docs='doc Foo', yt_channels='FooVlogs',
                                              websites='Bar.com', fb_pages='Baz',
                                              insta_pages='Foo, Baz')


class AddSubjectFormTestCase(SubjectFormTestCaseBase, TestCase):
    def test_add_subject_form(self):
        """Test add Subject form"""
        data = {'name': 'Foo', 'slug': 'foo', 'books': 'Foo, Bar', 'movies': 'Bar, Foo',
                'docs': 'doc Bar', 'yt_channels': 'BazVlogs', 'websites': 'Foo.com',
                'fb_pages': 'Bar', 'insta_pages': 'Bar, Baz'}
        form = AddSubjectForm(data=data)
        form.save()
        subjects = Subject.objects.all()
        self.assertEqual(len(subjects), 2)
        new_subject = Subject.objects.get(slug='foo')
        self.assertTrue(new_subject.name, 'Foo')

class EditSubjectFormTestCase(SubjectFormTestCaseBase, TestCase):
    def test_edit_subject_form(self):
        """Test edit subject"""
        data = {'name': 'Foo Bar', 'slug': 'foobar', 'books': 'Foo, Bar', 'movies': 'Bar, Foo',
                'docs': 'doc Bar', 'yt_channels': 'BazVlogs', 'websites': 'Foo.com',
                'fb_pages': 'Bar', 'insta_pages': 'Bar, Baz'}
        form = EditSubjectForm(instance=self.subject, data=data)
        self.assertTrue(form.is_valid())
        form.save()
        subject = Subject.objects.get()
        self.assertEqual(subject.name, 'Foo Bar')
        self.assertEqual(subject.slug, 'foobar')
