from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('students/', student_list, name='student_list'),
    path('students/<int:student_id>/', student_detail, name='student_detail'),
    path('courses/', course_list, name='course_list'),
    path('grades/', grade_journal, name='grade_journal'),
    path('courses/add', course_add_view, name='course_add'),
    path('students/add', StudentAddView.as_view(), name='student_add'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('reg/', RegisterUser.as_view(), name='reg'),
    path('students/edit/<int:pk>/', StudentUpdateView.as_view(), name='student_edit'),
    path('students/delete/<int:pk>/', StudentDeleteView.as_view(), name='student_delete'),
    path('courses/edit/<int:pk>/', CourseUpdateView.as_view(), name='course_edit'),
    path('courses/delete/<int:pk>/', CourseDeleteView.as_view(), name='course_delete'),
]