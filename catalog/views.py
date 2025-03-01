
from .models import Home, Landlord, QuantityRooms, HomeImage
from django.views import generic
from django.contrib.auth import login
from .forms import HomeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import CustomUserCreationForm

# Create your views here.

def index(request):
    """
    Домашняя страница
    """

    num_homes = Home.objects.all().count()
    num_landlords = Landlord.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_homes': num_homes, 'num_landlords': num_landlords, 'num_visits': num_visits}
    )

@login_required
def profile_view(request):
    return render(request, 'catalog/profile.html')

class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'catalog/change_password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "Your password was successfully updated!")
        return super().form_valid(form)

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически логиним пользователя
            return redirect('index')  # Редирект на главную
    else:
        form = CustomUserCreationForm()
    return render(request, 'catalog/register.html', {'form': form})

@login_required
def create_home(request):
    if request.method == "POST":
        form = HomeForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')
        if form.is_valid():
            home = form.save(commit=False)

            landlord, created = Landlord.objects.get_or_create(
                user=request.user,
                defaults={
                    "name": request.user.username,
                    "phone_number": request.user.phone_number or "Не указан",
                }
            )

            home.landlord = landlord
            home.save()
            for file in files:
                HomeImage.objects.create(home=home, image=file)
            return redirect("home-detail", pk=home.pk)
    else:
            form = HomeForm()
    return render(request, 'catalog/home_form.html', {'form': form})


class HomeListView(generic.ListView):
    model = Home
    template_name = 'catalog/home_list.html'  # Укажите путь к шаблону
    context_object_name = 'home_list'  # Имя переменной контекста для шаблона
    paginate_by = 50  # Опционально: количество элементов на странице

class HomeDetailView(generic.DetailView):
    model = Home
    template_name = 'catalog/home_detail.html'  # Укажите путь к вашему шаблону
    context_object_name = 'home'  # Опционально: имя переменной контекста

    def home_detail(request, pk):
        home = get_object_or_404(Home, pk=pk)
        return render(request, 'catalog/home_detail.html', {'home': home})

    def get_object(self, queryset=None):
        home = super().get_object(queryset)

        # Проверяем, был ли пользователь уже на этой странице
        session_key = f'viewed_home_{home.id}'
        if not self.request.session.get(session_key, False):
            home.views_count += 1
            home.save(update_fields=['views_count'])
            self.request.session[session_key] = True  # Помечаем, что он уже смотрел

        return home

class LandlordListView(generic.ListView):
    model = Landlord
    template_name = 'catalog/landlord_list.html'  # Укажите путь к шаблону
    context_object_name = 'landlords'  # Имя переменной контекста для шаблона

class LandlordDetailView(generic.DetailView):
    model = Landlord
    template_name = 'catalog/landlord_detail.html'