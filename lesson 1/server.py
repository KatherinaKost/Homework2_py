import socket

HOST = ('127.0.0.1', 7777)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()

while 1:
    conn, addr = sock.accept()    
    print(conn)
    print(addr)

    data = conn.recv(1024).decode()
    print(data)
    if 'Привет' in data:
          conn.send("Привет, как тебя зовут?".encode())
    else:
         conn.send("как тебя зовут?".encode())
    data = conn.recv(1024).decode()
    print(data)
    conn.send(f'Очень приятно, {data}!'.encode())
    data = conn.recv(1024).decode()
    if data == 'выйти':
          break 

conn.close()
