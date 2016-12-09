import asyncore
import socket
import json

clients = {}

users = {}
users["Anya"] = "123"
users["Titto"] = "1211"


class MessageHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.name = 0

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
