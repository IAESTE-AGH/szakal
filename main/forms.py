from django.forms import ModelForm

from django.contrib.auth.models import User
from main.models import Industry


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class DefaultForm(ModelForm):
    class Meta:
        exclude = ('id',)


class IndustryForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = Industry
