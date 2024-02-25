from typing import Union

import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from starlette.responses import FileResponse

import mongoManager as mm
from pydantic import BaseModel
from gridfs import GridFS
from datetime import datetime
from bson import ObjectId
from bcrypt import hashpw, checkpw, gensalt

app = FastAPI()

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
        raise HTTPException(status_code=400, detail="El usuario ya existe")

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


    #Return status code 200 and message: "User created"
    return {"status": 200, "message": "User created"}

# Ruta para obtener la información de un usuario
@app.get("/users/get")
def get_user(user_id: str):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios
    fs = GridFS(db)

    # Verificar si el usuario existe
    user_document = users_collection.find_one({"_id": user_id})
    if user_document is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


    # Recuperar la imagen de perfil del usuario
    profile_pic = fs.get(user_document['profilepic']).read()
    profile_pic = profile_pic.decode('utf-8')

    return FileResponse(profile_pic, media_type="image/jpeg")

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
        raise HTTPException(status_code=400, detail="La conversación ya existe")

    # Crear la conversación
    conversation_data = {
        "arr_mensajes": [],
        "personas": [members.id_usuario1, members.id_usuario2]
    }
    inserted_conversation = conversations_collection.insert_one(conversation_data)
    mm.disconnect(client)

    #Return status code 200 and message: "Conversation created", devolver el id de la conversación
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
        raise HTTPException(status_code=400, detail="La conversación no existe")
    
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
    conversations_collection.update_one({"_id": ObjectId(message.id_conversacion)}, {"$push": {"arr_mensajes": mensaje_doc}})
    mm.disconnect(client)

    #Return status code 200 and message: "Message added"
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
@app.post("/conversations/retrieve/")
async def retrieve_conversations(user: user_id):
    client = mm.connect()
    db = client['ProyectoDB2']
    conversations_collection = db.conversacion
    users_collection = db.usuarios
    fs = GridFS(db)

    # Verificar si el usuario existe
    if not users_collection.find_one({"_id": user.id}):
        raise HTTPException(status_code=400, detail="El usuario no existe")

    # Recuperar las conversaciones del usuario
    conversations = conversations_collection.find({"personas": user.id})
    retrieved_conversations = []
    for conversation in conversations:
        # Recuperar el nombre de la persona con la que se está conversando
        other_person = conversation["personas"][0] if conversation["personas"][1] == user.id else conversation["personas"][1]
        other_person_data = users_collection.find_one({"_id": other_person})
        other_person_name = f"{other_person_data['nombre']} {other_person_data['apellido']}"
        # Recuperar la foto de perfil de la persona con la que se está conversando
        #profile_pic = fs.get(other_person_data['profilepic']).read()
        #profile_pic = profile_pic.decode('utf-8')
        # Recuperar el último mensaje
        last_message = conversation["arr_mensajes"][-1]
        # Crear el objeto de conversación
        retrieved_conversations.append({
            "id_conversacion": str(conversation["_id"]),
            "nombre_persona": other_person_name,
            "fecha_ultimo_mensaje": last_message["fechahora"],
            "contenido_ultimo_mensaje": last_message["mensaje"],
        })
    mm.disconnect(client)

    #Return status code 200 and message: "Conversations retrieved", devolver las conversaciones
    return {"status": 200, "message": "Conversations retrieved", "conversations": retrieved_conversations}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)