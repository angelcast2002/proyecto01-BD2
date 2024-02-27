from typing import Union

import bcrypt
import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from starlette.responses import FileResponse, Response, JSONResponse

import mongoManager as mm
from pydantic import BaseModel
from gridfs import GridFS
from datetime import datetime
from bson import ObjectId
from bcrypt import hashpw, checkpw, gensalt
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Definición del modelo de usuario
class User(BaseModel):
    id: str
    password: str
    nombre: str
    apellido: str
    birthdate: str


# Ruta para crear un nuevo usuario
@app.post("/users")
def create_user(user: User = Depends(), profile_pic: UploadFile = File(...)):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios
    fs = GridFS(db)

    # Verificar si el usuario ya existe
    if users_collection.find_one({"_id": user.id}):
        raise HTTPException(status_code=400, detail={"status": 400, "message": "Usuario ya existe"})

    # Guardar la imagen en GridFS
    profile_pic_id = fs.put(profile_pic.file, filename=profile_pic.filename)

    # Hashear la contraseña antes de almacenarla
    hashed_password = hashpw(user.password.encode('utf-8'), gensalt())

    # Insertar el nuevo usuario en la base de datos
    user_data = user.dict()
    user_data["birthdate"] = datetime.strptime(user_data["birthdate"], "%Y-%m-%d")
    user_data['password'] = hashed_password.decode('utf-8')
    user_data['profilepic'] = profile_pic_id
    user_data['_id'] = user_data.pop('id')

    inserted_user = users_collection.insert_one(user_data)
    mm.disconnect(client)

    # Return status code 200 and message: "User created"
    return {"status": 200, "message": "User created"}


class UserUpdate(BaseModel):
    id: str
    nombre: str
    apellido: str
    birthdate: str


# Ruta para actualizar la información de un usuario
@app.put("/users")
def update_user(user: UserUpdate = Depends()):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios
    # Verificar si el usuario ya existe
    if not users_collection.find_one({"_id": user.id}):
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario no existe"})

    # Insertar el nuevo usuario en la base de datos
    user_data = user.dict()
    user_data["birthdate"] = datetime.strptime(user_data["birthdate"], "%Y-%m-%d")

    inserted_user = users_collection.update_one({"_id": user.id}, {"$set": user_data})
    mm.disconnect(client)

    # Return status code 200 and message: "User created"
    return {"status": 200, "message": "User updated"}

# Ruta para actualizar la foto de perfil de un usuario
@app.put("/users/profilepic")
def update_profilepic(user_id: str, profile_pic: UploadFile = File(...)):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios
    fs = GridFS(db)

    # Verificar si el usuario ya existe
    if not users_collection.find_one({"_id": user_id}):
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario no existe"})

    # Guardar la imagen en GridFS
    profile_pic_id = fs.put(profile_pic.file, filename=profile_pic.filename)

    # Actualizar la imagen de perfil del usuario
    users_collection.update_one({"_id": user_id}, {"$set": {"profilepic": profile_pic_id}})
    mm.disconnect(client)

    # Return status code 200 and message: "Profile picture updated"
    return {"status": 200, "message": "Profile picture updated"}

class UserDelete(BaseModel):
    id: str

# Ruta para borrar un usuario
@app.post("/users/delete")
def delete_user(user : UserDelete):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios
    conversations_collection = db.conversacion
    fs = GridFS(db)

    # Verificar si el usuario ya existe
    if not users_collection.find_one({"_id": user.id}):
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario no existe"})

    # Borrar la imagen de perfil del usuario
    user_document = users_collection.find_one({"_id": user.id})
    fs.delete(user_document['profilepic'])

    # Borrar el usuario de la base de datos
    users_collection.delete_one({"_id": user.id})

    # Verificar si todas las personas en una conversación han sido eliminadas
    conversations = conversations_collection.find({"personas": user.id})
    for conversation in conversations:
        if not users_collection.find_one({"_id": {"$in": conversation["personas"]}}):
            # Si todas las personas en la conversación han sido eliminadas, eliminar la conversación
            conversations_collection.delete_one({"_id": conversation["_id"]})

    mm.disconnect(client)

    # Return status code 200 and message: "User deleted"
    return {"status": 200, "message": "User deleted"}


# Ruta para obtener la información de un usuario
@app.post("/users/profilepic")
def get_user(user: UserDelete):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios
    fs = GridFS(db)

    # Verificar si el usuario existe
    user_document = users_collection.find_one({"_id": user.id}, {"profilepic": 1})
    if user_document is None:
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario no existe"})

    # Recuperar la imagen de perfil del usuario
    profile_pic = fs.get(user_document['profilepic']).read()

    image_bytes: bytes = profile_pic


    mm.disconnect(client)

    return Response(content=image_bytes, media_type="image/png")


# Ruta que devuelve la información de un usuario, menos la foto, el password y el id.
@app.post("/users/info")
def get_user_info(user: UserDelete):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios

    """ retornar tambien status code 200 y message: "User retrieved"""
    user_document = users_collection.find_one({"_id": user.id}, {"_id": 0, "password": 0, "profilepic": 0})
    if user_document is None:
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario no existe"})

    user_document['birthdate'] = users_collection.aggregate([
        {"$match": {"_id": user.id}},
        {"$project": {"birthdate": {"$dateToString": {"format": "%Y-%m-%d", "date": "$birthdate"}}}}
    ]).next()["birthdate"]

    mm.disconnect(client)
    return {"status": 200, "message": "User retrieved", "user_info": user_document}


# Definición del modelo de datos para el inicio de sesión
class LoginData(BaseModel):
    id: str
    password: str


# Ruta para el inicio de sesión
@app.post("/login")
def login(login_data: LoginData):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios

    user_id = login_data.id
    password = login_data.password

    # Verificar si el usuario existe
    user_document = users_collection.find_one({"_id": user_id})
    if user_document is None:
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario no existe"})

    # Verificar la contraseña
    hashed_password = user_document["password"]  # Obtener la contraseña hashada de la base de datos
    if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail={"status": 401, "message": "Credenciales inválidas"})

    mm.disconnect(client)
    # Inicio de sesión exitoso
    return {"status": 200, "message": "Inicio de sesión exitoso"}


class members_conversation(BaseModel):
    id_usuario1: str
    id_usuario2: str

# Ruta para crear una conversación
@app.post("/conversations/")
async def create_conversation(members: members_conversation):
    client = mm.connect()
    db = client['ProyectoDB2']
    conversations_collection = db.conversacion

    # verifica si los usuarios existen
    users_collection = db.usuarios
    if not users_collection.find_one({"_id": members.id_usuario1}):
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario 1 no existe"})
    if not users_collection.find_one({"_id": members.id_usuario2}):
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario 2 no existe"})
    

    # Verificar si la conversación ya existe
    if conversations_collection.find_one({"personas": {"$all": [members.id_usuario1, members.id_usuario2]}}):
        raise HTTPException(status_code=400, detail={"status": 400, "message": "La conversacion ya existe"})

    # Crear la conversación
    conversation_data = {
        "arr_mensajes": [],
        "personas": [members.id_usuario1, members.id_usuario2]
    }
    inserted_conversation = conversations_collection.insert_one(conversation_data)
    mm.disconnect(client)

    # Return status code 200 and message: "Conversation created", devolver el id de la conversación
    return {"status": 200, "message": "Conversation created", "id_conversacion": str(inserted_conversation.inserted_id)}



class message(BaseModel):
    id_conversacion: str
    emisor: str
    mensaje: str
    es_archivo: bool


# Ruta para añadir un mensaje a una conversación
@app.post("/messages/")
async def add_message(message: message):
    client = mm.connect()
    db = client['ProyectoDB2']
    conversations_collection = db.conversacion
    fs = GridFS(db)
    # Verificar si el usuario existe
    users_collection = db.usuarios
    if not users_collection.find_one({"_id": message.emisor}):
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario no existe"})

    # Verificar si la conversación existe
    if not conversations_collection.find_one({"_id": ObjectId(message.id_conversacion)}):
        raise HTTPException(status_code=400, detail={"status": 400, "message": "La conversacion no existe"})

    # Guardar el mensaje en GridFS si es un archivo
    if message.es_archivo:
        mensaje_id = fs.put(message.mensaje.encode('utf-8'), filename=f"msg_{datetime.now().timestamp()}")
        mensaje = str(mensaje_id)
    else:
        mensaje = message.mensaje

    # Crear el mensaje
    mensaje_doc = {
        "emisor": message.emisor,
        "mensaje": mensaje,
        "es_archivo": message.es_archivo,
        "fechahora": datetime.now()
    }

    # Insertar el mensaje en la conversación
    conversations_collection.update_one({"_id": ObjectId(message.id_conversacion)},
                                        {"$push": {"arr_mensajes": mensaje_doc}})
    mm.disconnect(client)

    # Return status code 200 and message: "Message added"
    return {"status": 200, "message": "Message added", "id_conversacion": message.id_conversacion}


"""
Debe devolver:
- nombre de la persona con la que se está conversando
- id de la conversación
- fecha del último mensaje
- contenido del último mensaje
- foto de perfil de la persona con la que se está conversando
"""


class user_id(BaseModel):
    id: str


# Ruta para recuperar las conversaciones de un usuario.
class RetrieveConversationsRequest(BaseModel):
    user_id: str


@app.post("/conversations/retrieve/")
async def retrieve_conversations(request: RetrieveConversationsRequest):
    user_id = request.user_id
    client = mm.connect()
    db = client['ProyectoDB2']
    conversations_collection = db.conversacion
    users_collection = db.usuarios

    if not users_collection.find_one({"_id": user_id}):
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario no existe"})

    # Utilizando la agregación para ordenar por la fecha del último mensaje
    pipeline = [
        {"$match": {"personas": user_id}},  # Filtra las conversaciones que incluyen al usuario
        {"$addFields": {"ultimo_mensaje": {"$arrayElemAt": ["$arr_mensajes", -1]}}},  # Añade el último mensaje a cada documento
        {"$sort": {"ultimo_mensaje.fechahora": -1}},  # Ordena los documentos por la fecha del último mensaje de forma descendente
    ]
    conversations = conversations_collection.aggregate(pipeline)

    retrieved_conversations = []
    for conversation in conversations:
        other_person = conversation["personas"][0] if conversation["personas"][1] == user_id else conversation["personas"][1]
        other_person_data = users_collection.find_one({"_id": other_person})
        other_person_name = f"{other_person_data['nombre']} {other_person_data['apellido']}"
        last_message = conversation["ultimo_mensaje"]

        retrieved_conversations.append({
            "id_conversacion": str(conversation["_id"]),
            "nombre_persona": other_person_name,
            "fecha_ultimo_mensaje": last_message["fechahora"],
            "contenido_ultimo_mensaje": last_message["mensaje"],
        })
    mm.disconnect(client)

    length = len(retrieved_conversations)

    return {"status": 200, "message": "Conversations retrieved", "num_conversations": length , "conversations": retrieved_conversations}

class RetrieveConversationsRequestSpecific(BaseModel):
    user_id: str
    limit: int

# Ruta para retornar n conversaciones. 
@app.post("/conversations/retrieve/limit")
async def retrieve_conversations(request: RetrieveConversationsRequestSpecific):
    user_id = request.user_id
    limit = request.limit
    client = mm.connect()
    db = client['ProyectoDB2']
    conversations_collection = db.conversacion
    users_collection = db.usuarios

    if not users_collection.find_one({"_id": user_id}):
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario no existe"})
    
    pipeline = [
        {"$match": {"personas": user_id}},  # Filtra las conversaciones que incluyen al usuario
        {
            "$addFields": {
                "ultimo_mensaje": {"$arrayElemAt": ["$arr_mensajes", -1]},
                "cantidad_mensajes": {"$size": "$arr_mensajes"}
            }
        },
        {"$sort": {"ultimo_mensaje.fechahora": -1}},  # Ordena los documentos por la fecha del último mensaje de forma descendente
        {"$limit": limit}
    ]

    retrieved_conversations = []
    for conversation in conversations_collection.aggregate(pipeline):
        # Verifica si existe un último mensaje
        if conversation.get("ultimo_mensaje"):
            other_person = conversation["personas"][0] if conversation["personas"][1] == user_id else conversation["personas"][1]
            other_person_data = users_collection.find_one({"_id": other_person})
            other_person_name = f"{other_person_data['nombre']} {other_person_data['apellido']}"
            last_message = conversation["ultimo_mensaje"]

            retrieved_conversations.append({
                "id_conversacion": str(conversation["_id"]),
                "nombre_persona": other_person_name,
                "fecha_ultimo_mensaje": last_message["fechahora"],
                "contenido_ultimo_mensaje": last_message["mensaje"],
                "cantidad_mensajes": conversation["cantidad_mensajes"]
            })
        else:
            # Maneja el caso en el que no hay mensajes en la conversación
            other_person = conversation["personas"][0] if conversation["personas"][1] == user_id else conversation["personas"][1]
            other_person_data = users_collection.find_one({"_id": other_person})
            other_person_name = f"{other_person_data['nombre']} {other_person_data['apellido']}"

            retrieved_conversations.append({
                "id_conversacion": str(conversation["_id"]),
                "nombre_persona": other_person_name,
                "fecha_ultimo_mensaje": "",
                "contenido_ultimo_mensaje": "",
                "cantidad_mensajes": 0
            })

    length = len(retrieved_conversations)

    mm.disconnect(client)
    return {"status": 200, "message": "Conversations retrieved", "num_conversations": length, "conversations": retrieved_conversations}




# Ruta para recuperar los mensajes de una conversación
class RetrieveMessagesRequest(BaseModel):
    conversation_id: str

@app.post("/messages/retrieve/")
async def retrieve_messages(request: RetrieveMessagesRequest):
    conversation_id = request.conversation_id
    client = mm.connect()
    db = client['ProyectoDB2']
    conversations_collection = db.conversacion
    users_collection = db.usuarios

    conversation = conversations_collection.find_one({"_id": ObjectId(conversation_id)})
    if conversation is None:
        raise HTTPException(status_code=404, detail={"status": 404, "message": "La conversacion no existe"})

    retrieved_messages = []
    for message in conversation["arr_mensajes"]:
        emisor_data = users_collection.find_one({"_id": message["emisor"]})
        emisor_name = f"{emisor_data['nombre']} {emisor_data['apellido']}"

        retrieved_messages.append({
            "id_emisor": message["emisor"],
            "emisor": emisor_name,
            "mensaje": message["mensaje"],
            "es_archivo": message["es_archivo"],
            "fechahora": message["fechahora"]
        })
    mm.disconnect(client)

    return {"status": 200, "message": "Messages retrieved", "messages": retrieved_messages}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
