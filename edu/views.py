from requests import Response
from rest_framework import viewsets, generics
from rest_framework.generics import DestroyAPIView, CreateAPIView, RetrieveAPIView

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .permissions import IsSubscriber


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()



class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()


class SubscriptionCreateAPIView(CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer, *args, **kwargs):
        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        pk = self.kwargs.get('pk')
        new_subscription.course = Course.objects.get(pk=pk)
        new_subscription.save()

class SubscriptionDestroyAPIView(DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsSubscriber]


class LessonPaymentAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        payment_link = serializer.data['payment_link']
        return Response({'payment_link': payment_link})


class CoursePaymentAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        payment_link = serializer.data['payment_link']
        return Response({'payment_link': payment_link})