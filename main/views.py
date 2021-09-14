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


class AddIndustryView(CreateView):
    template_name = 'default_form.html'
    form_class = IndustryForm
    success_url = reverse_lazy('industry')


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
    success_url = '/'

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form_class = eval(
            f'{self.kwargs["object_to_add"].capitalize()}Form'
            if self.kwargs['object_to_add'].capitalize() in self.predefined_models else None)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form_class = eval(
            f'{self.kwargs["object_to_add"].capitalize()}Form'
            if self.kwargs['object_to_add'].capitalize() in self.predefined_models else None)
        return super().post(request, *args, **kwargs)


def industry(request):
    return render(request, 'home.html')


def company(request):
    pass


def event(request):
    pass


def statistics(request):
    pass


def top_10_users(request):
    pass


def current_event(request):
    pass
