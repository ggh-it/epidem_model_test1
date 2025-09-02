import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

def seirvd_model(t, y, beta, sigma, gamma, nu, mu):
    """ Рівняння SEIRVD """
    S, E, I, R, V, D = y
    dSdt = -beta * S * I - nu * S
    dEdt = beta * S * I - sigma * E
    dIdt = sigma * E - gamma * I - mu * I
    dRdt = gamma * I
    dVdt = nu * S
    dDdt = mu * I
    return [dSdt, dEdt, dIdt, dRdt, dVdt, dDdt]

def run_simulation(beta, sigma, gamma, nu, mu):
    """ Запуск моделювання SEIRVD"""
    # Початкові умови
    S0, E0, I0, R0, V0, D0 = 0.98, 0.01, 0.01, 0.0, 0.0, 0.0
    t_start, t_end = 0, 200

    # Обчислення системи диференціальних рівнянь
    sol = solve_ivp(
        seirvd_model, (t_start, t_end), [S0, E0, I0, R0, V0, D0],
        t_eval=np.linspace(t_start, t_end, 1000), args=(beta, sigma, gamma, nu, mu)
    )

    t = sol.t  # Часові точки

    # Знаходження пікових значень та їх днів
    peaks = {
        's_peak': np.max(sol.y[0]), 's_peak_day': t[np.argmax(sol.y[0])],
        'e_peak': np.max(sol.y[1]), 'e_peak_day': t[np.argmax(sol.y[1])],
        'i_peak': np.max(sol.y[2]), 'i_peak_day': t[np.argmax(sol.y[2])],
        'r_peak': np.max(sol.y[3]), 'r_peak_day': t[np.argmax(sol.y[3])],
        'v_peak': np.max(sol.y[4]), 'v_peak_day': t[np.argmax(sol.y[4])],
        'd_peak': np.max(sol.y[5]), 'd_peak_day': t[np.argmax(sol.y[5])],
    }

    return sol, peaks
