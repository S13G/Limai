import base64

import bcrypt


def hash_password(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    # Encode to base64 for safe storage as string
    encoded_hashed_password = base64.b64encode(hashed_password).decode()
    return encoded_hashed_password


def verify(plain_password, hashed_password) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    # Decode the base64 encoded hashed password back to bytes
    hashed_password = base64.b64decode(hashed_password.encode('utf-8'))
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)
