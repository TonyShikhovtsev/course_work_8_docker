from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=input('email:'),
            first_name='Name',
            last_name='user',
            is_staff=False,
            is_superuser=bool(input("is_superuser(0/1):"))

        )

        user.set_password('1234567!')
        user.save()