from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Définir une fonction de hash
def hash(password: str):
    return pwd_context.hash(password)

#vérification de Mdp
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)