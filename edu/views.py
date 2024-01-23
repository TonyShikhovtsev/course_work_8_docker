from datetime import timedelta, datetime
import pytz

from requests import Response
from rest_framework import viewsets, generics
from rest_framework.generics import DestroyAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .permissions import IsSubscriber, IsOwner, IsModerator
from .tasks import subscriber_notice



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


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    класс для изменения урока на основе generics
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    # доступно только авторизованным пользователям, модераторам или владельцам
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def perform_update(self, serializer):
        """
        Определяем порядок изменения урока
        """
        changed_lesson = serializer.save()
        date_time_now = datetime.now()  # получаем текущие дату и время
        moscow_timezone = pytz.timezone('Europe/Moscow')  # устанавливаем часовой пояс
        date_now = date_time_now.astimezone(moscow_timezone)  # устанавливаем текущую дату с учетом часового пояса

        # если дата последнего изменения урока существует, проверяем условие запуска отложенной задачи
        if changed_lesson.lesson_datetime_changing:

            # устанавливаем дату последнего изменения урока с учетом часового пояса
            lesson_last_change_date = changed_lesson.lesson_datetime_changing.astimezone(moscow_timezone)

            # если текущее время больше времени последнего изменения урока на количество часов
            if abs(date_now - lesson_last_change_date) > timedelta(hours=4):
                # запускаем отложенную задачу по информированию подписчиков курса о изменениях уроков курса
                subscriber_notice.delay(changed_lesson.course_id)

        # заносим текущие дату и время в последние изменения урока
        changed_lesson.lesson_datetime_changing = date_now
        changed_lesson.save()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    класс для удаления одного мото на основе generics
    """
    queryset = Lesson.objects.all()

    # доступно только авторизованным владельцам
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """
    класс для создания подписки
    """
    serializer_class = SubscriptionSerializer

    # доступно только авторизованным пользователям
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Определяем порядок создания нового объекта
        """
        new_subscription = serializer.save()
        new_subscription.user = self.request.user  # задаем подписчика
        new_subscription.save()


class SubscriptionListAPIView(generics.ListAPIView):
    """
    класс для вывода списка подписок
    """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    # доступно только авторизованным пользователям, модераторам или владельцам
    # permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    permission_classes = [AllowAny]


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    """
    класс для изменения подписки
    """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    # доступно только авторизованным пользователям, модераторам или владельцам
    permission_classes = [IsAuthenticated, IsModerator | IsSubscriber]