from rest_framework.routers import DefaultRouter
from django.urls import path
from payments.apps import PaymentsConfig
from payments.views import PaymentCreateAPIView, PaymentListAPIView, PaymentRetrieveAPIView, PaymentDestroyAPIView


app_name = PaymentsConfig.name


urlpatterns = [
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payment/', PaymentListAPIView.as_view(), name='payments'),
    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment-get'),
    path('payment/delete/<int:pk>/', PaymentDestroyAPIView.as_view(), name='payment-delete')
]