from django.db import models
from django.contrib.auth.models import AbstractUser



NULLABLE = {"null": True, "blank": True}
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, verbose_name='Телефона', **NULLABLE)
    city = models.CharField(max_length=70, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='products/', verbose_name='Аватар', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name="активный")
    moderator = models.BooleanField(default=False, verbose_name='Модератор')



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []