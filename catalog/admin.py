from django.contrib import admin
from .models import Home, QuantityRooms, Landlord

# Register your models here.

# admin.site.register(Home)
# admin.site.register(QuantityRooms)
# admin.site.register(Landlord)

@admin.register(Landlord)
class LandlordAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number')
    fields = ['name', 'phone_number']

@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'landlord', 'quantity', 'city', 'street', 'house_number', 'price')
    list_filter = ('city', 'quantity', 'price')  # Добавляем фильтрацию
    search_fields = ('title', 'description', 'landlord__name')  # Поиск
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'landlord', 'quantity', 'price'),
        }),
        ('Адрес', {
            'fields': ('city', 'street', 'house_number', 'apartment_number'),
        }),
        ('Другое', {
            'fields': ('original_address',),
        }),
    )

@admin.register(QuantityRooms)
class QuantityRoomAdmin(admin.ModelAdmin):
    pass

