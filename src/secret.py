from nacl.public import PrivateKey, SealedBox
from nacl.secret import SecretBox
from nacl.utils import random

import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def new_symmetric_key():
    return random(SecretBox.KEY_SIZE)

def new_pair():
    sk = PrivateKey.generate()
    return sk.encode(), sk.public_key.encode()

def symmetric_encrypt(key: bytes, plaintext: bytes):
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_plaintext) + encryptor.finalize()
    # 密文结构 cipher + '$$$' + iv
    ciphertext = ct + b'$$$' + iv
    return ciphertext

def symmetric_decrypt(key:bytes, ciphertext:bytes):
    ct, iv = ciphertext.rsplit(b'$$$')
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_plaintext = unpadder.update(padded_plaintext)
    unpadded_plaintext += unpadder.finalize()
    return unpadded_plaintext

def encrypt(sk:bytes, plaintext: bytes):
    return SealedBox(PrivateKey(sk).public_key).encrypt(plaintext)

def decrypt(sk:bytes, ciphertext: bytes):
    return SealedBox(PrivateKey(sk)).decrypt(ciphertext)