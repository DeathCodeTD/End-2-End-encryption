import socket
import sys
import time
import math
from mod import Mod
import random
import cryptography
from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# modular arithmatic


my_privatenum = random.randint(1, 10)
my_pr = math.pow(3, my_privatenum)
my_num = my_pr % 17

# print(my_num)
# print(my_pr)


s = socket.socket()
host = input(str("Please enter the hostname of the server : "))
port = 8080
s.connect((host, port))
print(" Connected to chat server")
s_num = s.recv(1024)
s_num = s_num.decode()
s_num = int(s_num)
s_num = pow(s_num, my_privatenum)
secret_num = s_num % 17
print(secret_num)

# encryption key
send_num = my_num
s.send(str(send_num).encode())

password_provided = str(secret_num)
password = password_provided.encode()

salt = b"\xb9\x1f|}'S\xa1\x96\xeb\x154\x04\x88\xf3\xdf\x05"

kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                 length=32,
                 salt=b'dfjasdlkfja;fj;lkj;',
                 iterations=100000,
                 backend=default_backend())

key = base64.urlsafe_b64encode(kdf.derive(password))
print(key)
print(secret_num)
print(salt)

fernet = Fernet(key)

while 1:
    incoming_message = s.recv(1024)
    print(f'incoming_message:{incoming_message}(encrypted)')
    incoming_message = fernet.decrypt(incoming_message).decode('ASCII')
    print(" Server : ", incoming_message)
    print("")
    message = input(str(">> "))
    message = message.encode()
    message = fernet.encrypt(message).decode('ASCII')
    s.send(message.encode())
    print("message has been sent...")
    print("")
