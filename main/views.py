import datetime

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import render
from django.http import HttpResponseRedirect
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

PREDEFINED_MODELS_STAFF = [
    'Company',
    'Industry',
    'Event'
]

PREDEFINED_MODELS = [
    'Assignment',
    'Company',
    'Contact',
    'Industry',
    'Event'
]


def assign_form(create=False, update=False, delete=False):
    def decorator(func):
        def wrap(self, request, *args, **kwargs):
            object_ = self.kwargs['object'].capitalize()
            if object_ in PREDEFINED_MODELS:
                self.model = eval(object_)
                self.object = None
                if update:
                    self.form_class = eval(f'{object_}UpdateForm')
                elif create:
                    self.form_class = eval(f'{object_}CreateForm')
                elif delete:
                    pass

                self.success_url = f'/{object_.lower()}'
                return func(self, request, *args, **kwargs)
            return ValueError

        return wrap

    return decorator


class RegisterView(CreateView):
    template_name = 'auth/user_form.html'
    form_class = UserForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        user = authenticate(
            username=self.request.POST['username'],
            password=self.request.POST['password']
        )
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)


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


class UpdateObjectView(UpdateView):
    # todo split into predefined_models for staff and for normal user
    template_name = 'default_form.html'

    # todo IMPORTANT: figure out permissions and who can modify what, maybe create more form types

    @assign_form(update=True)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @assign_form(update=True)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AddObjectView(CreateView):
    # todo split into predefined_models for staff and for normal user
    template_name = 'default_form.html'

    @assign_form(create=True)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @assign_form(create=True)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DeleteObjectView(DeleteView):
    template_name = 'default_form.html'

    @assign_form(delete=True)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @assign_form(delete=True)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


def assign_user_view(request, object, pk):
    if object.capitalize() in PREDEFINED_MODELS_USER_MANAGED:
        model = eval(object.capitalize())
        object_ = model.objects.filter(id=pk).first()
        if object_.user:
            raise PermissionError('already taken')
        else:
            object_.user = request.user
            object_.save()
    else:
        raise ValueError
    return HttpResponseRedirect(f'/{object}')
