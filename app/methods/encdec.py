import bcrypt


# hashing function
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    #returns the string of bytes
    return hashed.decode()

# verification function   
def verify_password(password: bytes, hashed_hex: bytes) -> bool:
    return bcrypt.checkpw(password, hashed_hex)

