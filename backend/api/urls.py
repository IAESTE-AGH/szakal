from django.urls import path
from .views import User, Industry, Company, Event, Statistics, Top10Users, CurrentEvent

urlpatterns = [
    path('user', User.as_view()),
    path('event', Event.as_view()),
    path('industry', Industry.as_view()),
    path('company', Company.as_view()),
    path('statistics', Statistics.as_view()),
    path('top_10_users', Top10Users.as_view()),
    path('current_event', CurrentEvent.as_view())
]