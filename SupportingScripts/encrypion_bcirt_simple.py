#!/usr/bin/python
#https://nitratine.net/blog/post/encryption-and-decryption-in-python/
# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : scripts/encryption_bcirt_simple.py
# Author            : Balazs Lendvay
# Date created      : 2019.08.18
# Purpose           : Encryption script for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.08.18  Lendvay     1      Initial file
# **********************************************************************;
# from django.shortcuts import render

from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class bCIRT_Encryption():
    def __init__(self):
        self.key = None
        pass

    def generate_key_manual(self, ppassword, psalt):
        password_provided = ppassword # This is input in the form of a string
        password = password_provided.encode() # Convert to type bytes
        # salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        salt = psalt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
        return key

    def encrypt_string(self, pmsg, pkey):
        # Encrypt a string in bytes format and output a base64 representation
        # from cryptography.fernet import Fernet
        message = pmsg.encode()
        f = Fernet(pkey)
        encrypted = f.encrypt(message)
        return encrypted

    def decrypt_string(self, pkey, pencrypted):
        # decrypt the text
        # encrypted = b"...encrypted bytes..."
        f = Fernet(pkey)
        decrypted = f.decrypt(pencrypted)
        return decrypted

# key = bCIRT_Encryption().generate_key_manual('password','salt_')
# print(key)
# strenc = bCIRT_Encryption().encrypt_string('Almafa', key)
# print(strenc)
# strdec = bCIRT_Encryption().decrypt_string(key, strenc)
# print(strdec)
