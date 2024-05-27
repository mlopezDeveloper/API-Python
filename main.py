from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)


app.mount("/static", StaticFiles(directory="static"),name="static")#para montar recursos estaticos

    #siempre que nosotros llamamos a un servidor, la operacion que se ejecuta debe ser asincrono
    #que es asincrono (async), una peticion asincronico -> nosotros desde la web o movil llamamos al servidor y 
    #nuestra aplicacion no puede hacer nada hasta que retorne algo el servidor
    #Tipos de peticiones - Get es practicamente todo lo que hacemos cuando vamos a un explorar y llamamos una web
    #cuando voy a un web, lo que hago es un get a HTTPS:// NOMBRE DE LA WEB osea quiero obtener algo, que tiene esa url
    #Protocolo de comunicacion standar -> HTTP - HTTPS(con seguridad)

@app.get("/")
async def root(): 
    return "Hola FastAPI"

@app.get("/url")
async def url(): 
    return { "url":"htpps://mouredev.com/python" }

