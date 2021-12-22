from django.forms import ModelForm, PasswordInput, MultipleChoiceField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from main.models import User, Industry, Company, Category, Event, CategoryCompany, Assignment


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


class ExtendedForm(DefaultForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices = ((obj.id, obj.name) for obj in self.RELATED_MODEL.objects.all())

        self.fields[self.RELATED_DISPLAY_NAME] = MultipleChoiceField(choices=choices)

        params = {self.Meta.model.__name__.lower(): self.instance.id}
        initial_ids = [getattr(obj, self.RELATED_MODEL.__name__.lower()).id for obj in
                       self.MANY_TO_MANY_MODEL.objects.filter(**params).all()]

        self.fields[self.RELATED_DISPLAY_NAME].initial = initial_ids


class IndustryCreateForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = Industry


class CompanyCreateForm(ExtendedForm):
    RELATED_MODEL = Category
    RELATED_DISPLAY_NAME = 'categories'
    MANY_TO_MANY_MODEL = CategoryCompany

    class Meta(ExtendedForm.Meta):
        model = Company
        exclude = ('user', 'update_date', 'insert_date')


class CompanyUpdateForm(ExtendedForm):
    RELATED_MODEL = Category
    RELATED_DISPLAY_NAME = 'categories'
    MANY_TO_MANY_MODEL = CategoryCompany

    class Meta(ExtendedForm.Meta):
        model = Company
        exclude = ('update_date', 'insert_date', 'deleted', 'delete_date', 'number_of_ratings', 'update_person_name')


class CategoryCreateForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = Category


class CategoryCompanyCreateForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = CategoryCompany


class EventCreateForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = Event


class EventUpdateForm(ModelForm):
    class Meta:
        model = Event
        fields = ['active']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username')


class AssignmentCreateForm(DefaultForm):
    class Meta(DefaultForm.Meta):
        model = Assignment
        exclude = ('user', 'update_date', 'created_at')


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']


# class ContactCreateForm(ExtendedForm):
#     RELATED_MODEL = Category
#     RELATED_DISPLAY_NAME = 'categories'
#     MANY_TO_MANY_MODEL = CategoryCompany
#
#     class Meta(DefaultForm.Meta):
#         model = Contact
#         fields = ['accepted', 'date', 'comment', 'rating', 'company', 'contact_person', 'event', 'status',
#                   'type']
