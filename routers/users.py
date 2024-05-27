from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()#instancia

#Entidad user

class User(BaseModel): #basemodel esta dando la capacidad de crear una entidad
    id: int
    name: str
    surname: str
    url: str
    age: int 

users_list = [
        User(id = 1, name = "Marcos", surname = "Lopez", url = "https://moure.dev", age = 28),
        User(id = 2, name = "Laura", surname = "Ibarra", url = "https://moure.dev", age = 24),
        User(id = 3, name = "Brais", surname = "Moure", url = "https://moure.dev", age = 35)
        ]

@router.get("/usersjson")
async def usersjson():
    return [{"name":"Marcos", "surname":"Lopez", "url":"https://moure.dev", "age":28},
            {"name":"Laura", "surname":"Ibarra", "url":"https://moure.dev","age":24},
            {"name":"Brais", "surname":"Moure", "url":"https://moure.dev","age":35}]

@router.get("/users")
async def users():
    return users_list

#path
@router.get("/user/{id}") #http://127.0.0.1:8000/user/id=1
async def user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
#query
@router.get("/userquery/") #http://127.0.0.1:8000/userquery/?id=1
async def user(id: int):
    return search_user(id)

#post
@router.post("/user/", response_model=User, status_code=201) #le indico como se va a crear un usuario me devuelva un 201 que es un estado que se creo algo
async def user(user: User):
    if type(search_user(user.id)) == User:
        #return {"error": "El usuario ya existe"}
        #return HTTPException(status_code=204, detail="El usuario ya existe")
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user

#put
@router.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error":"Non se ha actualizado el usuario"}
    else:
        return user

#delete
@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index] #eliminamos
            found = True
    if not found:
        return {"error":"No se ha eliminado el usuario"}

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}