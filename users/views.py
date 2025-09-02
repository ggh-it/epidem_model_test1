from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator  # Додаємо пагінатор
from modeling.models import SimulationResult  # Імпортуємо модель результатів


def register(request):
    # Якщо користувач вже авторизований, перенаправляємо на профіль
    if request.user.is_authenticated:
        return redirect('profile')

    # Обробка POST-запиту (надсилання форми реєстрації)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Зберігаємо нового користувача
            username = form.cleaned_data.get('username')
            messages.success(request, f'Акаунт {username} був успішно створений!')
            login(request, user)  # Відразу авторизуємо нового користувача
            return redirect('profile')  # Перенаправляємо на профіль
    else:
        form = UserCreationForm()  # Порожня форма при GET-запиті

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    # Отримуємо всі симуляції поточного користувача
    simulations_list = SimulationResult.objects.filter(user=request.user).order_by('-timestamp')

    # Додаємо пагінацію (10 симуляцій на сторінку)
    paginator = Paginator(simulations_list, 10)
    page_number = request.GET.get('page')
    simulations = paginator.get_page(page_number)

    return render(request, 'users/profile.html', {'simulations': simulations})


@login_required
def delete_simulation(request, pk):
    """ Видаляє вибрану симуляцію користувача """
    simulation = get_object_or_404(SimulationResult, pk=pk, user=request.user)

    if request.method == "POST":
        simulation.delete()
        messages.success(request, "Симуляція успішно видалена!")
        return redirect('profile')

    return render(request, "users/confirm_delete.html", {"simulation": simulation})


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')  # Перенаправляємо в особистий кабінет
        return super().dispatch(request, *args, **kwargs)
