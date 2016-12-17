import asyncore
import socket
import json
from diffiehellman.diffiehellman import DiffieHellman
from bigint.big import *
from AESCipher.AESCipher import AESCipher
from Crypto.Random import random
from Crypto.PublicKey import ElGamal
from Crypto.Util.number import GCD
from Crypto.Hash import SHA

clients = {}

users = {"Anya": "123", "Titto": "1211", "Alice": "123", "Bob": "123"}

ElGamalKey = {
    'x': 39618305357764467552470495913115822425625260473404888117782791806968178497902,
    'y': 10510494267870926425420828279300334327548548361622046172269274495889301652492,
    'g': 52931492782774089032240858805384312244601143630200862182145989767835812439526,
    'p': 97876007283895611191945706438217835830283264987363181522362440407719068602587
}

ElGamalObjKey = ElGamal.construct((ElGamalKey['p'], ElGamalKey['g'], ElGamalKey['y'], ElGamalKey['x']))


class MessageHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.name = 0
        self.Key = DiffieHellman()
        self.Key.generate_public_key()
        self.cipher = None

    def handle_read(self):
        data = self.recv(4096).decode()
        print("data: ", data)
        if data:
            if self.cipher is not None:
                j = json.loads(self.cipher.decrypt(data))
            else:
                j = json.loads(data)
            print("loginfo: " + json.dumps(j))
            if j["action"] == "register" and self.cipher:
                try:
                    if not j["data"]["login"] in users.keys():
                            users[j["data"]["login"]] = j["data"]["pass"]
                            self.name = j["data"]["login"]
                            clients[self.name] = self
                            self.send(self.cipher.encrypt(json.dumps({"action": "register", "status": "AUTH_OK"})))
                    else:
                        self.send(self.cipher.encrypt(json.dumps({"action": "register", "status": "AUTH_ERR"})))
                        self.close()
                except Exception:
                    self.send(self.cipher.encrypt(json.dumps({"action": "register", "status": "AUTH_ERR"})))
                    self.close()

            elif j["action"] == "auth" and self.cipher:
                try:
                    if users[j["data"]["login"]] == j["data"]["pass"]:
                        self.name = j["data"]["login"]
                        clients[self.name] = self
                        self.send(self.cipher.encrypt(json.dumps({"action": "auth", "status": "AUTH_OK"})))
                    else:
                        self.send(self.cipher.encrypt(json.dumps({"action": "auth", "status": "AUTH_ERR"})))
                        self.close()
                except Exception:
                    self.send(self.cipher.encrypt(json.dumps({"action": "auth", "status": "AUTH_ERR"})))
                    self.close()

            elif j["action"] == "test":
                s = j["data"].encode()
                print(s)
            elif j["action"] == "message" and self.cipher:
                try:
                    chel = clients[j["data"]["to"]]
                    chel.send(chel.cipher.encrypt(json.dumps({"action": "message", "data": {"from": self.name, "message": j["data"]["message"]}})))
                except Exception:
                    self.send(self.cipher.encrypt(json.dumps({"action": "message", "status": "MESSAGE_ERR"})))

            elif j["action"] == "handshake":
                try:
                    h = SHA.new(int_to_base_str(self.Key.public_key).encode()).digest()
                    while 1:
                        k = random.StrongRandom().randint(1, ElGamalObjKey.p-1)
                        if GCD(k, ElGamalObjKey.p-1) == 1:
                            break
                    (SignR, SignS) = ElGamalObjKey.sign(h, k)
                    self.send(json.dumps({"action": "handshake", "status": "HANDSHAKE_OK", "data": {"pubkey": int_to_base_str(self.Key.public_key), "SignR": SignR, "SignS": SignS}}).encode())
                    print("pubkey: " + str(base_str_to_int(j["data"]["pubkey"])))
                    self.Key.generate_shared_secret(base_str_to_int(j["data"]["pubkey"]))
                    self.cipher = AESCipher(str(self.Key.shared_key).encode())
                except Exception as e:
                    print("ERROR: ", e)
                    self.send(json.dumps({"action": "handshake", "status": "HANDSHAKE_ERR"}).encode())
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
