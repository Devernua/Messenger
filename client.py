import asyncore
import socket
import json
import sys
from .diffiehellman.diffiehellman import DiffieHellman


class MessangerClient(asyncore.dispatcher):

    def __init__(self, host, port, login, password):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.buffer = json.dumps({'action': 'auth', 'data':{'login': login, 'pass': password}}).encode('utf-8')
        self.keys = DiffieHellman()
        self.keys.generate_public_key()

        print("private key: ")
        print(self.keys.private_key)

        print("public key: ")
        print(self.keys.public_key)

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
        self.sender.buffer += json.dumps({"data": {"message": self.recv(1024).decode('utf-8'), "to": "Anya"}, "action": "message"}).encode()

login = str(input())
password = str(input())

client = MessangerClient('', 7777, login, password)
CmdlineClient(client, sys.stdin)

asyncore.loop()

