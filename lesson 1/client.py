import socket


HOST = ('127.0.0.1', 7777)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


sock.connect(HOST)

sock.sendall('Привет'.encode("utf-8")) 
print('---жду ответ от сервера---')
data = sock.recv(1024).decode() 
print(data) # печатаем ответ
sock.send('Катя'.encode())
data = sock.recv(1024).decode()
print(data)
sock.send('выйти'.encode())


sock.close()
