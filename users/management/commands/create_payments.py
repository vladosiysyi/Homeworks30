from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User, Payment
from materials.models import Course, Lesson
import random
from decimal import Decimal

class Command(BaseCommand):
    help = "Создаёт тестовые платежи для пользователей"

    def handle(self, *args, **options):
        # Проверка пользователей
        users = User.objects.all()
        if not users.exists():
            self.stdout.write("Пользователи не найдены. Создаю тестового пользователя...")
            try:
                user = User.objects.create_user(
                    email="testuser@example.com",
                    password="123456"
                )
                users = [user]
                self.stdout.write(f"Создан тестовый пользователь: {user.email}")
            except Exception as e:
                self.stdout.write(f"Не удалось создать пользователя: {e}")
                return

        # Проверка курсов
        courses = Course.objects.all()
        if not courses.exists():
            self.stdout.write("Курсы не найдены. Создаю тестовый курс...")
            course = Course.objects.create(
                title="Тестовый курс",
                description="Описание тестового курса"
            )
            courses = [course]
            self.stdout.write(f"Создан курс: {course.title}")

        # Проверка уроков
        lessons = Lesson.objects.all()
        if not lessons.exists():
            self.stdout.write("Уроки не найдены. Создаю тестовый урок...")
            lesson = Lesson.objects.create(
                title="Тестовый урок",
                description="Описание тестового урока",
                course=courses[0]
            )
            lessons = [lesson]
            self.stdout.write(f"Создан урок: {lesson.title}")

        # Создаём тестовые платежи
        payment_methods = ["cash", "transfer"]
        for user in users:
            # Платёж за курс
            Payment.objects.create(
                user=user,
                course=courses[0],
                amount=Decimal(random.randint(1000, 5000)),
                payment_method=random.choice(payment_methods),
                date=timezone.now()
            )
            # Платёж за урок
            Payment.objects.create(
                user=user,
                lesson=lessons[0],
                amount=Decimal(random.randint(200, 1000)),
                payment_method=random.choice(payment_methods),
                date=timezone.now()
            )

        self.stdout.write("Тестовые платежи успешно созданы.")
