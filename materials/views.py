from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from .models import Course, Lesson, Subscription
from .serializers import LessonDetailSerializer, CourseSerializer
from .permissions import IsModerator
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .paginators import MaterialsPagination

# кастомное разрешение для модераторов и админов
class IsModeratorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or getattr(request.user, "role", "") in ["moderator", "admin"]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.prefetch_related('lessons').all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsModeratorOrAdmin()]
        elif self.action in ['create', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.select_related('course').all()
    serializer_class = LessonDetailSerializer
    pagination_class = MaterialsPagination

    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        serializer.save(owner=self.request.user, course_id=course_id)

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        elif self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.select_related('course').all()
    serializer_class = LessonDetailSerializer

    def get_queryset(self):
        user = self.request.user
        # Модератор видит все, обычный пользователь только свои
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]  # любой аутентифицированный может смотреть
        elif self.request.method in ["PUT", "PATCH"]:
            return [IsModeratorOrAdmin()]  # редактировать могут модератор или админ
        elif self.request.method == "DELETE":
            return [IsAdminUser()]  # удалять только админ
        return [IsAuthenticated()]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})
