from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import SimulationResult

@admin.register(SimulationResult)
class SimulationResultAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "timestamp")  # Які поля відображати у списку
    list_filter = ("user", "timestamp")  # Фільтри справа
    search_fields = ("user__username",)  # Пошук по користувачу

admin.site.site_header = "SEIRVD Адмін-панель"  # Зміна заголовку в панелі адміна
admin.site.site_title = "SEIRVD"
