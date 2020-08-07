from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files import File

from lists.forms import AddListForm, EditListForm
from subjects.models import Content
from users.models import BucketUser
from lists.models import List


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.bucketuser = BucketUser.objects.get(user=self.user)
        self.list = List.objects.create(
            user=self.bucketuser,
            name="Test List",
            description="Testing for lists models.",
            image=File(file=b""),
            visibility="public",
            topics=['History', 'Philosophy']
        )
        self.content = Content.objects.create(title="Foo",
                                              image=File(file=b""))
        self.content2 = Content.objects.create(title="Bar",
                                               image=File(file=b""))
        self.list.content.add(self.content)


class AddListFormTestCase(BaseTestCase, TestCase):
    def test_add_list_form(self):
        """Test add List form"""
        data = {'name':'Bar', 'description': 'List for testing',
                'topics': 'Trading'}
        form = AddListForm(data=data)
        form.instance.user = self.bucketuser
        form.save()
        lists = List.objects.all()
        self.assertEqual(len(lists), 4)
        new_list = List.objects.get(name='Bar')
        self.assertEqual(list(new_list.content.all()), [])
        self.assertEqual(new_list.user, self.bucketuser)


class EditListFormTestCase(BaseTestCase, TestCase):
    def test_edit_list_form(self):
        """Test edit List form"""
        data = {'name':'Bar Baz', 'description': 'Further testing',
                'visibility': 'private', 'topics': 'History'}
        form = EditListForm(instance=self.list, data=data)
        self.assertTrue(form.is_valid())
        form.save()
        edited_list = List.objects.get(name='Bar Baz')
        self.assertEqual(edited_list.description, 'Further testing')
        self.assertEqual(edited_list.visibility, 'private')
        self.assertEqual(edited_list.topics, 'History')


class AddContentToListFormTestCase(BaseTestCase, TestCase):
    def test_add_content_to_list_form(self):
        """Test add content to list form"""
        pass
