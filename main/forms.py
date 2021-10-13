from django.forms import ModelForm, PasswordInput

from django.contrib.auth.models import User
from main.models import Industry, Company, Category, Event


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': PasswordInput()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class DefaultForm(ModelForm):
    class Meta:
        fields = '__all__'


class IndustryCreateForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = Industry


class CompanyCreateForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = Company
        exclude = ('update_date', 'insert_date')


class CompanyUpdateForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = Company
        exclude = ('update_date', 'insert_date', 'deleted', 'delete_date', 'number_of_ratings', 'update_person_name')


class CategoryCreateForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = Category


class EventCreateForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = Event
