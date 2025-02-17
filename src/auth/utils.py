from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def gen_pass_hash(password: str) -> str:
    return pwd_cxt.hash(password)

def verify_pass(plain_password: str, hashed_password: str) -> bool:
    return pwd_cxt.verify(plain_password, hashed_password)    