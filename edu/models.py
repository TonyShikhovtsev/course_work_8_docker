from django.db import models

from users.models import NULLABLE, User


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='название курса')
    image = models.ImageField(upload_to='courses/', verbose_name='изображение', **NULLABLE)
    description = models.TextField(verbose_name='описание курса',  **NULLABLE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, **NULLABLE)


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'



class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='название урока')
    image = models.ImageField(upload_to='lessons/', verbose_name='изображение', **NULLABLE)
    description = models.TextField(verbose_name='описание урока', **NULLABLE)
    video_link = models.TextField(verbose_name='ссылка на видео',  **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'



class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="курс")

    def __str__(self):
        return f'{self.user.email} подписан на {self.course.title}'