from django.views.generic import CreateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import template

from main.forms import IndustryForm, UserForm, CompanyForm
from main.models import Company

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


def home(request):
    if request.user.is_authenticated:
        context = {
            "company_count": Company.objects.all().count(),
            "companies_unmanaged": Company.objects.filter(assigned_user=None).count(),
            "user_count": User.objects.all().count(),
            "user_managed_companies": Company.objects.filter(assigned_user=request.user).all()
        }

        return render(request, 'home.html', context)
    else:
        return HttpResponseRedirect('/login/')


class AddObjectView(CreateView):
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
