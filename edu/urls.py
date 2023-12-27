from django.urls import path

from.apps import EducationConfig
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionCreateAPIView, \
    SubscriptionDestroyAPIView

app_name = EducationConfig.name

router = DefaultRouter()

router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('lesson/<int:pk>/create_sub/', SubscriptionCreateAPIView.as_view(), name='sub_create'),
    path('lesson/<int:pk>/delete_sub/', SubscriptionDestroyAPIView.as_view(), name='sub_delete'),

] + router.urls