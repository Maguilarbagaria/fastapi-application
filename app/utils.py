from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #hashing algorithm

def hash(pss:str):
    return pwd_context.hash(pss)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)