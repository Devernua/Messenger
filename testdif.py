from diffiehellman.diffiehellman import DiffieHellman
import base64
k1 = DiffieHellman()
k1.generate_public_key()
k2 = DiffieHellman()
k2.generate_public_key()

k1.generate_shared_secret(k2.public_key)
k2.generate_shared_secret(k1.public_key)

print(k1.shared_key == k2.shared_key)

#print(pow(k2.public_key,k1.private_key,k1.prime))
#print(pow(k1.public_key,k2.private_key,k2.prime))

print(k1.shared_key)
print(k2.shared_key)

p1 = k1.public_key
b1 = base64.b64encode(bytes(str(p1), 'ascii')).decode('utf-8')
print(p1)
print(b1)
b2 = base64.b64decode(b1)
print(b2)

