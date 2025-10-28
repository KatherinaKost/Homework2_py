from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import*
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView

from django.db import connection
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


class CoursAddView(CreateView):#1вариант ч/з класс
    form_class = CourseAddForm  #по отдельной форме, форма для ввода данных 
    template_name = 'course_add_form.html' #шаблон с формой
    success_url = reverse_lazy('students')   #для того чтобы не возникала циклическая ссылка, в случае удачной операции переход на стьюдентс

# def course_add_view(r): #2 варинт добавления через функцию (вручную) для формы наследуемой от формы  
#     if r.method == 'POST':
#         form = CourseAddForm(r.POST) #r.Post все данные, которые заполняются постом и создается форма 
#         if form.is_valid():#если на моменте валидации будет ошибка, она попадает в форму всеравно
#             """ form.save()
#             return redirect('courses') """
#             try:
#                 Courses.objects.create(**form.cleaned_data) #только если прошла валидацию, **form.cleaned_data - словарь с данными из формы, создается запись в модель дб
#             except Exception as e:
#                 form.add_error(None, 'Ошибка') #в форму попадает ошибка

#     else:
#         form = CourseAddForm() #создается объект из формы если GET(пустая)
#         return render(r, 'course_add_form.html', context={'form':form})
    


#Вариант для формы наследуемый от модели
@login_required(login_url='/login/') #если не автор-н отправл-ся на логин урл
def course_add_view(r): #2 варинт добавления через функцию (вручную)  
    if r.method == 'POST':
        form = CourseAddForm2(r.POST) #r.Post все данные, которые заполняются постом и создается форма 
        if form.is_valid():#если на моменте валидации будет ошибка, она попадает в форму всеравно
           form.save()
           return redirect ('course_list')
#тут уже модель сохраняется благодоря form.save()
    else:
        form = CourseAddForm2() #создается объект из формы если GET(пустая)
        return render(r, 'course_add_form.html', context={'form':form})
    
class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Courses
    form_class = CourseAddForm2
    template_name = 'course_edit_form.html'
    success_url = reverse_lazy('course_list')
    login_url = '/login/'

class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Courses    #тут берется уже сама модель для удаления записи!!!!!а не форма
    template_name = 'course_confirm_delete.html'
    success_url = reverse_lazy('course_list')
    login_url = '/login/'
    
class StudentAddView(LoginRequiredMixin, CreateView):
    form_class = StudentAddForm
    template_name = 'student_add_form.html'
    success_url = reverse_lazy('student_list')
    login_url = '/login/' #пишется когда есть LoginRequiredMixin в случае необ-ти залогин-ся отправит на логин

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentAddForm
    template_name = 'student_edit_form.html'
    success_url = reverse_lazy('student_list')
    login_url = '/login/'

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student    #тут берется уже сама модель для удаления записи!!!!!а не форма
    template_name = 'student_confirm_delete.html'
    success_url = reverse_lazy('student_list')
    login_url = '/login/'


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_success_url(self): #при успешном логинировании переносит на гл стр, а в чем отличие??
        return reverse_lazy('home')
    
def logout_user(r):
    logout(r)
    return redirect('home')

class RegisterUser(CreateView):
    #form_class = UserCreationForm #з джанго
    form_class = RegisterUserForm
    template_name = 'reg.html'
    success_url = reverse_lazy('login')
    def form_valid(self, form): #внутри формы сами сохраняем юзера и реализуется логин сразу, чтобы не переходить на стр логин
        user = form.save()
        login(self.request, user)
        return redirect('home')