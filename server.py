import asyncore
import socket
import json
from .diffiehellman.diffiehellman import DiffieHellman
from Crypto import Random
from Crypto.Random import random
from Crypto.PublicKey import ElGamal
from Crypto.Util.number import GCD
from Crypto.Hash import SHA

clients = {}

users = {"Anya": "123", "Titto": "1211"}

ElGamalKey = {
    'x': 39618305357764467552470495913115822425625260473404888117782791806968178497902,
    'y': 10510494267870926425420828279300334327548548361622046172269274495889301652492,
    'g': 52931492782774089032240858805384312244601143630200862182145989767835812439526,
    'p': 97876007283895611191945706438217835830283264987363181522362440407719068602587
}

ElGamalObjKey = ElGamal.construct((ElGamalKey['p'], ElGamalKey['g'], ElGamalKey['y'], ElGamalKey['x']))
DiffiKey = DiffieHellman()
DiffiKey.generate_public_key()
SignR = ''
SignS = ''


class MessageHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.name = 0
        self.Key = 0

    def handle_read(self):
        data = self.recv(4096).decode('utf-8')
        if data:
            print("loginfo: " + data)
            j = json.loads(data)

            if j["action"] == "register":
                try:
                    if not j["data"]["login"] in users.keys():

                            users[j["data"]["login"]] = j["data"]["pass"]
                            self.name = j["data"]["login"]
                            clients[self.name] = self
                            self.send(json.dumps({"action": "register", "status": "AUTH_OK"}).encode())
                    else:
                        self.send(json.dumps({"action": "register", "status": "AUTH_ERR"}).encode())
                        self.close()
                except Exception:
                    self.send(json.dumps({"action": "register", "status": "AUTH_ERR"}).encode())
                    self.close()

            elif j["action"] == "auth":
                try:
                    if users[j["data"]["login"]] == j["data"]["pass"]:
                        self.name = j["data"]["login"]
                        clients[self.name] = self
                        self.send(json.dumps({"action": "auth", "status": "AUTH_OK"}).encode())
                    else:
                        self.send(json.dumps({"action": "auth", "status": "AUTH_ERR"}).encode())
                        self.close()
                except Exception:
                    self.send(json.dumps({"action": "auth", "status": "AUTH_ERR"}).encode())
                    self.close()

            elif j["action"] == "message":
                try:
                    clients[j["data"]["to"]].send(json.dumps({"action": "message", "data":{"from": self.name, "message": j["data"]["message"]}}).encode())
                except Exception:
                    self.send(json.dumps({"action": "message", "status": "MESSAGE_ERR"}).encode())

            elif j["action"] == "handshake":
                try:
                    self.Key = j["data"]["pubkey"]
                    self.send(json.dumps({"action": "handshake", "data": {"pubkey": str(DiffiKey.public_key), "signR": SignR, "signS": SignS}}).encode())
                except Exception:
                    self.send(json.dumps({"action": "handshake", "status": "MESSAGE_ERR"}).encode())

            else:
                print("WATAFA")


class MessangerServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print('Incoming connection from %s' % repr(addr))
            MessageHandler(sock)


server = MessangerServer('', 7777)
asyncore.loop()
