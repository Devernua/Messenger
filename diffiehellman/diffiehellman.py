# coding=utf-8

"""
diffiehellmann declares the main key exchange class.
"""

__version__ = '0.13.3'

from hashlib import sha256

from .decorators import requires_private_key
from .exceptions import MalformedPublicKey, RNGError
from .primes import PRIMES

try:
    from ssl import RAND_bytes
    rng = RAND_bytes
except(AttributeError, ImportError):
    raise RNGError


class DiffieHellman:
    """
    Implements the Diffie-Hellman key exchange protocol.
    """

    def __init__(self,
                 group=5,
                 key_length=200):

        self.key_length = max(200, key_length)
        self.generator = PRIMES[group]["generator"]
        self.prime = PRIMES[group]["prime"]

    def generate_private_key(self):
        """
        Generates a private key of key_length bits and attaches it to the object as the __private_key variable.
        :return: void
        :rtype: void
        """
        key_length = self.key_length // 8 + 8
        key = 0

        try:
            key = int.from_bytes(rng(key_length), byteorder='big')
        except:
            key = int(hex(rng(key_length)), base=16)

        self.__private_key = key
        #print("KEEEEEY: " + str(key))

    def verify_public_key(self, other_public_key):
        return self.prime - 1 > other_public_key > 2 and pow(other_public_key, (self.prime - 1) // 2, self.prime) == 1

    @requires_private_key
    def generate_public_key(self):
        """
        Generates public key.
        :return: void
        :rtype: void
        """
        self.public_key = pow(self.generator,
                              self.__private_key,
                              self.prime)

    @requires_private_key
    def generate_shared_secret(self, other_public_key, echo_return_key=False):
        """
        Generates shared secret from the other party's public key.
        :param other_public_key: Other party's public key
        :type other_public_key: int
        :param echo_return_key: Echo return shared key
        :type bool
        :return: void
        :rtype: void
        """
        if self.verify_public_key(other_public_key) is False:
            raise MalformedPublicKey

        self.shared_secret = pow(other_public_key,
                                 self.__private_key,
                                 self.prime)

        #shared_secret_as_bytes = self.shared_secret.to_bytes(self.shared_secret.bit_length() // 8 + 1, byteorder='big')

        #_h = sha256()
        #_h.update(bytes(shared_secret_as_bytes))

        #self.shared_key = _h.hexdigest()
        self.shared_key = int(str(self.shared_secret)[:16])

        if echo_return_key is True:
            return self.shared_key