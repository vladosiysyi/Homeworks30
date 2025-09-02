from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Course, Lesson
from .serializers import LessonDetailSerializer, CourseSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.prefetch_related('lessons').all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            # просматривать и редактировать могут админы и модераторы
            self.permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]
        elif self.action in ['create', 'destroy']:
            # создавать и удалять могут только админы
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.select_related('course').all()
    serializer_class = LessonDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), IsModerator() | IsAdminUser()]
        elif self.request.method == "POST":
            return [IsAdminUser()]  # только админ может создавать урок
        return [IsAuthenticated()]

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.select_related('course').all()
    serializer_class = LessonDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Модератор видит все, обычный пользователь только свои
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "PATCH"]:
            return [IsAuthenticated(), IsModerator() | IsAdminUser()]
        elif self.request.method == "DELETE":
            return [IsAdminUser()]  # удалять только админ
        return [IsAuthenticated()]