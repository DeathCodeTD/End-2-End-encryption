import socket
import sys
import time
import math
from mod import Mod
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import cryptography
from cryptography.fernet import Fernet
import random
## end of imports ###
# modular arithmatic
my_privatenum = random.randint(1, 10)
my_pr = pow(3, my_privatenum)
my_num = my_pr % 17

### init ###

s = socket.socket()
host = socket.gethostname()
print(" server will start on host : ", host)
port = 8080
s.bind((host, port))
print("")
print(" Server done binding to host and port successfully")
print("")
print("Server is waiting for incoming connections")
print("")
s.listen(1)
conn, addr = s.accept()
print(addr, " Has connected to the server and is now online ...")
print("")
my_num = str(my_num).encode()
conn.send(my_num)

c_num = conn.recv(1024)
c_num = c_num.decode()
c_num = float(c_num)
c_num = int(c_num)
c_num = math.pow(c_num, my_privatenum)
secret_num = c_num % 17
secret_num = int(secret_num)
print(secret_num)
# creating the encryption key
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
print(salt)
print(secret_num)

while 1:
    message = input(str(">> "))
    message = message.encode()

    # encryption
    fernet = Fernet(key)
    message = fernet.encrypt(message).decode('ASCII')

    conn.send(message.encode())
    print("message has been sent...")
    print("")
    incoming_message = conn.recv(1024)
    print(f'incoming message:{incoming_message}(encrypted)')
    incoming_message = fernet.decrypt(incoming_message).decode('ASCII')
    print(" Client : ", incoming_message)
    print("")
    
