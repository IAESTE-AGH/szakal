from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('user/', views.ProfileView.as_view(), name='profile'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),  # todo test

    path('<str:object>/add/', views.AddObjectView.as_view(), name='add'),
    path('<str:object>/list/search/', views.Filtered.as_view(), name='filtered'),

    path('<str:object>/list/', views.ListObjectsView.as_view(), name='list_all'),
    path('<str:object>/<int:pk>/delete/', staff_member_required(views.DeleteObjectView.as_view()), name='delete'),
    path('<str:object>/<int:pk>/assign/', views.assign_user_view, name='assign'),
    path('<str:object>/<int:pk>/unassign/', views.unassign_user_view, name='unassign'),
    path('<str:object>/<int:pk>/', views.UpdateObjectView.as_view(), name='update'),

    path('<str:object>/<str:whos>/', views.ListObjectsView.as_view(), name='list'),



    path('', views.Home.as_view(), name='home')
]
