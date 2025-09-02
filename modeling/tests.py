"""
White-box testing
"""
from django.test import TestCase  # Імпортуємо базовий клас для створення тестів у Django
from modeling.seirvd import run_simulation # Імпортуємо функцію запуску моделювання SEIRVD з файлу seirvd.py
import numpy as np # Імпортуємо бібліотеку для обчислення та аналізу числових масивів

class SEIRVDModelTest(TestCase):
    """
        Цим unit-тестом, робимо перевірку, чи зберігається сумарна чисельність населення
        всіх груп S, E, I, R, V, D ≈ 1 на всьому часовому інтервалі
    """
    def test_population_conservation(self):
        # Задаємо базові параметри моделі
        beta, sigma, gamma, nu, mu = 0.3, 0.1, 0.05, 0.01, 0.01
        # Викликаємо функцію run_simulation — отримуємо рішення системи та пікові значення
        sol, _ = run_simulation(beta, sigma, gamma, nu, mu)
        # Обчислюємо суму кожної з 6-ти груп у кожен момент часу:
        # sol.y — це матриця розміром (6, N), де кожен рядок — окрема група (S, E, I, R, V, D)
        # np.sum(...) — сумує значення по кожному стовпцю (тобто на кожному кроці часу)
        total_population = np.sum(sol.y, axis=0)
        # assertTrue — перевіряє, чи умова істинна (True).
        # np.allclose (...) — перевіряє, що всі значення total_population ≈ 1
        # atol=1e-2 - це допустима абсолютна похибка, тут вона = 0.01 (тобто це +-1%)
        self.assertTrue(np.allclose(total_population, 1.0, atol=1e-2))


