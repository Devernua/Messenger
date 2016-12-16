import asyncore
import socket
import json
import base64
from diffiehellman.diffiehellman import DiffieHellman
from bigint.big import *
#from Crypto import Random
#from Crypto.Random import random
#from Crypto.PublicKey import ElGamal
#from Crypto.Util.number import GCD
#from Crypto.Hash import SHA

clients = {}

users = {"Anya": "123", "Titto": "1211", "Alice": "123", "Bob": "123"}
#TODO: ELGAMALKEY
#ElGamalKey = {
#    'x': 39618305357764467552470495913115822425625260473404888117782791806968178497902,
#    'y': 10510494267870926425420828279300334327548548361622046172269274495889301652492,
#    'g': 52931492782774089032240858805384312244601143630200862182145989767835812439526,
#    'p': 97876007283895611191945706438217835830283264987363181522362440407719068602587
#}

#ElGamalObjKey = ElGamal.construct((ElGamalKey['p'], ElGamalKey['g'], ElGamalKey['y'], ElGamalKey['x']))
#DiffiKey = DiffieHellman(510428738036561312652990084235844497188341007623364898897175201156295630370837118234650925786641101882207081084207240817149749011965245510001517970883956429596188392276241036937980020903928392897530321256596008229377706782950274059867699897248012778073319712294573458504805667960122152714558974731533958413713733087654143816779107268784642737415604392803776730223903346749262168734542486485299107190114500936884736610337647599071826449082529663786975115224352000770139919223203983176077147733228034176066124687228428422630502585868026381159079440927482712201700365451855416145414535027217143458985545453505857905605679641482916193672285327937905576782523280389972153653015018782202696072121609391983260266349128426821674354641945846720115085518254536864425682520184514234983311821944396690053397408440134741687051107550197259757259917914791366898932987482447466227491363837215795916898510556390500060719460817686595490774227585850087405771923157619172353358948259506206986987336607310109276734968951240355455737596002511893144555359293991159508786726955129049106723009297588121485114516257591795334129157026109380953149564860682227837794674535889279811711191713512241173737908527914490130326703457456848930226179396152598402479324729223284370362871048651839735600425157157527648162004076578917466514737601280803771096316601249262848649152408149206462317760182584109725998322107181529592993819181037531541935869360138143501403434707878438856879258880923800541874457336395283679605072206518711203800866096332460405511175743569765132373788749703036992868019470560232825219226778328226566997183435976701128806239896610368715770536546378127685839503456668339369891702109051664031646879921431945416230223463140997394776093017843725578856846048608879153104788938632782223013129417973122010375055347831935418852474344984162347596668547190144504652904596346828312205883107606111742928784700202920057216929590955250724386262444569238169701323022846719346408363760335404314822993750208605554111959278582087786575706598890084602993088120880286975599093955129598561545198385967550076487409896628867203065607542161284923768354036115805994275662635665065723748610684174612134171733839355337012118697067357590889029484481290707210109610099563314851182111937968357327673354073419276035082181384834860303808601741142314201572299856706471283660617464480040155333452048806206262832284503711211928014349488681340624352184751341970546912230812420858062954467433007592534074193025025667358,
#                         212908996222673460450725901049499834708546109904802215626678057775631647802693552778712133318241631203775617153532309220841818560321675558605583068632652891104689404254585531)
#DiffiKey.generate_public_key()
#h = SHA.new(str(DiffiKey.public_key).encode()).digest()
#while 1:
#    k = random.StrongRandom().randint(1, ElGamalObjKey.p-1)
#    if GCD(k, ElGamalObjKey.p-1) == 1:
#        break
#(SignR, SignS) = ElGamalObjKey.sign(h, k)


class MessageHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.name = 0
        self.Key = DiffieHellman()
        self.Key.generate_public_key()
        #self.difKey = 0

    def handle_read(self):
        data = self.recv(4096).decode('utf-8')
        if data:
            print("loginfo: " + data)
            if self.Key:
                pass
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

            elif j["action"] == "test":
                s = j["data"].encode()
                print(s)
            elif j["action"] == "message":
                try:
                    clients[j["data"]["to"]].send(json.dumps({"action": "message", "data": {"from": self.name, "message": j["data"]["message"]}}).encode())
                except Exception:
                    self.send(json.dumps({"action": "message", "status": "MESSAGE_ERR"}).encode())

            elif j["action"] == "handshake":
                #try
                #self.Key = int(j["data"]["pubkey"])
                #TODO: SUBSCRIBE and SIGN a PubKEY
                try:
                    self.send(json.dumps({"action": "handshake", "status": "HANDSHAKE_OK", "data": {"pubkey": int_to_base_str(self.Key.public_key)}}).encode())
                    print("pubkey: " + str(base_str_to_int(j["data"]["pubkey"])))
                    self.Key.generate_shared_secret(base_str_to_int(j["data"]["pubkey"]))
                except Exception:
                    self.send(json.dumps({"action": "handshake", "status": "HANDSHAKE_ERR"}).encode())
                #print(self.Key.public_key)
                #print(int(str(self.Key.public_key)))
                print("MY KEY: " + str(self.Key.public_key))
                print("HIM KEY: " + str(base_str_to_int(j["data"]["pubkey"])))
                print("SHARED KEY: " + str(self.Key.shared_key))
                    # self.send(json.dumps({"action": "handshake", "data": {"pubkey": str(DiffiKey.public_key), "signR": SignR, "signS": SignS}}).encode())
                #except Exception:
                    #self.send(json.dumps({"action": "handshake", "status": "MESSAGE_ERR"}).encode())

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
