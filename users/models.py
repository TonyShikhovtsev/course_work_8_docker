from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

NULLABLE = {"null": True, "blank": True}

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone, city, avatar, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, city=city, avatar=avatar, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, city, avatar, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, phone, city, avatar, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=15, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='аватарка', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'city', 'avatar']

    objects = CustomUserManager()
