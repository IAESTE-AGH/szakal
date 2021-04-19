from django.urls import path
from . import views

urlpatterns = [
    path('user', views.user, name='user'),
    path('event', views.event, name='event'),
    path('industry', views.industry, name='industry'),
    path('company', views.company, name='company'),
    path('statistics', views.statistics, name='statistics'),
    path('top_10_users', views.top_10_users, name='top_10_users'),
    path('current_event', views.current_event, name='current_event')
]