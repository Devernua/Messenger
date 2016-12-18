import asyncore
import socket
import json
import sys
from diffiehellman.diffiehellman import DiffieHellman
from bigint.big import *
from AESCipher.AESCipher import AESCipher
from Crypto.PublicKey import ElGamal
from Crypto.Hash import SHA

ElGamalKey = ElGamal.construct((97876007283895611191945706438217835830283264987363181522362440407719068602587,
                                52931492782774089032240858805384312244601143630200862182145989767835812439526,
                                10510494267870926425420828279300334327548548361622046172269274495889301652492))


class MessangerClient(asyncore.dispatcher):

    def __init__(self, host, port, login, password):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.login = login
        self.password = password
        self.Key = DiffieHellman()
        self.Key.generate_public_key()
        self.buffer = json.dumps({'action': 'handshake', 'data': {'pubkey': int_to_base_str(self.Key.public_key)}}).encode()
        self.cipher = None

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(4024).decode('utf-8')
        if data:
            if self.cipher is not None:
                j = json.loads(self.cipher.decrypt(data))
            else:
                j = json.loads(data)
            print(j)

            if j["action"] == "handshake":
                tmp = base_str_to_int(j["data"]["pubkey"])
                h = SHA.new(j["data"]["pubkey"].encode()).digest()
                self.Key.generate_shared_secret(tmp)
                SignR = int(j["data"]["SignR"])
                SignS = int(j["data"]["SignS"])

                if not ElGamalKey.verify(h, (SignR, SignS)):
                    raise("BAD SIGNATURE")

                self.cipher = AESCipher(str(self.Key.shared_key).encode())
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
        s = self.recv(1024).decode('utf-8')
        (to, msg) = s.split(':', 1)
        self.sender.buffer += json.dumps({"data": {"message": msg, "to": to}, "action": "message"}).encode('utf-8')

login = str(input())
password = str(input())

client = MessangerClient('127.0.0.1', 7777, login, password)
CmdlineClient(client, sys.stdin)

asyncore.loop()

