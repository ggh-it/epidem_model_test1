import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render, redirect, get_object_or_404
from .seirvd import run_simulation
from .models import SimulationResult
from django.http import HttpResponse
import csv


def model_view(request):
    """ Веб-сторінка для запуску моделі SEIRVD"""
    if request.method == "POST":
        # Отримуємо параметри із форми
        beta = float(request.POST.get("beta", 0.3))
        sigma = float(request.POST.get("sigma", 0.1))
        gamma = float(request.POST.get("gamma", 0.05))
        nu = float(request.POST.get("nu", 0.01))
        mu = float(request.POST.get("mu", 0.01))

        # Запуск симуляції
        sol, peaks = run_simulation(beta, sigma, gamma, nu, mu)

        # Збереження результатів до бази даних
        result = SimulationResult.objects.create(
            user=request.user if request.user.is_authenticated else None,
            beta=beta, sigma=sigma, gamma=gamma, nu=nu, mu=mu,
            s_peak=peaks["s_peak"], e_peak=peaks["e_peak"], i_peak=peaks["i_peak"],
            r_peak=peaks["r_peak"], v_peak=peaks["v_peak"], d_peak=peaks["d_peak"],
            s_peak_day=peaks["s_peak_day"], e_peak_day=peaks["e_peak_day"],
            i_peak_day=peaks["i_peak_day"], r_peak_day=peaks["r_peak_day"],
            v_peak_day=peaks["v_peak_day"], d_peak_day=peaks["d_peak_day"],
            parameters={"beta": beta, "sigma": sigma, "gamma": gamma, "nu": nu, "mu": mu},
            results={"solution": sol.y.tolist(), "time": sol.t.tolist()}
        )

        # Генерація графіку
        plot_url = generate_plot(sol, peaks)

        # Передаємо дані до шаблону
        return render(request, "modeling/results.html", {
            "peaks": peaks,
            "plot_url": plot_url,
            "parameters": result.parameters,  # Передача параметрів у шаблон
            "user": request.user,
            "simulation": result
        })

    return render(request, "modeling/form.html")


def generate_plot(sol, peaks):
    """ Генеруємо графік з піковими значеннями та розміщуємо легенду за межами графіку """
    fig, ax = plt.subplots(figsize=(8, 5))
    labels = ["S (сприйнятливі)", "E (інкубовані)", "I (інфіковані)", "R (одужалі)",
              "V (вакциновані)", "D (померлі)"]
    colors = ['blue', 'orange', 'red', 'green', 'purple', 'black']

    for i in range(6):
        ax.plot(sol.t, sol.y[i], label=labels[i], color=colors[i])

        # Пікові точки
        peak_day = peaks[f"{labels[i][0].lower()}_peak_day"]
        peak_value = peaks[f"{labels[i][0].lower()}_peak"]
        ax.scatter(peak_day, peak_value, color=colors[i], s=50, marker='o', label=f"Пік {labels[i]}")

    ax.set_xlabel("Час")
    ax.set_ylabel("Частка населення")
    ax.set_title("Результати моделювання SEIRVD")

    # Додаємо сітку
    ax.grid(True, linestyle="--", linewidth=0.5)

    # Переміщення легенди за межі графіку
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    fig.subplots_adjust(right=0.75)  # Зміщення кордону графіка для обліку легенди

    # Зберігання у буфер
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    string = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()
    return f"data:image/png;base64,{string}"


def simulation_detail(request, pk):
    """ Сторінка з деталями симуляції """
    simulation = get_object_or_404(SimulationResult, pk=pk)

    # Упорядковані параметри
    ordered_parameters = {
        "beta": simulation.beta,
        "sigma": simulation.sigma,
        "gamma": simulation.gamma,
        "nu": simulation.nu,
        "mu": simulation.mu,
    }

    # Підготовка даних для таблиці
    time_series = simulation.results.get("time", [])
    solutions = simulation.results.get("solution", [])

    if solutions and len(solutions) == 6:
        simulation_data = list(zip(
            time_series,
            solutions[0], solutions[1], solutions[2],
            solutions[3], solutions[4], solutions[5]
        ))
    else:
        simulation_data = []

    # Генерація графіку на основі збережених даних
    plot_url = generate_saved_plot(simulation)

    return render(request, "modeling/simulation_detail.html", {
        "simulation": simulation,
        "ordered_parameters": ordered_parameters,  # Передаємо впорядковані параметри
        "simulation_data": simulation_data,
        "plot_url": plot_url,
        "user": request.user
    })


def generate_saved_plot(simulation):
    """ Відновлює графік з збережених даних та додає пікові точки. """
    fig, ax = plt.subplots(figsize=(8, 5))

    t = simulation.results.get("time", [])
    solution = simulation.results.get("solution", [])
    labels = ["S (сприйнятливі)", "E (інкубовані)", "I (інфіковані)", "R (одужалі)",
              "V (вакциновані)", "D (померлі)"]
    colors = ['blue', 'orange', 'red', 'green', 'purple', 'black']

    if not t or not solution or len(solution) != 6:
        print("Помилка: дані для графіка відсутні або некоректні")
        return ""

    for i in range(6):
        ax.plot(t, solution[i], label=labels[i], color=colors[i])

        # Додаємо пікові точки, якщо вони є
        peak_day = getattr(simulation, f"{labels[i][0].lower()}_peak_day", None)
        peak_value = getattr(simulation, f"{labels[i][0].lower()}_peak", None)

        if peak_day is not None and peak_value is not None:
            ax.scatter(peak_day, peak_value, color=colors[i], s=50, marker='o', label=f"Пік {labels[i]}")

    ax.set_xlabel("Час")
    ax.set_ylabel("Частка населення")
    ax.set_title("Результати моделювання SEIRVD")

    # Додаємо сітку
    ax.grid(True, linestyle="--", linewidth=0.5)

    # Переміщення легенди за межі графіку
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    fig.subplots_adjust(right=0.75)

    # Зберігання у буфер
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    string = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()

    print(f"Графік згенерований, довжина base64: {len(string)}")  # Перевірка, чи створюється зображення
    return f"data:image/png;base64,{string}"


def home(request):
    return render(request, 'home.html')


def download_graph(request, pk):
    """ Дає можливість користувачу завантажити графік симуляції """
    simulation = get_object_or_404(SimulationResult, pk=pk)
    image_data = generate_saved_plot(simulation)  # Генерация графикаГенерація графіку

    if not image_data:
        return HttpResponse("Помилка: графік не знайдено", status=404)

    image_bytes = base64.b64decode(image_data.split(",")[1])

    response = HttpResponse(image_bytes, content_type="image/png")
    response["Content-Disposition"] = f'attachment; filename="simulation_{pk}_graph.png"'
    return response


def export_simulation_csv(request, pk):
    """ Експортує результати симуляції до CSV-файлу з виправленим кодуванням """
    simulation = get_object_or_404(SimulationResult, pk=pk)

    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = f'attachment; filename="simulation_{pk}_data.csv"'

    writer = csv.writer(response, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Заголовки стовпців (заміна кодування та можливих артефактів)
    writer.writerow(["Час", "S (сприйнятливі)", "E (інкубовані)",
                     "I (інфіковані)", "R (одужалі)",
                     "V (вакциновані)", "D (померлі)"])

    time_series = simulation.results.get("time", [])
    solutions = simulation.results.get("solution", [])

    if solutions and len(solutions) == 6:
        for i in range(len(time_series)):
            row = [
                time_series[i],
                solutions[0][i], solutions[1][i], solutions[2][i],
                solutions[3][i], solutions[4][i], solutions[5][i]
            ]
            writer.writerow(row)

    return response
