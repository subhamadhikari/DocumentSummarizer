import os
import hashlib


def encrypt_pass(password: str):
    salt = os.urandom(32)
    print("salt",salt)
    print("type",type(salt))
    hash_object = hashlib.sha256()
    hash_object.update(salt + password.encode())
    hash_password = hash_object.hexdigest()

    return hash_password,salt

def verify_pass(db_password:str,password:str,salt:bytes):
    password_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
