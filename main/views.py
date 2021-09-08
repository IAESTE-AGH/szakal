from django.views.generic import CreateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from main.forms import IndustryForm, UserForm


class RegisterView(CreateView):
    template_name = 'auth/user_form.html'
    form_class = UserForm
    success_url = reverse_lazy('home')


class AddIndustryView(CreateView):
    template_name = 'default_form.html'
    form_class = IndustryForm
    success_url = reverse_lazy('industry')


def home(request):
    return render(request, 'home.html')


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


def login(request):
    pass
