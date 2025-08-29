from rest_framework import serializers
from .models import Payment
from materials.serializers import CourseSerializer, LessonSerializer

class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user_email', 'date', 'course', 'lesson', 'amount', 'payment_method']
