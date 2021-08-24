from django.views.generic import CreateView
from django.contrib.auth.models import User


class CreateUser(CreateView):
    model = User
    fields = ['username']


def industry(request):
    pass


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
