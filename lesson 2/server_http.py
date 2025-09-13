'''
написать приложение-сервер используя модуль socket работающее в домашней 
локальной сети.
Приложение должно принимать данные с любого устройства в сети отправленные 
или через программу клиент или через браузер
    - если данные пришли по протоколу http создать возможность след.логики:
        - если путь "/" - вывести главную страницу
        
        - если путь содержит /test/<int>/ вывести сообщение - тест с номером int запущен
        
        - если путь содержит message/<login>/<text>/ вывести в консоль/браузер сообщение
            "{дата время} - сообщение от пользователя {login} - {text}"
        
        - если путь содержит указание на файл вывести в браузер этот файл
        
        - во всех остальных случаях вывести сообщение:
            "пришли неизвестные  данные по HTTP - путь такой то"

'''

import socket
import re
from datetime import datetime
from urllib.parse import unquote

def is_file(path):       
    if '.' in path:
        ext =  path.split(".")[-1]
        if ext in ['jpg','png','gif', 'ico', 'txt', 'html', 'json']:
            return True
    return False


def send_inf(text, conn):
    conn.send(OK)
    conn.send(HEADERS)
    conn.send(text)


def send_file(file_name, conn):
    try:
        with open(file_name.lstrip('/'), 'rb') as f:                   
            print(f"send file {file_name}")
            conn.send(OK)
            conn.send(HEADERS)
            conn.send(f.read())
            
    except IOError:
        print('нет файла')
        conn.send(ERR_404)
        

HOST = ('127.0.0.1', 7778)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(HOST)
sock.listen()

OK = b'HTTP/1.1 200 OK\n'
HEADERS = b"Content-Type: text/html; charset=utf-8\n\n"
ERR_404 = b'HTTP/1.1 404 Not Found\n\n'

while 1:
    try:
        conn, adr = sock.accept()
        data = conn.recv(1024).decode()
        method, path, vers = data.split('\n')[0].split()

        print(path)

        if path == '/':                #если путь "/" - вывести главную страницу
            html = "<h1> Главная страница </h1>".encode()
            send_inf(html, conn)

        elif re.fullmatch(r'/test/(\d+)/', path):          #проверка есть совпадение с /test/<int>/
            num = path.rstrip('/').split('/')[-1]
            text_info = f'тест с номером {int(num)} запущен'.encode()
            send_inf(text_info, conn)     

        elif re.fullmatch(r'/message/([^/]+)/([^/]+)/', path):        #если путь содержит message/<login>/<text>/ 
            lst = path.rstrip('/').split('/')
            login = lst[-2]
            text =  unquote(lst[-1])
            current_datetime = datetime.now().replace(microsecond=0)
            text_info = f'{current_datetime} - сообщение от пользователя {login} - {text}'.encode()
            send_inf(text_info, conn)

        elif is_file(path):           #если путь содержит указание на файл вывести в браузер этот файл
            send_file(path, conn)

        else:
            conn.send(b'HTTP/1.1 404 Not Found\n')
            conn.send(b'Content-Type: text/html; charset=utf-8\n\n')
            conn.send(f'пришли неизвестные  данные по HTTP - путь {path}'.encode())
            

    except ValueError:
        print("Неверный HTTP-запрос")
        conn.send(ERR_404)
        
    finally:
        conn.close()    
        

            
                   
         
      
                 

