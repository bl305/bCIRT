#!/usr/bin/python
#https://nitratine.net/blog/post/encryption-and-decryption-in-python/

#Generate a secure key
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print("Orig key: %s"%(key))

#Manual key generation
# import base64
# import os
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
#
# password_provided = "password" # This is input in the form of a string
# password = password_provided.encode() # Convert to type bytes
# salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
# kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=salt,
#     iterations=100000,
#     backend=default_backend()
# )
# key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once

#Write the key to a file
file = open('encryption.key', 'wb')
file.write(key) # The key is type bytes still
file.close()

#Read th key back from the file
file = open('encryption.key', 'rb')
key = file.read() # The key will be type bytes
print("Read key: %s"%(key))
file.close()

# Encrypt a string in bytes format and output a base64 representation
# from cryptography.fernet import Fernet
message = "SECRET TEXT".encode()
f = Fernet(key)
encrypted = f.encrypt(message)
print("Encrypted:%s"%(encrypted))

# decrypt the text
# from cryptography.fernet import Fernet
# encrypted = b"...encrypted bytes..."
f = Fernet(key)
decrypted = f.decrypt(encrypted)
print("Decrypted:%s"%(decrypted))

# Encrypt files
# from cryptography.fernet import Fernet
# key = b'' # Use one of the methods to get a key (it must be the same when decrypting)
# input_file = 'test.txt'
# output_file = 'test.encrypted'
#
# with open(input_file, 'rb') as f:
#     data = f.read()
#
# fernet = Fernet(key)
# encrypted = fernet.encrypt(data)
#
# with open(output_file, 'wb') as f:
#     f.write(encrypted)
#
# You can delete input_file if you want

# Decrypt files:
# from cryptography.fernet import Fernet
# key = b'' # Use one of the methods to get a key (it must be the same as used in encrypting)
# input_file = 'test.encrypted'
# output_file = 'test.txt'
#
# with open(input_file, 'rb') as f:
#     data = f.read()
#
# fernet = Fernet(key)
# encrypted = fernet.decrypt(data)
#
# with open(output_file, 'wb') as f:
#     f.write(encrypted)
#
# # You can delete input_file if you want