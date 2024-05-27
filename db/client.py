from pymongo import MongoClient

#db_client = MongoClient().local #instanciamos la clase || si no le indicamos nada se conecta al local

db_client = MongoClient(
    "mongodb+srv://codermexweb:codermexweb@cluster0.sfnbgtp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
).test
