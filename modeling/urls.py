from django.urls import path
from .views import model_view, simulation_detail, download_graph, export_simulation_csv

urlpatterns = [
    path("simulate/", model_view, name="simulate"),
    path('simulation/<int:pk>/', simulation_detail, name='simulation_detail'),
    path('simulation/<int:pk>/download_graph/', download_graph, name='download_graph'),
    path('simulation/<int:pk>/export_csv/', export_simulation_csv, name='export_csv'),
]
