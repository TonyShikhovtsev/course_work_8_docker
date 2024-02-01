import django_filters

from .models import Payment
from edu.models import Course
from edu.models import Lesson

class PaymentFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=(
            ('date', 'date'),
        ),
        field_labels={
            'date': 'Дата',
        },
        label='Сортировать'
    )

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method']
