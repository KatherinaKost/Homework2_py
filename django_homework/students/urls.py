from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('students/', student_list, name='student_list'),
    path('students/<int:student_id>/', student_detail, name='student_detail'),
    path('courses/', course_list, name='course_list'),
    path('grades/', grade_journal, name='grade_journal'),
]