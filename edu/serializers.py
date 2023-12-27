from rest_framework import serializers

from edu.models import Course, Lesson, Subscription


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

