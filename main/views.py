from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# from .forms import CreateUserForm


class CreateUserView(CreateView):
    model = User
    template_name = 'auth/user_form.html'
    fields = '__all__'
    success_url = '/user'

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     context = {'form': CreateUserForm()}
    #     return render(request, 'auth/user_form.html', context)
    #
    # def post(self, request, *args, **kwargs):
    #     form = CreateUserForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         user.save()
    #         return HttpResponseRedirect(reverse_lazy('users:detail', args=[user.id]))
    #     return render(request, 'create_user.html', {'form': form})


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
