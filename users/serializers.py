from .models import Payment
from materials.serializers import CourseSerializer, LessonDetailSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonDetailSerializer(read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user_email', 'date', 'course', 'lesson', 'amount', 'payment_method']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'country', 'avatar', 'first_name', 'last_name']