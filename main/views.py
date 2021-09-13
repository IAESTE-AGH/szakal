from django.views.generic import CreateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import template

from main.forms import IndustryForm, UserForm
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
    context = {
    "company_count": Company.objects.all().count(),
    "companies_unmanaged": Company.objects.filter(assigned_user=None).count(),
    "user_count": User.objects.all().count(),
    "user_managed_companies": Company.objects.filter(assigned_user=request.user).all()
    }

    return render(request, 'home.html', context)


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
