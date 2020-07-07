from django.test import TestCase

from subjects.forms import (AddSubjectForm, EditSubjectForm,
                            AddContentForm, EditContentForm)
from subjects.models import Subject, Content


class BaseTestCase(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name="Test Subject",
                                              description="This is a test subject.")
        self.content = Content.objects.create(subject=self.subject,
                                              title="Test Content",
                                              type=CONTENT_TYPES[2],
                                              creator="Foo Bar",
                                              description="Test content description, this is.",
                                              bookmarked_by=self.bucket_user)


class AddSubjectFormTestCase(BaseTestCase, TestCase):
    def test_add_subject_form(self):
        """Test add Subject form"""
        data = {'name':'Bar', 'description': 'This is another test subject.''}
        form = AddSubjectForm(data=data)
        form.save()
        subjects = Subject.objects.all()
        self.assertEqual(len(subjects), 2)
        new_subject = Subject.objects.get(slug='bar')
        self.assertTrue(new_subject.name, 'Bar')


class EditSubjectFormTestCase(BaseTestCase, TestCase):
    def test_edit_subject_form(self):
        """Test edit subject"""
        data = {'name':'Bar Baz', 'description': 'This is another test subject.''}
        form = EditSubjectForm(instance=self.subject, data=data)
        self.assertTrue(form.is_valid())
        form.save()
        subject = Subject.objects.get()
        self.assertEqual(subject.name, 'Bar Baz')
        self.assertEqual(subject.slug, 'bar-baz')


class AddContentFormTestCase(BaseTestCase, TestCase):
    def test_add_content_form(self):
        """Test add Content form"""
        data = {'title': 'FooTest', 'type': CONTENT_TYPES[3],
                'creator': 'bar baz', 'content_url': 'www.bartest.com/foo/baz'}
        form = AddContentForm(data=data)
        form.save()
        contents = Content.objects.all()
        self.assertEqual(len(contents), 2)
        new_content = Content.objects.get(slug='footest')
        self.assertTrue(new_content.name, 'FooTest')


class EditContentFormTestCase(BaseTestCase, TestCase):
    def test_edit_content_form(self):
        """Test edit content"""
        data = {'title': 'Foo Bar', 'type': CONTENT_TYPES[1],
                'creator': 'Bar Bar', 'content_url': 'www.bartest.com/foo/baz'}
        form = EditContentForm(instance=self.content, data=data)
        self.assertTrue(form.is_valid())
        form.save()
        content = Content.objects.get()
        self.assertEqual(content.name, 'Foo Bar')
        self.assertEqual(content.slug, 'foo-bar')
