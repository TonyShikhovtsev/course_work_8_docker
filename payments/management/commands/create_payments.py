
from django.core.management.base import BaseCommand
from edu.models import Course, Lesson
from users.models import User
from payments.models import Payment
from datetime import datetime

class Command(BaseCommand):
    help = 'Create sample payments'

    def handle(self, *args, **kwargs):
        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        # Создание нескольких примеров платежей
        Payment.objects.create(user=user, date=datetime.now(), course=course, amount=50.0, payment_method='cash')
        Payment.objects.create(user=user, date=datetime.now(), lesson=lesson, amount=20.0, payment_method='transfer')

        self.stdout.write(self.style.SUCCESS('Successfully created sample payments'))
