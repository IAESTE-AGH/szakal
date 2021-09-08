from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('event/', views.event, name='event'),
    path('industry/', views.industry, name='industry'),
    path('industry/add/', views.AddIndustryView.as_view(), name='add_industry'),
    path('company/', views.company, name='company'),
    path('statistics/', views.statistics, name='statistics'),
    path('top_10_users/', views.top_10_users, name='top_10_users'),
    path('current_event/', views.current_event, name='current_event'),
    path('/', views.home, name='home')
]
