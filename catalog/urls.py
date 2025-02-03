from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import profile_view, CustomPasswordChangeView
urlpatterns = [
    path('', views.index, name='index'),  # Главная страница каталога
    path('homes/', views.HomeListView.as_view(), name='homes'),
    path('landlords/', views.LandlordListView.as_view(), name='landlords'),
    path('landlord/<int:pk>/', views.LandlordDetailView.as_view(), name='landlord-detail'),
    path('home/<uuid:pk>/', views.HomeDetailView.as_view(), name='home-detail'),

    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='catalog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Профиль
    path('register/', views.register, name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile/change-password/', CustomPasswordChangeView.as_view(), name='change_password')
]



