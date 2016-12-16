from diffiehellman.diffiehellman import DiffieHellman

k1 = DiffieHellman()
k1.generate_public_key()
k2 = DiffieHellman()
k2.generate_public_key()

k1.generate_shared_secret(k2.public_key)
k2.generate_shared_secret(k1.public_key)

print(k1 == k2)

print(pow(k2.public_key,k1.private_key,k1.prime))
print(pow(k1.public_key,k2.private_key,k2.prime))

print(k1.shared_key)
print(k2.shared_key)