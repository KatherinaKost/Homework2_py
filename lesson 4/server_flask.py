'''
Добавить к прошлому проекту 2 страницы 
    - страницу с формой регистрации.
        Регистрация должна содержать имя фамилию возраст email логин пароль.
        После отправки формы регистрации проверить данные на валидность
            - имя фамилия - только русские буквы
            - логин - латинские цифры и _. От 6 до 20 символов
            - пароль - обязательно хотя бы 1 латинская маленькая, 1 заглавная и  1 цифр. От 8 до 15 символов.
            - * email - должен быть валидным
            - * возраст - целое число от 12 до 100
        При успешной проверке  добавить пользователя в базу/файл/список/словарь 
            и направить пользователя на форму входа.
        При выявлении ошибок снова показать форму, но уже с заполненными полями 
            и в любом месте формы показать список ошибок.
        
    - страницу с формой входа на сайт.
        - при успешном входе                             
            - пометить в сессиях что он залогинился
            - перенаправить на главную страницу
        - при ошибке показать форму снова, с сообщением об ошибке



Все прежние страницы сделать открытыми только для пользователей которые произвели вход на сайт.
Если пользователь не залогинился и переходит на них - перенаправлять его на форму входа. 
На фоме входа сделать ссылку на форму регистрации.

Если пользовался залогинился - на каждой странице сверху писать - "Приветствуем вас имя фамилия"

На главной странице показывать ссылку ВХОД и РЕГИСТРАЦИЯ для пользователей которые не вошли на сайт
и ссылку ВЫХОД для  пользователей которые вошли на сайт

Таким образом новый пользователь имеет доступ  только на главную страницу где есть ссылка на вход регистрацию.
После регистрации и входа он имеет доступ на все доступные страницы.

'''

from flask import Flask, render_template, redirect, request, url_for, session
import check
from flask_bcrypt import Bcrypt
import get_url
import users_save
from functools import wraps


def get_error(log, fname, lname, mail, age, pas):
    err = {}
    if not check.chek_log(log):
        err['login'] = 'err:латинские цифры и _. От 6 до 20 символов'
    if not check.chek_name(fname):
        err['firstName'] = 'err: только русские буквы'
    if not check.chek_name(lname):
        err['lastName'] = 'err: только русские буквы'
    if not check.chek_email(mail):
        err['mail'] = 'err: невалидный email'
    if not check.chek_age(age):
        err['age'] = 'err: от 12 до 100'
    if not check.chek_pass(pas):
        err['pas'] = 'err пароль: 1 латинская маленькая, 1 заглавная и  1 цифр. От 8 до 15 символов'
    return err

def chek_log(f): #декоратор для т.входа, если сессия есть, то возвр. декорируемую функцию, если нет то переход
    @wraps(f)
    def wrapper (*args, **kwargs):
        if 'user_login' not in session:
            return redirect(url_for('form_sign'))
        login = session.get('user_login')
        user = users_save.get_user_by_login(login)
        userNAME = f"{user.get('firstName')} {user.get('lastName')}" #вытягиваю фио и отправляю в наши функции
        return f(*args, **kwargs, userNAME=userNAME)
    return wrapper


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fd339322409f0dfc0f1f1f0732ddad28a4d83204'
bcrypt = Bcrypt(app)

def hash_pass(pas):
    return bcrypt.generate_password_hash(pas).decode('utf-8')

def error_sign(login, pas):
    err = {}
    users = users_save.load_user()
    if login not in users:
        err['login'] = f'Пользователь {login} не найден'
    else:
        if not bcrypt.check_password_hash(users[login]['pass'], pas):
            err['pass'] = 'Неверный пароль'
    return err


@app.route('/')
def main_page():
    if 'user_login' not in session:
        return render_template('1.html', user=None)
    login = session.get('user_login')
    user = users_save.get_user_by_login(login)
    userNAME = f"{user.get('firstName')} {user.get('lastName')}"
    return render_template('1.html', user=userNAME)

@app.route('/duck/')
@chek_log    
def ducks(userNAME):  
    image, num = get_url.get_duck()
    return render_template('duck.html', image=image, num=num, user=userNAME)

@app.route('/fox/<int:num>/')
@chek_log 
def fox(num, userNAME):
    if 1 <= num <= 10:
        images_lst = get_url.get_fox(num)
        return render_template('fox.html', foxes=images_lst, user=userNAME)
    return '<h1>Количество изображений должно быть в пределах от 1 до 10</h1>'


@app.route('/weather-minsk/')
@chek_log 
def weather_minsk(userNAME):
    weather = get_url.get_weather()
    return render_template('weather.html', weather = weather, user=userNAME)

@app.route('/weather/<string:city>/')
@chek_log 
def weather(city, userNAME):
    weather_city = get_url.get_weather(city)
    if weather_city.get('error'):
        return f"Ошибка: {weather_city['message']}</h2>"

    return render_template('weather.html', weather=weather_city, user=userNAME)


@app.route('/form_reg/', methods=['GET', 'POST'])
def form_reg(): 
    if request.method == 'POST':
        login = request.form.get('login')
        fname = request.form.get('firstName')
        lname = request.form.get('lastName')
        mail = request.form.get('email')
        age = request.form.get('age')
        pas = request.form.get('pass')

        errors = get_error(login, fname, lname, mail, age, pas)

        if not errors:
            pass_hash = hash_pass(pas)
            user_info = {'firstName': fname, 'lastName':lname, 'email':mail, 'age':age, 'pass':pass_hash}

            if users_save.save_user(login, user_info):
                return redirect(url_for('form_sign'))
            else:
                err_save = f'Пользователь с логином {login} существует'
                return render_template('form_reg.html',errors={}, errsave=err_save, data_form=request.form)
            
        else:
            return render_template('form_reg.html', errors=errors, data_form=request.form)
    return render_template('form_reg.html', errors={}, data_form={})
        

@app.route('/form_sign/', methods=['GET', 'POST'])
def form_sign():
    if request.method == 'POST':
        login = request.form.get('login')
        pas = request.form.get('pass')

        errors = error_sign(login, pas)

        if not errors:
            session['user_login'] = login
            return redirect(url_for('main_page'))
        
        else:
            return render_template('form_sign.html', err=errors, data_form=request.form)
    return render_template('form_sign.html', err={}, data_form={})


@app.route('/logout')
def logout():
    session.pop('user_login', None) 
    return redirect(url_for('main_page'))  

@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'

app.run(debug=True)

