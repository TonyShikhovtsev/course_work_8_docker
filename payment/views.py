from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payment.serializers import PaymentSerializer
from payment.models import Payment
from edu.models import Course, Lesson
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from edu.services import StripePayments


class PaymentCourseCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        new_payment = serializer.save()
        new_payment.user = self.request.user
        new_payment.paid_course = Course.objects.get(pk=self.kwargs.get('pk'))
        new_payment.save()
        price = new_payment.paid_course.price
        stripe_payment = StripePayments(user=new_payment.user, course=new_payment.paid_course, amount=price)
        new_payment.stripe_session = stripe_payment.create_session()['session_id']
        new_payment.url = stripe_payment.create_session()['url_pay']
        new_payment.save()


class PaymentLessonCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        new_payment = serializer.save()
        new_payment.user = self.request.user
        new_payment.paid_lesson = Lesson.objects.get(pk=self.kwargs.get('pk'))
        new_payment.save()
        price = new_payment.paid_lesson.price
        stripe_payment = StripePayments(user=new_payment.user, course=new_payment.paid_lesson, amount=price)
        new_payment.stripe_session = stripe_payment.create_session()['session_id']
        new_payment.url = stripe_payment.create_session()['url_pay']
        new_payment.save()


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('paid_course', 'paid_lesson', 'pay_type')
    ordering_fields = ('date_of_payment',)


class PaymentRetrieveAPIView(RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        payment = self.queryset.get(pk=self.kwargs.get('pk'))
        session_id = payment.stripe_session
        status_paid = StripePayments.retrieve_session(session_id=session_id)
        payment.status_paid = status_paid
        payment.save()
        return Response({'status': payment.status_paid}, )