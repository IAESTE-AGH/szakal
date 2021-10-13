from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),  # todo test

    path('<str:object>/add/', staff_member_required(views.AddObjectView.as_view()), name='add'),

    path('<str:object>/update/<int:pk>/', staff_member_required(views.UpdateObjectView.as_view()), name='update'),

    path('<str:object>/list/<str:whos>/', views.ListObjectsView.as_view(), name='list'),
    path('<str:object>/', views.ListObjectsView.as_view(), name='list_all'),

    path('', views.Home.as_view(), name='home')
]
