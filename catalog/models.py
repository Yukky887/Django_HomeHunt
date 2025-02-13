from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

from django.contrib.auth import get_user_model
User = get_user_model()

class QuantityRooms(models.Model):
    """
    Модель для ввода количества комнат в квартире (например, студия, однокомнатная, двухкомнатная и т. д.).
    """
    name = models.CharField(
        max_length=200,
        help_text="Введите количество комнат (например, студия, однокомнатная, двухкомнатная и т. д.)."
    )

    def __str__(self):
        return self.name

class HomeImage(models.Model):
    home = models.ForeignKey('Home', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='home_images/', help_text="Загрузите изображение квартиры")

class Home(models.Model):
    """
    Модель, представляющая квартиру (но не конкретный экземпляр квартиры).
    """
    title = models.CharField(
        max_length=200,
        help_text="Краткое описание квартиры"
    )
    landlord = models.ForeignKey(
        'Landlord',
        on_delete=models.SET_NULL,
        null=True,
        help_text="Арендодатель квартиры"
    )
    description = models.TextField(
        max_length=1000,
        help_text="Введите описание квартиры"
    )
    price = models.CharField(
        max_length=10,
        help_text="Цена аренды"
    )
    quantity = models.ForeignKey(
        'QuantityRooms',
        on_delete=models.SET_NULL,
        null=True,
        help_text="Выберите количество комнат"
    )
    # Адрес квартиры
    city = models.CharField(
        max_length=100,
        help_text="Город, где находится квартира"
    )
    street = models.CharField(
        max_length=200,
        help_text="Улица, где находится квартира"
    )
    house_number = models.CharField(
        max_length=10,
        help_text="Номер дома"
    )
    apartment_number = models.CharField(
        max_length=10,
        help_text="Номер квартиры",
        blank=True
    )
    # Уникальный URL квартиры
    original_address = models.URLField(
        unique=True,
        blank = True,
        null=True,
        help_text="Уникальный URL с оригинального сайта"
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Уникальный ID квартиры"
    )
    # Счётчик просмотров
    views_count = models.IntegerField(
        default=0
    )

    class Meta:
        ordering = ["city", "street", "house_number", "price"]

    def __str__(self):
        return f"{self.title} - {self.city}, {self.street}, {self.house_number}, {self.price}"

    def get_absolute_url(self):
        """
        Возвращает URL для доступа к конкретной квартире.
        """
        return reverse('home-detail', args=[str(self.id)])



class Landlord(models.Model):
    """
    Модель представляющая арендодателя
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="landlord", null=True, blank=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)

    def get_absolute_url(self):
        """
         Возвращает URL-адрес для доступа к конкретному экземпляру арендодателя.
        """
        return reverse('landlord-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.name}, {self.phone_number}"