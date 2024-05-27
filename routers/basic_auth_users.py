from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#OAuth2PasswordBearer -> se va a encargar de gestionar la autenticacion osea el usuario y contraseña
#OAuth2PasswordRequestForm -> la forma en la que se va a enviar a nuestro backend a nuestro api estos criterios de autoenticacion, es decir la forma en la que
#nosotros tenemos que enviar desde el cliente el usuario y la contraseña y la forma que el backend va a capturar el usuario y contraseña para ver si de verdad
#es un usuario de nuestro sistema

router = APIRouter(
                prefix="/basicauth", 
                tags=["basicauth"],
                responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}}#en caso que alla problema va a tirar un 404
                )


oauth2 = OAuth2PasswordBearer(tokenUrl="login")#autenticacion


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
        "password": "123456"
    },
    "mouredev2": {
        "username": "mouredev2",
        "fullname": "Brais Moure 2",
        "email": "braismoure2@gmail.com",
        "disabled": True,
        "password": "654321"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas",headers={"WWW-Authenticate":"Bearer"})
    if user.disabled:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): #Depends() -> en este caso le indica que va a recibir datos pero no depende de nadie
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    return {"access_token": user.username,"token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
