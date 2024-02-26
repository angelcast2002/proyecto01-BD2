from typing import Union

import bcrypt
import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from starlette.responses import FileResponse, Response

import mongoManager as mm
from pydantic import BaseModel
from gridfs import GridFS
from datetime import datetime
from bson import ObjectId
from bcrypt import hashpw, checkpw, gensalt
from fastapi.middleware.cors import CORSMiddleware

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
def update_user(user: UserUpdate = Depends(), profile_pic: UploadFile = File(...)):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios
    fs = GridFS(db)
    # Verificar si el usuario ya existe
    if not users_collection.find_one({"_id": user.id}):
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario no existe"})

    # Guardar la imagen en GridFS
    profile_pic_id = fs.put(profile_pic.file, filename=profile_pic.filename)

    # Insertar el nuevo usuario en la base de datos
    user_data = user.dict()
    user_data["birthdate"] = datetime.strptime(user_data["birthdate"], "%Y-%m-%d")
    user_data['profilepic'] = profile_pic_id

    inserted_user = users_collection.update_one({"_id": user.id}, {"$set": user_data})
    mm.disconnect(client)

    # Return status code 200 and message: "User created"
    return {"status": 200, "message": "User updated"}


# Ruta para borrar un usuario
@app.delete("/users")
def delete_user(user_id: str):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios
    fs = GridFS(db)

    # Verificar si el usuario ya existe
    if not users_collection.find_one({"_id": user_id}):
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario ya existe"})

    # Borrar la imagen de perfil del usuario
    user_document = users_collection.find_one({"_id": user_id})
    fs.delete(user_document['profilepic'])

    # Borrar el usuario de la base de datos
    users_collection.delete_one({"_id": user_id})
    mm.disconnect(client)

    # Return status code 200 and message: "User deleted"
    return {"status": 200, "message": "User deleted"}


# Ruta para obtener la información de un usuario
@app.get("/users/profilepic")
def get_user(user_id: str):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios
    fs = GridFS(db)

    # Verificar si el usuario existe
    user_document = users_collection.find_one({"_id": user_id})
    if user_document is None:
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario no existe"})

    # Recuperar la imagen de perfil del usuario
    profile_pic = fs.get(user_document['profilepic']).read()

    image_bytes: bytes = profile_pic
    mm.disconnect(client)

    return Response(content=image_bytes, media_type="image/png")
    #return Response(content=image_bytes, media_type="image/png")

# Ruta que devuelve la información de un usuario, menos la foto, el password y el id. 
@app.get("/users")
def get_user_info(user_id: str):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios
    
    """ retornar tambien status code 200 y message: "User retrieved"""
    user_document = users_collection.find_one({"_id": user_id}, {"_id": 0, "password": 0, "profilepic": 0})
    if user_document is None:
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario no existe"})
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

    # 65db97526a2cdde556925375


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

    """
    [
    {
        "_id": {"$oid": "65db97526a2cdde556925375"},
        "arr_mensajes": [],
        "personas": ["prueba", "prueba2"]
    }
    ]

    
    Toda la información debería hacerse push en arr_mensajes. 
    ahí, en [[emisor, mensaje, esarchivo, fecha], [emisor, mensaje, esarchivo, fecha]...]
    """

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
    # fs = GridFS(db)

    if not users_collection.find_one({"_id": user_id}):
        raise HTTPException(status_code=404, detail={"status": 404, "message": "El usuario no existe"})

    conversations = conversations_collection.find({"personas": user_id})
    retrieved_conversations = []
    for conversation in conversations:
        other_person = conversation["personas"][0] if conversation["personas"][1] == user_id else \
        conversation["personas"][1]
        other_person_data = users_collection.find_one({"_id": other_person})
        other_person_name = f"{other_person_data['nombre']} {other_person_data['apellido']}"
        """
        profile_pic_id = other_person_data['profilepic']
        profile_pic = fs.get(profile_pic_id).read()
        profile_pic_b64 = b64encode(profile_pic).decode('utf-8')
        """
        last_message = conversation["arr_mensajes"][-1]

        retrieved_conversations.append({
            "id_conversacion": str(conversation["_id"]),
            "nombre_persona": other_person_name,
            "fecha_ultimo_mensaje": last_message["fechahora"],
            "contenido_ultimo_mensaje": last_message["mensaje"],
        })
    mm.disconnect(client)

    return {"status": 200, "message": "Conversations retrieved", "conversations": retrieved_conversations}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
