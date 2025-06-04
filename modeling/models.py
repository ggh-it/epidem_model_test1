from django.db import models
from django.contrib.auth.models import User

class SimulationResult(models.Model):
    """ Модель для зберігання результатів симуляції SEIRVD. """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # Дата и время запуска

    # Вхідні параметри моделі
    beta = models.FloatField(default=0.0)  # Скорость передачи инфекции Швидкість передачі
    sigma = models.FloatField(default=0.0)  # Швидкість переходу з E в I
    gamma = models.FloatField(default=0.0)  # Швидкість одужання
    nu = models.FloatField(default=0.0)  # Швидкість вакцинації
    mu = models.FloatField(default=0.0)  # Швидкість смертності

    # Вихідні дані (піки)
    s_peak = models.FloatField(default=0.0)  # Пік S
    e_peak = models.FloatField(default=0.0)  # Пік E
    i_peak = models.FloatField(default=0.0)  # Пік I
    r_peak = models.FloatField(default=0.0)  # Пік R
    v_peak = models.FloatField(default=0.0)  # Пік V
    d_peak = models.FloatField(default=0.0)  # Пік D

    # Дні, коли відбулися піки
    s_peak_day = models.FloatField(default=0.0)
    e_peak_day = models.FloatField(default=0.0)
    i_peak_day = models.FloatField(default=0.0)
    r_peak_day = models.FloatField(default=0.0)
    v_peak_day = models.FloatField(default=0.0)
    d_peak_day = models.FloatField(default=0.0)

    # JSON-поля для зберігання повного набору вхідних даних і результатів
    parameters = models.JSONField(blank=True, null=True)  # Всі вхідні параметри
    results = models.JSONField(blank=True, null=True)  # Повні результати моделювання

    def __str__(self):
        return f"Simulation by {self.user if self.user else 'Anonymous'} on {self.timestamp}"
