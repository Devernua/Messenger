import asyncore
import socket
import json

clients = []


class MessageHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(4096).decode('utf-8')
        if data:
            print(data)
            j = json.loads(data)
            d = {}
            self.name = j["name"]
            d["handler"] = self
            clients.append(d)

            for i in clients:
                print(i["handler"].name)
                self.send(i["handler"].name.encode() + b'\n')
                # print(json)

                # for i in range(len(clients)):
                #    try:
                #    	clients[i].send(data)
                #    except Exception:
                #        print("WATAFAAAA!\n")
                #        clients[i] = 0
                #    finally:
                #        print("BAD EXCEPTIONS\n")
                #        clients[i] = 0
                # clients = [i for i in clients if i != 0]


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
            # clients.append(EchoHandler(sock))


server = MessangerServer('', 7777)
asyncore.loop()
