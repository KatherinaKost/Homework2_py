'''
Написать веб-приложение на Flask со следующими ендпоинтами:
    - главная страница - содержит ссылки на все остальные страницы
    - /duck/ - отображает заголовок "рандомная утка №ххх" и картинка утки 
                которую получает по API https://random-d.uk/api/random
                
    - /fox/<int>/ - аналогично утке только с лисой (- https://randomfox.ca), 
                    но количество разных картинок определено int. 
                    если int больше 10 или меньше 1 - вывести сообщение 
                    что можно только от 1 до 10
    
    - /weather-minsk/ - показывает погоду в минске в красивом формате
    
    - /weather/<city>/ - показывает погоду в городе указанного в city
                    если такого города нет - написать об этом
    
    - по желанию добавить еще один ендпоинт на любую тему 
    
    
Добавить обработчик ошибки 404. (есть в example)
    

'''

from flask import Flask, render_template
import requests

def get_duck():
    res = requests.get('https://random-d.uk/api/random')
    d = res.json()
    num = d['url'].split('.')[1].split('/')[-1]
    url_img = d['url']
    return url_img, num

def get_fox(num):
    images = []
    while num:
        res = requests.get('https://randomfox.ca/floof/')
        d = res.json()
        images.append(d['image'])
        num -= 1
    return images

def get_weather(city=None):
    url = f'http://api.openweathermap.org/data/2.5/weather'

    if city:
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56','lang': 'ru'}
    else:
        params = {'q': 'Minsk', 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56', 'lang': 'ru' }

    answer = requests.get(url, params)
    res = answer.json()

    if answer.status_code != 200:
        return {
                'error': True,
                'message': res.get('message', 'Город не найден')
            }
    
    result = {
            'city': res['name'],
            'weather':res["weather"][0]["main"],
            'temp':round(res['main']['temp']-273.15, 1),
            'humidity':res['main']['humidity'],
            'feels_like':round(res['main']['feels_like']-273.15, 1),
            'wind':res['wind']['speed']
    }
    return result

app = Flask(__name__)

@app.route('/')
def main_page():        
    return render_template('1.html')

@app.route('/duck/')    
def ducks():
    image, num = get_duck()
    return render_template('duck.html', image = image, num = num)

@app.route('/fox/<int:num>/')
def fox(num):
    if 1 <= num <= 10:
        images_lst = get_fox(num)
        return render_template('fox.html', foxes=images_lst)
    return '<h1>Количество изображений должно быть в пределах от 1 до 10</h1>'


@app.route('/weather-minsk/')
def weather_minsk():
    weather = get_weather()
    return render_template('weather.html', weather = weather)

@app.route('/weather/<string:city>/')
def weather(city):
    weather_city = get_weather(city)
    if weather_city.get('error'):
        return f"Ошибка: {weather_city['message']}</h2>"

    return render_template('weather.html', weather=weather_city)



@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'

app.run(debug=True)




