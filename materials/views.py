from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.prefetch_related('lessons').all()
    serializer_class = CourseSerializer

class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.select_related('course').all()
    serializer_class = LessonSerializer

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.select_related('course').all()
    serializer_class = LessonSerializer
