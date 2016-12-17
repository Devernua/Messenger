from diffiehellman.diffiehellman import DiffieHellman, rng
import base64
from Crypto import Random
from Crypto.Cipher import AES

from AESCipher.AESCipher import AESCipher
from bigint.big import *
#k1 = DiffieHellman()
#k1.generate_public_key()
#k2 = DiffieHellman()
#k2.generate_public_key()

#k1.generate_shared_secret(k2.public_key)
#k2.generate_shared_secret(k1.public_key)

#print(k1.shared_key == k2.shared_key)

#print(pow(k2.public_key,k1.private_key,k1.prime))
#print(pow(k1.public_key,k2.private_key,k2.prime))

#print(k1.shared_key)
#print(k2.shared_key)

#p1 = k1.public_key
#b1 = base64.b64encode(bytes(str(p1), 'ascii')).decode('utf-8')
#print(p1)
#print(b1)
#b2 = int(base64.b64decode(b1).decode('utf-8'))
#print(p1 == b2)
#print(b2)
#print(Random.new().read(AES.block_size))

key = b'1234567890123456'
chiper = AESCipher(key)
enc = chiper.encrypt("hui")
print(enc)
print(chiper.decrypt(enc))
#print(pack_bigint(int.from_bytes(rng(16), byteorder='big')))
#print(rng(16).decode())
