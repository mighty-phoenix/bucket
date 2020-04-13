from django import forms
from django.contrib.auth.models import User
#from allauth.account.forms import ChangePasswordForm
#from django.core.exceptions import ValidationError

from common.helpers import SubmitCancelFormHelper
from users.models import BucketUser


class UserForm(forms.ModelForm):
    """User form combined with BucketUserForm"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        bucket_user = BucketUser.objects.get(user=user)
        bucket_user_kwargs = kwargs.copy()
        bucket_user_kwargs['instance'] = bucket_user
        self.bucket_user_form = BucketUserForm(*args, **bucket_user_kwargs)

        super(UserForm, self).__init__(*args, **kwargs)

        self.fields.update(self.bucket_user_form.fields)
        self.initial.update(self.bucket_user_form.initial)

        self.helper = SubmitCancelFormHelper(
            self, cancel_href="{{ bucketuser.get_absolute_url }}")

    def save(self, *args, **kwargs):
        self.bucket_user_form.save(*args, **kwargs)
        return super(UserForm, self).save(*args, **kwargs)


class BucketUserForm(forms.ModelForm):
    """Form for BucketUser model"""
    class Meta:
        model = BucketUser
        fields = ('blog_url', 'homepage_url', 'profile_picture')


'''
class SystersChangePasswordForm(ChangePasswordForm):
    # The clean_password1() method which checks that new password differs from the old one
    # is added to allauth ChangePasswordForm class.
    # So ChangePasswordForm class is derived.
    def __init__(self, *args, **kwargs):
        super(SystersChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        if self.cleaned_data["newpassword"] == self.cleaned_data.get("oldpassword", None):
            raise ValidationError("New password must differ from the old one.")
        return self.cleaned_data["new_password"]
'''
