
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from students.models import Student, Courses, Grade
import random

class Command(BaseCommand):
    help = 'Заполняет базу фейковыми студентами и курсами'

    def handle(self, *args, **kwargs):
        fake = Faker('ru_RU')  # генерация на русском языке

        courses = []
        for code, label in Courses.courses:
            for num in range(1, 4):  # 3 потока по каждому предмету
                start = fake.date_between(start_date='-180d', end_date='-30d')
                end = fake.date_between(start_date=start, end_date='+120d')
                course, _ = Courses.objects.get_or_create(
                    name=code,
                    course_num=num,
                    defaults={
                        'start_date': start,
                        'end_date': end,
                        'description': f'{label} — поток {num}'  
                    }
                )
                courses.append(course)

        # 2. Создаём студентов
        students = []
        for _ in range(10):
            student, created = Student.objects.get_or_create(
                name=fake.first_name(),
                surname=fake.last_name(),
                defaults={
                    'age': random.randint(14, 25),
                    'sex': random.choice(['m', 'f']),
                    'active': True,
                }
            )
            student.save()  # сначала сохраним, чтобы был ID
            # Назначаем 1–3 курса (ManyToMany)
            selected_courses = random.sample(courses, k=random.randint(1, min(3, len(courses))))
            student.course.set(selected_courses)
            students.append(student)

         # 3. Добавляем оценки
        grades = []
        for student in students:
            student_courses = list(student.course.all())
            for _ in range(random.randint(3, 8)):
                course = random.choice(student_courses)
                grade_val = random.randint(60, 100)
                date = fake.date_between(start_date=course.start_date, end_date='today')
                grades.append(Grade(
                    person=student,
                    course=course,
                    grade=grade_val,
                    date=date
                ))
        Grade.objects.bulk_create(grades)
        