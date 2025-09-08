from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from materials.models import Lesson, Course, Subscription

User = get_user_model()

class LessonCRUDTestCase(APITestCase):
    def setUp(self):
        # обычный пользователь
        self.user = User.objects.create_user(email='user@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

        # курс
        self.course = Course.objects.create(title='Test Course', owner=self.user)

        # данные урока без course!
        self.lesson_data = {
            "title": "Test Lesson",
            "description": "Lesson description",
            "video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
        }

    def test_list_lessons(self):
        Lesson.objects.create(owner=self.user, course=self.course, title='L1', description='Desc1', video_url='https://youtube.com/watch?v=abc')
        url = reverse('materials:lesson-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_user_cannot_create_lesson(self):
        url = reverse('materials:lesson-list-create')
        response = self.client.post(url, {**self.lesson_data, 'course': self.course.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_lesson(self):
        admin = User.objects.create_superuser(email='admin@example.com', password='adminpass')
        self.client.force_authenticate(user=admin)
        url = reverse('materials:lesson-list-create')
        response = self.client.post(url, {**self.lesson_data, 'course': self.course.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_retrieve_lesson(self):
        lesson = Lesson.objects.create(owner=self.user, course=self.course, title='L1', description='Desc1', video_url='https://youtube.com/watch?v=abc')
        url = reverse('materials:lesson-detail', kwargs={'pk': lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], lesson.title)

    def test_user_cannot_update_or_delete_lesson(self):
        lesson = Lesson.objects.create(owner=self.user, course=self.course, title='L1', description='Desc1', video_url='https://youtube.com/watch?v=abc')
        url = reverse('materials:lesson-detail', kwargs={'pk': lesson.pk})

        response = self.client.patch(url, {'title': 'Updated'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", password="testpass")
        self.admin = User.objects.create_superuser(email="admin@test.com", password="adminpass")
        self.course = Course.objects.create(title="Test Course", owner=self.admin)

    def test_subscribe_and_unsubscribe(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscription")

        # Подписка
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
        self.assertEqual(response.data["message"], "Подписка добавлена")

        # Отписка
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
        self.assertEqual(response.data["message"], "Подписка удалена")
