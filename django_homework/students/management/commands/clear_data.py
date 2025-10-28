
from django.core.management.base import BaseCommand
from students.models import Student, Courses, Grade

class Command(BaseCommand):
    help = 'Удаляет все данные из моделей Student, Courses, Grade'

    def handle(self, *args, **kwargs):
        Grade.objects.all().delete()
        Student.objects.all().delete()
        Courses.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS('Все данные успешно удалены!')
        )