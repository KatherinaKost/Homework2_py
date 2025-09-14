'''
если данные пришли НЕ по протоколу http создать возможность след.логики:
        - если пришла строка формата "command:reg; login:<login>; password:<pass>"
            - выполнить проверку:
                login - только латинские символы и цифры, минимум 6 символов
                password - минимум 8 символов, должны быть хоть 1 цифра
            - при успешной проверке:
                1. вывести сообщение на стороне клиента: 
                    "{дата время} - пользователь {login} зарегистрирован"
                2. добавить данные пользователя в список/словарь на сервере
            - если проверка не прошла вывести сообщение на стороне клиента:
                "{дата время} - ошибка регистрации {login} - неверный пароль/логин"
                
        - если пришла строка формата "command:signin; login:<login>; password:<pass>"
            выполнить проверку зарегистрирован ли такой пользователь на сервере:                
            
            при успешной проверке:
                1. вывести сообщение на стороне клиента: 
                    "{дата время} - пользователь {login} произведен вход"
                
            если проверка не прошла вывести сообщение на стороне клиента:
                "{дата время} - ошибка входа {login} - неверный пароль/логин"
        
        - во всех остальных случаях вывести сообщение на стороне клиента:
            "пришли неизвестные  данные - <присланные данные>"
'''
import socket
import re
from datetime import datetime


def valid(login, password):
    if not  re.fullmatch(r'[a-zA-Z0-9]+', login):    #только латинские символы и цифры, 
        return False
    
    if len(login) < 6:     #минимум 6 символов
        return False
    
    if not re.search(r'\d', password):   #должны быть хоть 1 цифра
        return False
    
    if  len(password) < 8:  #минимум 8 символов
        return False
    
    return True
    
HOST = ('127.0.0.1', 7778)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(HOST)
sock.listen() 

user = []

while True:
    try:
        conn, add = sock.accept()
        print(f'-----Пользователь {add}-----')
        while True:
            try:
                data = conn.recv(1024).decode()
                print('Полученная инф.', data)

                if data == 'exit':
                    print('Пользователь отключился')
                    break

                if not data:
                    break
            
                dict_data = dict(i.split(':') for i in data.split('; '))

                if dict_data['command'] == 'reg':
                    if valid(dict_data['login'], dict_data['password']):
                        current_datetime = datetime.now().replace(microsecond=0)
                        answer = f"{current_datetime} - пользователь {dict_data['login']} зарегистрирован"
                        print(answer)
                        conn.send(data.encode())
                        user.append(dict_data['login'])
                    else:
                        answer = f'{datetime.now().replace(microsecond=0)} - ошибка регистрации {dict_data['login']} - неверный пароль/логин'
                        print(answer)
                        conn.send(answer.encode())

                if dict_data['command'] == 'signin':
                    if dict_data['login'] in user:
                        current_datetime = datetime.now().replace(microsecond=0)
                        answer = f'{current_datetime} - пользователь {dict_data['login']} произведен вход'
                        print(answer)
                        conn.send(answer.encode())
                    else:
                        answer = f'{datetime.now().replace(microsecond=0)} - ошибка входа {dict_data['login']} - неверный пароль/логин'
                        print(answer)
                        conn.send(answer.encode())

                else:
                    conn.send('Неизвестная команда'.encode())


            except Exception as e:
                error_msg = f"пришли неизвестные данные - {data}"
                print(f"Ошибка: {e}")
                try:
                    conn.send(error_msg.encode())
                except:
                    break

        conn.close()
        print(user)

    except Exception as e:
        print(f"Ошибка при подключении: {e}")  

               
                 