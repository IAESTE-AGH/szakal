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
            "companies_unmanaged": Company.objects.filter(assigned_user=None).count(),
            "user_count": User.objects.all().count(),
            "user_managed_companies": Company.objects.filter(assigned_user=request.user).all()
        }
        return render(request, self.template, context)


class Companies(LoginRequiredMixin, ListView):
    template_name = 'companies.html'
    model = Company


class MyCompanies(Companies):
    def get_queryset(self):
        return Company.objects.filter(assigned_user=self.request.user)


class AllCompanies(Companies):
    def get_queryset(self):
        return Company.objects.all()


class TakenCompanies(Companies):
    def get_queryset(self):
        return Company.objects.filter(assigned_user__isnull=False)


class Industries(LoginRequiredMixin, ListView):
    template_name = 'industries.html'
    model = Industry


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
