import asyncore
import socket
import json
import sys
from diffiehellman.diffiehellman import DiffieHellman
from bigint.big import *
from AESCipher.AESCipher import AESCipher
from Crypto import Random
from Crypto.Random import random
from Crypto.PublicKey import ElGamal
from Crypto.Util.number import GCD
from Crypto.Hash import SHA
import base64

#TODO:remember ELGamalKey
#key = DiffieHellman()
#key.generate_public_key()
#print(key.public_key)

class MessangerClient(asyncore.dispatcher):

    def __init__(self, host, port, login, password):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.login = login
        self.password = password
        self.Key = DiffieHellman()
        self.Key.generate_public_key()
        #self.buffer = json.dumps({'action': 'auth', 'data': {'login': login, 'pass': password}}).encode('utf-8')
        self.buffer = json.dumps({'action': 'handshake', 'data': {'pubkey': int_to_base_str(self.Key.public_key)}}).encode()
        self.cipher = None

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(4024).decode('utf-8')
        if data:
            #print(data)
            if self.cipher is not None:
                j = json.loads(self.cipher.decrypt(data))
            else:
                j = json.loads(data)
            print(j)
            #j = json.loads(data)
            if j["action"] == "handshake":
                self.Key.generate_shared_secret(base_str_to_int(j["data"]["pubkey"]))
                #print("MY KEY: " + str(self.Key.public_key))
                #print("HIM KEY: " + str(base_str_to_int(j["data"]["pubkey"])))
                #print("SHARED KEY: " + str(self.Key.shared_key))
                self.cipher = AESCipher(str(self.Key.shared_key).encode())
                #TODO:check al gamal
                #TODO:cut difkey end chifer by AES
                self.buffer = json.dumps({'action': 'auth', 'data': {'login': login, 'pass': password}}).encode('utf-8')

    def writable(self):
        return len(self.buffer) > 0

    def handle_write(self):
        if self.cipher is not None:
            sent = self.send(self.cipher.encrypt(self.buffer.decode()))
            self.buffer = self.buffer[sent:]
        else:
            sent = self.send(self.buffer)
            self.buffer = self.buffer[sent:]


class CmdlineClient(asyncore.file_dispatcher):
    def __init__(self, sender, file):
        asyncore.file_dispatcher.__init__(self, file)
        self.sender = sender

    def handle_read(self):
        #self.recv(1024).decode('utf-8')
        #TODO:chifer by AES
        #self.sender.buffer += json.dumps({"data": {"pubkey": str(key.public_key)}, "action": "handshake"}).encode()
        self.sender.buffer += json.dumps({"data": {"message": self.recv(1024).decode('utf-8'), "to": "Anya"}, "action": "message"}).encode('utf-8')

login = str(input())
password = str(input())

client = MessangerClient('', 7777, login, password)
CmdlineClient(client, sys.stdin)

asyncore.loop()

