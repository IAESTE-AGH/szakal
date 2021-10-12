from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),  # todo test

    path('add/<str:object_to_add>/', staff_member_required(views.AddObjectView.as_view()), name='add'),

    path('list/<str:model>/<str:whos>', views.ListObjectsView.as_view(), name='list'),

    path('', views.Home.as_view(), name='home')
]
