from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from django.contrib.auth import views as auth_views
from modeling.views import home  # Імпортуємо представлення для головної сторінки

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Головна сторінка
    path("modeling/", include("modeling.urls")),
    path('users/', include('users.urls')),  # Підключаємо маршрути користувачів
    path('accounts/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # Використовуємо кастомний шаблон
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("", lambda request: redirect("login")),  # Перенаправлення на сторінку входу
]

