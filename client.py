import asyncore
import socket
import json
import sys


class MessangerClient(asyncore.dispatcher):

    def __init__(self, host, port, login, password):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.buffer = json.dumps({'name': login, 'password': password}).encode('utf-8')

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print(self.recv(1024).decode('utf-8'))

    def writable(self):
        return len(self.buffer) > 0

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]


class CmdlineClient(asyncore.file_dispatcher):
    def __init__(self, sender, file):
        asyncore.file_dispatcher.__init__(self, file)
        self.sender = sender

    def handle_read(self):
        self.sender.buffer += self.recv(1024)

login = str(input())
password = str(input())

client = MessangerClient('', 7777, login, password)
CmdlineClient(client, sys.stdin)

asyncore.loop()

