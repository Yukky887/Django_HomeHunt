# Generated by Django 4.2.17 on 2025-02-10 11:24

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('title', models.CharField(help_text='Краткое описание квартиры', max_length=200)),
                ('description', models.TextField(help_text='Введите описание квартиры', max_length=1000)),
                ('price', models.CharField(help_text='Цена аренды', max_length=10)),
                ('city', models.CharField(help_text='Город, где находится квартира', max_length=100)),
                ('street', models.CharField(help_text='Улица, где находится квартира', max_length=200)),
                ('house_number', models.CharField(help_text='Номер дома', max_length=10)),
                ('apartment_number', models.CharField(blank=True, help_text='Номер квартиры', max_length=10)),
                ('original_address', models.URLField(help_text='Уникальный URL с оригинального сайта', unique=True)),
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID квартиры', primary_key=True, serialize=False)),
                ('views_count', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['city', 'street', 'house_number', 'price'],
            },
        ),
        migrations.CreateModel(
            name='QuantityRooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите количество комнат (например, студия, однокомнатная, двухкомнатная и т. д.).', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Landlord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='landlord', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HomeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Загрузите изображение квартиры', upload_to='home_images/')),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.home')),
            ],
        ),
        migrations.AddField(
            model_name='home',
            name='landlord',
            field=models.ForeignKey(help_text='Арендодатель квартиры', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.landlord'),
        ),
        migrations.AddField(
            model_name='home',
            name='quantity',
            field=models.ForeignKey(help_text='Выберите количество комнат', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.quantityrooms'),
        ),
    ]
