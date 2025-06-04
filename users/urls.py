from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

urlpatterns = [
    # Реєстрація та автентифікація
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Особистий кабінет
    path('profile/', views.profile, name='profile'),
    path('profile/delete_simulation/<int:pk>/', views.delete_simulation, name='delete_simulation'),

    # Зміна пароля
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
]
