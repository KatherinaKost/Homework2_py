from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.

def home(r):
    return render(r, 'home.html')

def student_list(r):
    students = Student.objects.all()
    return render(r, 'students_list.html', context={'students':students})
    

def  student_detail(r, student_id):
    student = Student.objects.get(id=student_id)
    grades = Grade.objects.filter(person=student).select_related('course')         
    return render (r, 'student_detail.html', context={'student':student,'grades':grades})

#select_related('course') — это способ "подгрузить связанный объект (курс) сразу вместе с основным (оценкой), чтобы не обращаться к бд много раз".
#используется для связи ForeignKey — «много к одному" и OneToOneField — «один к одному»
#для связи ManyToManyField — «многие ко многим» - prefetch_related().
    
    


def course_list(r):
    courses = Courses.objects.all()
    return render(r, 'course_list.html', context={'courses': courses})

def grade_journal(r):
    grades = Grade.objects.select_related('person', 'course').order_by('date')
    return render(r, 'grade_journal.html', context={'grades': grades})
