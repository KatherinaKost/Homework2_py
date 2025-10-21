from django.contrib import admin

# Register your models here.

from .models import Student, Courses, Grade

#admin.site.register(Student)   #для регистрации

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'name', 'sex', 'average_grade', 'short_name') #поля которые показывает
    search_fields = ('surname',)

    def short_name(self, obj):  #виртуальное поле в бд нет, в админке -есть
        return f'{obj.surname} {obj.name[0]}' #почему obj? obj - приходит объект ORM
    
    def average_grade(self, obj):
        gs = [g.grade for g in obj.grades.all()]
        return round(sum(gs)/len(gs), 2) if gs else '-'
    
@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display= ('id', 'name', 'start_date', 'end_date')
    search_fields = ('name',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('person', 'grade', 'course', 'date')
    search_fields = ('person',)
    list_filter = ('person',)
    
