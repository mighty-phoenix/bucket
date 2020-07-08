from django.test import TestCase
from django.contrib.auth.models import User

from lists.forms import AddListForm, EditListForm
from subjects.models import Content
from users.models import BucketUser
from lists.models import List


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.bucketuser = BucketUser.objects.get(user=self.user)
        self.list = List.objects.create(user=self.bucketuser,
                                        name="Test List")
        self.content = Content.objects.create(title="Foo")
        self.content2 = Content.objects.create(title="Bar")
        self.list.content.add(self.content)


class AddListFormTestCase(BaseTestCase, TestCase):
    def test_add_list_form(self):
        """Test add List form"""
        data = {'name':'Bar', 'description': 'List for testing',
                'content': [self.content]}
        form = AddListForm(data=data)
        form.instance.user = self.bucketuser
        form.save()
        lists = List.objects.all()
        self.assertEqual(len(lists), 2)
        new_list = List.objects.get(name='Bar')
        self.assertEqual(list(new_list.content.all()), [self.content])


class EditListFormTestCase(BaseTestCase, TestCase):
    def test_edit_list_form(self):
        """Test edit List form"""
        data = {'name':'Bar Baz', 'description': 'Further testing',
                'content': [self.content2]}
        form = EditListForm(instance=self.list, data=data)
        self.assertTrue(form.is_valid())
        form.save()
        edited_list = List.objects.get()
        self.assertEqual(edited_list.name, 'Bar Baz')
        self.assertEqual(edited_list.description, 'Further testing')
        self.assertEqual(list(edited_list.content.all()), [self.content2])
