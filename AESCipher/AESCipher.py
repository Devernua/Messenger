from Crypto.Cipher import AES
from Crypto import Random
from bigint.big import *


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return base64.standard_b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
            enc = base64.standard_b64decode(enc)
            iv = enc[:16]
            cipher = AES.new(self.key, AES.MODE_CFB, iv)
            return cipher.decrypt(enc[16:]).decode()
