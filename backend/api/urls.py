from django.urls import path
from .views.companies import AddCompany, GetCompanies
from .views.utils import GetTop10Users, GetStatistics, GetCurrentEvent
from .views.users import GetUser, LoginUser, RegisterUser
from .views.events import GetEvents, AddEvent
from .views.industries import GetIndustries, AddIndustry, DeleteIndustry

urlpatterns = [
    path('user/register', RegisterUser.as_view()),
    path('user/login', LoginUser.as_view()),
    path('user/get_profile', GetUser.as_view()),
    path('event/add_event', AddEvent.as_view()),
    path('event/get_events', GetEvents.as_view()),
    path('industry/get_industries', GetIndustries.as_view()),
    path('industry/add_industry', AddIndustry.as_view()),
    path('industry/delete_industry', DeleteIndustry.as_view()),
    path('company/add_company', AddCompany.as_view()),
    path('company/get_companies', GetCompanies.as_view()),
    path('utils/get_statistics', GetStatistics.as_view()),
    path('utils/get_top_10_users', GetTop10Users.as_view()),
    path('utils/get_current_event', GetCurrentEvent.as_view())
]