from django.forms import ModelForm, PasswordInput

from django.contrib.auth.models import User
from main.models import Industry, Company, Category


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
        exclude = ('id',)


class IndustryForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = Industry


class CompanyForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = Company


class CategoryForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = Category
