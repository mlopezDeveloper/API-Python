from pydantic import BaseModel #esta libreria nos permitia gestionar modelos a nivel entidad
from typing import Optional


class User(BaseModel):#basemodel esta dando la capacidad de crear una entidad
    id: str | None = None
    username: str
    email: str


