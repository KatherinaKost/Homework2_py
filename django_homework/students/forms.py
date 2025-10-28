from django import forms
from .models import Courses, Student
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

class CourseAddForm(forms.Form):
    langs = Courses.courses
    
    name = forms.ChoiceField(choices=langs, label='Название', required=True)
    course_num = forms.IntegerField(min_value=1, max_value=100, label='Номер')
    start_date = forms.DateField(widget=forms.DateInput(
        attrs={'type':'date', 'class':'data123'})) #аттрибуты тип даты
    end_date = forms.DateField(widget=forms.DateInput(
        attrs={'type':'date', 'class':'data123'}))
    decription = forms.CharField(widget=forms.Textarea(attrs={'rows':5 }), help_text='help help')

#в отличие от 1-го варианта наслед-ся от ModelForm (модель Course)
class CourseAddForm2(forms.ModelForm):
    class Meta:
        model = Courses
        #fields = '__all__'
        fields = ['name', 'start_date', 'end_date'] #см.поля в модели Course
        #можно указать отдельно виджеты отдельно в классе

class StudentAddForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'age', 'sex', 'active', 'course', 'photo']

    #проверка данных на уровне формы
    # def clean_age(self):
    #     age = self.cleaned_data['age']
    #     if age < 14:
    #         raise ValidationError('возраст не подходит')
        
class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Имя пользователя'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ваше имя'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Подтверждение пароля'})
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        