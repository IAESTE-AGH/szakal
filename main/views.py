import datetime

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django import template
from django.views import View

from main.forms import *
from main.models import *

register = template.Library()

PREDEFINED_MODELS_USER_MANAGED = [
    'Assignment',
    'Company',
    'Contact'
]

PREDEFINED_MODELS_USER = [
    'Company',
    'Contact',
    'ContactPerson',
    'Assignment'
]

PREDEFINED_MODELS = [
    'Assignment',
    'Company',
    'Contact',
    'ContactPerson',
    'Category',
    'Industry',
    'Event'
]


def assign_form(create=False, update=False, delete=False):
    def decorator(func):
        def wrap(self, request, *args, **kwargs):
            object_ = self.kwargs['object'].capitalize()
            if object_ in PREDEFINED_MODELS:
                if not request.user.is_staff and object_ not in PREDEFINED_MODELS_USER:
                    return PermissionError

                self.model = eval(object_)
                self.object = None
                if update:
                    if request.user.is_staff or eval(object_).objects.get(id=kwargs['pk']).user == request.user:
                        self.form_class = eval(f'{object_}UpdateForm')
                    else:
                        return PermissionError
                elif create:
                    self.form_class = eval(f'{object_}CreateForm')
                elif delete:
                    pass

                self.success_url = f'/{object_.lower()}'
                return func(self, request, *args, **kwargs)
            return ValueError

        return wrap

    return decorator


def handle_extended_form(create=False, update=False):
    def decorator(func):
        def wrap(self, request, *args, **kwargs):
            if issubclass(self.form_class, ExtendedForm):
                form = self.form_class(request.POST)
                if form.is_valid():
                    if create:
                        if self.kwargs['object'].capitalize() in PREDEFINED_MODELS_USER_MANAGED and not request.user.is_staff:
                            instance = form.save(commit=False)
                            instance.user = request.user
                            instance.save()
                        else:
                            instance = form.save()
                    elif update:
                        instance = self.form_class.Meta.model.objects.get(id=kwargs['pk'])
                    else:
                        raise ValueError

                    b_id = instance.id
                    a_name = self.form_class.RELATED_MODEL.__name__.lower()
                    b_name = self.form_class.Meta.model.__name__.lower()

                    if update:
                        filter_params = {f'{b_name}_id': b_id}
                        self.form_class.MANY_TO_MANY_MODEL.objects.filter(**filter_params).delete()

                    for a_id in form.cleaned_data[self.form_class.RELATED_DISPLAY_NAME]:
                        parameters = {
                            f'{a_name}_id': a_id,
                            f'{b_name}_id': b_id
                        }
                        new = self.form_class.MANY_TO_MANY_MODEL(**parameters)
                        new.save()

                    return HttpResponseRedirect(self.success_url, status=200)
            else:
                return func(self, request, *args, **kwargs)

        return wrap

    return decorator


class RegisterView(CreateView):
    template_name = 'auth/user_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')


class Home(LoginRequiredMixin, View):
    template = 'home.html'

    def get(self, request, *args, **kwargs):
        context = {
            "company_count": Company.objects.all().count(),
            "companies_unmanaged": Company.objects.filter(user=None).count(),
            "user_count": User.objects.all().count(),
            "user_managed_companies": Company.objects.filter(user=request.user).all()
        }
        return render(request, self.template, context)


class ListObjectsView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        model = self.kwargs['object'].capitalize()

        if model in PREDEFINED_MODELS:
            self.template_name = f'{model.lower()}.html'
        else:
            raise ValueError

        whos = self.kwargs.get('whos')
        if not whos:
            model = eval(model)
            return model.objects.all()
        elif model == 'Event':
            model = eval(model)
            if whos == 'local':
                return model.objects.filter(local=True)
            elif whos == 'global':
                return model.objects.filter(local=False)
            else:
                raise ValueError
        elif model in PREDEFINED_MODELS_USER_MANAGED:
            model = eval(model)
            if whos == 'my':
                return model.objects.filter(user=self.request.user)
            elif whos == 'taken':
                return model.objects.filter(user__isnull=False)
            else:
                raise ValueError
        else:
            raise ValueError


class UpdateObjectView(LoginRequiredMixin, UpdateView):
    template_name = 'default_form.html'

    @assign_form(update=True)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @assign_form(update=True)
    @handle_extended_form(update=True)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AddObjectView(LoginRequiredMixin, CreateView):
    template_name = 'default_form.html'

    @assign_form(create=True)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @assign_form(create=True)
    @handle_extended_form(create=True)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DeleteObjectView(LoginRequiredMixin, DeleteView):
    template_name = 'default_form.html'

    @assign_form(delete=True)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @assign_form(delete=True)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


def assigning_decorator(func):
    def wrap(request, object, pk, *args, **kwargs):
        if object.capitalize() in PREDEFINED_MODELS_USER_MANAGED:
            model = eval(object.capitalize())
            object_ = model.objects.filter(id=pk).first()
        else:
            raise ValueError
        func(request, object_, pk, *args, **kwargs)
        return HttpResponseRedirect(f'/{object}')

    return wrap


@assigning_decorator
def assign_user_view(request, object, pk):
    if object.user:
        raise PermissionError('already taken')
    else:
        object.user = request.user
        object.save()


@assigning_decorator
def unassign_user_view(request, object, pk):
    if object.user == request.user:
        object.user = None
        object.save()
    else:
        raise PermissionError('youre not assigned to it')
