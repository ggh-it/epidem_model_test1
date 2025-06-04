from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import SimulationResult

@admin.register(SimulationResult)
class SimulationResultAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "timestamp")  # Какие поля показывать в списке
    list_filter = ("user", "timestamp")  # Фильтры справа
    search_fields = ("user__username",)  # Поиск по пользователю

admin.site.site_header = "SEIRVD Адмін-панель"  # Изменение заголовка в панели админа
admin.site.site_title = "SEIRVD"
