from django import template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from main.forms import *
from main.helpers.filtering_algorithm import filter_by_word
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
    'Event',
    'User'
]


def assign_form(obj="", create=False, update=False, delete=False):
    def decorator(func):
        def wrap(self, request, *args, **kwargs):
            if not obj:
                _object = "".join([el.capitalize() for el in self.kwargs['object'].split('-')])
            else:
                _object = "".join([el.capitalize() for el in obj.split('-')])
            if _object in PREDEFINED_MODELS:
                if not request.user.is_staff and _object not in PREDEFINED_MODELS_USER:
                    return PermissionError

                self.model = eval(_object)
                self.object = None
                if update:
                    if request.user.is_staff or eval(_object).objects.get(id=kwargs['pk']).user == request.user:
                        self.form_class = eval(f'{_object}UpdateForm')
                    else:
                        return PermissionError
                elif create:
                    self.form_class = eval(f'{_object}CreateForm')
                elif delete:
                    pass

                self.success_url = f'/{_object.lower()}/list'
                if _object.lower() == 'contact':
                    self.success_url = f'/company/my'

                return func(self, request, *args, **kwargs)
            return ValueError

        return wrap

    return decorator


def handle_extended_form(create=False, update=False, obj=""):
    def decorator(func):
        def wrap(self, request, *args, **kwargs):
            if not obj:
                _object = "".join([el.capitalize() for el in self.kwargs['object'].split('-')])
            else:
                _object = "".join([el.capitalize() for el in obj.split('-')])
            if issubclass(self.form_class, ExtendedForm):
                form = self.form_class(request.POST)
                if form.is_valid():
                    if create:
                        if _object in PREDEFINED_MODELS_USER_MANAGED:
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

                    if update:
                        return func(self, request, *args, **kwargs)
                    else:
                        return HttpResponseRedirect(self.success_url)
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
            "stats": {
                "company_count": Company.objects.all().count(),
                "companies_unmanaged": Company.objects.filter(user=None).count(),
                "user_count": User.objects.all().count(),
                "user_managed_companies": Company.objects.filter(user=request.user).all()
            },
            "events": {
                "currentEvents": Event.objects.filter(active=True)
            },
            "users": User.objects.annotate(companyCount=Count('company')).order_by('-companyCount')[:10],
            "myCompanies": Contact.objects.select_related('company', 'status').filter(user=request.user)
        }

        return render(request, self.template, context)

    @assign_form(update=True)
    @handle_extended_form(update=True)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, {**kwargs})


class ProfileView(LoginRequiredMixin, View):
    template = 'user.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number
        }
        return render(request, self.template, context)


class Filtered(LoginRequiredMixin, View):
    # template = 'company.html'

    def post(self, request, *args, **kwargs):
        model = self.kwargs['object'].capitalize()
        searched = request.POST.get("searched")
        status = request.POST.get("search_status")

        if model in PREDEFINED_MODELS:
            self.template = f'{model.lower()}.html'
            if status == 'my':
                context = {
                    "object_list": filter_by_word(searched, eval(model).objects.filter(user=self.request.user))
                }

            elif status == 'taken':
                context = {
                    "object_list": filter_by_word(searched, eval(model).objects.filter(user__isnull=False))
                }
            elif status == 'not_taken':
                context = {
                    "object_list": filter_by_word(searched, eval(model).objects.filter(user__isnull=True))
                }
            elif status == 'active':
                context = {
                    "object_list": filter_by_word(searched, eval(model).objects.filter(active=True))
                }
            elif status == 'not_active':
                context = {
                    "object_list": filter_by_word(searched, eval(model).objects.filter(active=False))
                }
            else:
                context = {
                    "object_list": filter_by_word(searched, eval(model).objects.all())
                }
            return render(request, self.template, context)
        else:
            return Exception


class ListObjectsView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        model = self.kwargs['object'].capitalize()
        if model in PREDEFINED_MODELS:
            self.template_name = f'{model.lower()}.html'
        else:
            raise ValueError

        sort_by = self.request.GET.get('sort_by', 'id')
        sort_order = '-' + sort_by if not self.request.GET.get('order') == 'asc' else sort_by
        whos = self.kwargs.get('whos')
        if not whos:
            model = eval(model)
            self.model = model
            return model.objects.all().order_by(sort_order)
        elif model == 'Event':
            model = eval(model)
            self.model = model
            if whos == 'local':
                return model.objects.filter(local=True).order_by(sort_order)
            elif whos == 'global':
                return model.objects.filter(local=False).order_by(sort_order)
            elif whos == 'active':
                return model.objects.filter(active=True).order_by(sort_order)
            else:
                raise ValueError
        elif model in PREDEFINED_MODELS_USER_MANAGED:
            model = eval(model)
            self.model = model
            if whos == 'my':
                return model.objects.filter(user=self.request.user).order_by(sort_order)
            elif whos == 'taken':
                return model.objects.filter(user__isnull=False).order_by(sort_order)
            elif whos == 'free':
                return model.objects.filter(user__isnull=True).order_by(sort_order)
            else:
                raise ValueError
        else:
            raise ValueError

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = self.model._meta.get_fields()

        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)

        model = self.kwargs['object'].capitalize()
        searched = request.POST.get("searched")
        print(request.POST)

        if model in PREDEFINED_MODELS:
            self.template = f'{model.lower()}.html'
            context["object_list"] = filter_by_word(searched, eval(model).objects.all())
            return render(request, self.template, context)
        else:
            return Exception


class UpdateEventActiveView(LoginRequiredMixin, UpdateView):
    template_name = 'eventSetActive.html'

    @assign_form(update=True)
    def get(self, request, *args, **kwargs):
        return Event.objects.filter(active=False)

    @assign_form(update=True)
    @handle_extended_form(update=True)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


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
        return HttpResponseRedirect(f'/{object}/list')

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


def company_details(request, object, pk):
    context = {
        "company": get_object_or_404(Company, pk=pk),
        "contacts": Contact.objects.filter(company=pk).order_by('-date'),
        "contact_persons": ContactPerson.objects.filter(company=pk)
    }

    return render(request, 'company_details.html', context)


class AddContactView(LoginRequiredMixin, CreateView):
    template = 'contact_form.html'

    def get(self, request, *args, **kwargs):
        company_id = request.GET['company']
        context = {
            "company": Company.objects.get(id=company_id),
            "contact_people": ContactPerson.objects.filter(company_id=company_id),
            "types": ContactType.objects.all(),
            "events": Event.objects.all(),
            "statuses": Status.objects.all(),
            "categories": Category.objects.all(),
        }

        return render(request, self.template, context)

    @assign_form(create=True, obj='contact')
    @handle_extended_form(create=True, obj='contact')
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, {**kwargs})


class AddContactPersonView(LoginRequiredMixin, CreateView):
    template = 'contact_person_form.html'
    company_id = None

    def get(self, request, *args, **kwargs):
        company_id = request.GET['company']
        context = {
            "company": Company.objects.get(id=company_id),
            "contact_people": ContactPerson.objects.filter(company_id=company_id),
            "types": ContactType.objects.all(),
            "events": Event.objects.all(),
            "statuses": Status.objects.all(),
            "categories": Category.objects.all(),
        }

        return render(request, self.template, context)

    @assign_form(create=True, obj='contact-person')
    @handle_extended_form(create=True, obj='contact-person')
    def post(self, request, *args, **kwargs):
        super().post(request, *args, {**kwargs})
        company_id = request.POST.get('company', '/')
        return HttpResponseRedirect(f'/company/{company_id}/company_details/')