from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.


class Student(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='имя',
        null=False,
        blank=False,   
    )
    """ null — разрешено ли в базе данных хранить "ничего" (NULL). blank — разрешено ли в формах (админке, сайтах) не заполнять поле.
     по сути, если в бд разрешим не заполнить поле, то для формы django может быть ошибка, если в бланк будет тру """
    
    surname = models.CharField(
        max_length=30,
        verbose_name='фамилия'
    )

    age = models.SmallIntegerField(
        null=True,
        blank=True,
        verbose_name='возраст',
        validators=[MinValueValidator(16),]    
    )

    sex = models.CharField(
        choices=[('m', 'male'), ('f', 'female')],
        verbose_name='пол', 
        max_length=10
    )

    active = models.BooleanField(verbose_name='активный')

    course = models.ManyToManyField(
        to='Courses',
        blank=True,
        verbose_name='курсы'
    )


    def __str__(self):
        return f'{self.name} {self.surname}'
    
    """ В Django, когда создается модель (описание таблицы в бд), ты можно внутри неё создать вложенный класс с именем Meta.
Этот класс не создаёт объектов и не хранит данные — он просто задаёт настройки для самой модели """
    class Meta:  
        verbose_name = 'студенты'
        verbose_name_plural = 'студенты' #когда обращаются ко многим
        indexes = [models.Index(fields=['surname'])] #индексация по surname
        ordering = ['surname']

class Courses(models.Model):
    courses = [
        ('py', 'python'),
        ('c', 'C++'),
        ('js','JavaScript')    
    ]
    name = models.CharField(
        choices=courses, 
        max_length=15,
        verbose_name='курсы'
    )
    start_date = models.DateField(verbose_name='начало курса')
    end_date = models.DateField(verbose_name='конец курса')

    def __str__(self):
        return self.name
    
class Grade(models.Model):
    person = models.ForeignKey(  #связь с таблицей студенты
        Student,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='чья оценка'
    )

    grade = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='оценка'
    )

    date = models.DateField(verbose_name='дата')

    course = models.ForeignKey(
        Courses,
        verbose_name='курсы',
        on_delete=models.CASCADE, 
        null=True
    )

    class Meta:   #настройки для именно таблицы, узнать потом подробнее!!!!!!!!!!!
        verbose_name = 'оценки'
        verbose_name_plural = 'оценка' #когда обращаются ко многим



        

