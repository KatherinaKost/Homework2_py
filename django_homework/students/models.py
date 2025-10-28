from django.db import models
from django.core.validators import MinValueValidator
from pytils.translit import slugify
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

    photo = models.ImageField(
        upload_to=r'photos/%Y/%m/%d',
        blank=True,
        verbose_name='фото'
    )
    # у django в бд хранится не фото, а ссылка
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        verbose_name='slug'
    )

    course = models.ManyToManyField(
        to='Courses',
        blank=True,
        verbose_name='курсы'
    )


    def __str__(self):
        return f'{self.name} {self.surname}'
    
    #для автомат. создания slug
    def save(self, *args, **kwargs):  #НЕ ЗАБЫТЬ В МОДЕЛИ УКАЗАТЬ СЛАГ
        if not self.slug:
            first_slug = slugify(self.surname+'_'+self.name)
            self.slug = self._get_unique_slug(first_slug)
        return super().save(*args, **kwargs)
    
    def _get_unique_slug(self, first_slug):
        slug = first_slug
        count = 1
        while Student.objects.filter(slug=slug).exists(): #exists() проверка наличия
            count += 1
            slug = f"{first_slug}_{count}"
        return slug
            
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
    course_num = models.PositiveSmallIntegerField(  
        verbose_name='номер потока',
        default=1
    )
    start_date = models.DateField(verbose_name='начало курса')
    end_date = models.DateField(verbose_name='конец курса')
    description = models.TextField(blank=True, verbose_name='описание')

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



        

