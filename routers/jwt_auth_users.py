from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "zf7sdf76xcv6xcv677x8cv6xcjxcjkvhcxv87879797987987xcv9798xcv79xc7v9xc7v9xc8v7"

router = APIRouter(
                prefix="/jwtauth", 
                tags=["jwtauth"],
                responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})#en caso que alla problema va a tirar un 404

oauth2 = OAuth2PasswordBearer(tokenUrl="login")#autenticacion

#CONTEXTO DE INCRIPTACIÓN
crypt = CryptContext(schemes=["bcrypt"])#algoritmo de incriptación

class User(BaseModel): #basemodel esta dando la capacidad de crear una entidad
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "mouredev": {
        "username": "mouredev",
        "fullname": "Brais Moure",
        "email": "braismoure@gmail.com",
        "disabled": False,
        "password": "$2a$12$LjOUzV4dVqdUBzR67YYUWOEd3UG6487Be1wzSTj/loSf53rxxjr26"
    },
    "mouredev2": {
        "username": "mouredev2",
        "fullname": "Brais Moure 2",
        "email": "braismoure2@gmail.com",
        "disabled": True,
        "password": "$2a$12$uCPYDPqrlBYWOs3aP0ZjQubXc1qZDO/SXMn4kvV1jXH3oAXcz2Y8O"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas",headers={"WWW-Authenticate":"Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            return exception

    except JWTError:
        raise exception
    
    return search_user(username)
    
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): #Depends() -> en este caso le indica que va a recibir datos pero no depende de nadie
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):#valida contraseña cryptada
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expire = datetime.utcnow() + access_token_expiration #la hora del sistema + la hora de expiration

    access_token = {
                    "sub": user.username,
                    "exp": expire}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),"token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user