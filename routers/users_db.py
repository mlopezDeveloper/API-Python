# USERS DB API

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(
                prefix="/userdb", 
                tags=["userdb"],
                responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}}#en caso que alla problema va a tirar un 404
                )

@router.get("/", response_model=list[User]) #Le indico que quiero traerme una lista de usuarios
async def users():
    return users_schema(db_client.users.find())#devuelve todo

#path
@router.get("/{id}") #http://127.0.0.1:8000/user/id=1
async def user(id: str):
    return search_user("_id", ObjectId(id))
#query
@router.get("/") #http://127.0.0.1:8000/userquery/?id=1
async def user(id: str):
    return search_user("_id", ObjectId(id))

#post
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED) #le indico como se va a crear un usuario me devuelva un 201 que es un estado que se creo algo
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        #return {"error": "El usuario ya existe"}
        #return HTTPException(status_code=204, detail="El usuario ya existe")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    # users_list.append(user)

    # Insert_one -> para insertar 1
    # Insert_many -> para insertar muchos
    user_dict = dict(user)
    del user_dict["id"] #eliminamos el id para autogenerarlo el propio mongoDB y no que no le pase un null cuando nosostros

    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.users.find_one({"_id": id}))#json
    

    return User(**new_user)#objeto de tipo usuario

#put
@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace(
            {
                "_id": ObjectId(user.id)
            },user_dict
        )
    except:
        return {"error":"No se ha actualizado el usuario"}
        
    return search_user("_id", ObjectId(user.id))

#delete
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error":"No se ha eliminado el usuario"}

def search_user(field: str, key):
    
    try:
        user =  db_client.users.find_one({field: key})# accediendo a la base y trayendo el mail 
        return User(**user_schema(user))#con el user_schema los transformamos
    except:
        return {"error": "No se ha encontrado el usuario"}
