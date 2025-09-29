
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
        params = {'q': 'Minsk', 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56', 'lang': 'ru'}

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

def get_rates():
    url = "https://www.nbrb.by/api/exrates/rates?periodicity=0"
    response = requests.get(url, timeout=5)
    data = response.json()

    usd_list = [item for item in data if item['Cur_Abbreviation'] == 'USD']
    eur_list = [item for item in data if item['Cur_Abbreviation'] == 'EUR']

    rates = {
        'USD': round(usd_list[0]['Cur_OfficialRate'], 2) if usd_list else '—',
        'EUR': round(eur_list[0]['Cur_OfficialRate'], 2) if eur_list else '—'
    }
    return (rates)

