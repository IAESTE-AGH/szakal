from django.views.generic import CreateView, ListView
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

from main.forms import UserForm
from main.models import Company, Industry

register = template.Library()

PREDEFINED_MODELS_USER = [
    'Assignment',
    'Company',
    'Contact'
]

PREDEFINED_MODELS = [
    'Assignment',
    'Company',
    'Contact',
    'Industry'
]


def assign_form(func):
    def wrap(self, request, *args, **kwargs):
        self.object = None
        self.form_class = eval(
            f'{self.kwargs["object_to_add"].capitalize()}Form'
            if self.kwargs['object_to_add'].capitalize() in self.predefined_models else None)
        return func(self, request, *args, **kwargs)

    return wrap


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
        self.model = self.kwargs['model'].capitalize()

        if self.model in PREDEFINED_MODELS:
            self.template_name = f'{self.model.lower()}.html'
        else:
            raise ValueError

        whos = self.kwargs['whos']

        if whos == 'all':
            model = eval(self.model)
            return model.objects.all()

        elif self.model in PREDEFINED_MODELS_USER:
            model = eval(self.model)
            if whos == 'my':
                return model.objects.filter(user=self.request.user)
            elif whos == 'taken':
                return model.objects.filter(user__isnull=False)
            else:
                raise ValueError
        else:
            raise ValueError


class AddObjectView(CreateView):
    # todo split into predefined_models for staff and for normal user
    predefined_models = [
        'Company',
        'Industry'
    ]
    template_name = 'default_form.html'
    # todo decide what to do with success_url
    success_url = '/'

    @assign_form
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @assign_form
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
