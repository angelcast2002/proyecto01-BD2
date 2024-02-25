from datetime import datetime
from typing import Union
import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gridfs import GridFS
from bson import ObjectId
from bcrypt import hashpw, gensalt
from base64 import b64encode
import motor.motor_asyncio
import mongoManager as mm

app = FastAPI()

class User(BaseModel):
    id: str
    password: str
    nombre: str
    apellido: str
    birthdate: str

@app.post("/users")
def create_user(user: User = Depends(), profile_pic: UploadFile = File(...)):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios
    fs = GridFS(db)

    if users_collection.find_one({"_id": user.id}):
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    profile_pic_id = fs.put(profile_pic.file, filename=profile_pic.filename)
    hashed_password = hashpw(user.password.encode('utf-8'), gensalt())

    user_data = user.dict()
    user_data["birthdate"] = datetime.strptime(user_data["birthdate"], "%Y-%m-%d")
    user_data['password'] = hashed_password.decode('utf-8')
    user_data['profilepic'] = profile_pic_id
    user_data['_id'] = user_data.pop('id')

    users_collection.insert_one(user_data)
    mm.disconnect(client)

    return {"status": 200, "message": "User created"}

@app.get("/users/get")
def get_user(user_id: str):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios
    fs = GridFS(db)

    user_document = users_collection.find_one({"_id": user_id})
    if user_document is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    profile_pic = fs.get(user_document['profilepic']).read()
    return FileResponse(profile_pic, media_type="image/jpeg")

class MembersConversation(BaseModel):
    id_usuario1: str
    id_usuario2: str

@app.post("/conversations/")
async def create_conversation(members: MembersConversation):
    client = mm.connect()
    db = client['ProyectoDB2']
    conversations_collection = db.conversacion  

    if conversations_collection.find_one({"personas": {"$all": [members.id_usuario1, members.id_usuario2]}}):
        raise HTTPException(status_code=400, detail="La conversación ya existe")

    conversation_data = {"arr_mensajes": [], "personas": [members.id_usuario1, members.id_usuario2]}
    inserted_conversation = conversations_collection.insert_one(conversation_data)
    mm.disconnect(client)

    return {"status": 200, "message": "Conversation created", "id_conversacion": str(inserted_conversation.inserted_id)}

class Message(BaseModel):
    id_conversacion: str
    emisor: str
    mensaje: str
    es_archivo: bool

@app.post("/messages/")
async def add_message(message: Message):
    client = mm.connect()
    db = client['ProyectoDB2']
    conversations_collection = db.conversacion
    fs = GridFS(db)

    if not conversations_collection.find_one({"_id": ObjectId(message.id_conversacion)}):
        raise HTTPException(status_code=400, detail="La conversación no existe")

    mensaje = message.mensaje if not message.es_archivo else str(fs.put(message.mensaje.encode('utf-8'), filename=f"msg_{datetime.now().timestamp()}"))

    mensaje_doc = {"emisor": message.emisor, "mensaje": mensaje, "es_archivo": message.es_archivo, "fechahora": datetime.now()}
    conversations_collection.update_one({"_id": ObjectId(message.id_conversacion)}, {"$push": {"arr_mensajes": mensaje_doc}})
    mm.disconnect(client)

    return {"status": 200, "message": "Message added", "id_conversacion": message.id_conversacion}

class RetrieveConversationsRequest(BaseModel):
    user_id: str

@app.post("/conversations/retrieve/")
async def retrieve_conversations(request: RetrieveConversationsRequest):
    user_id = request.user_id
    client = mm.connect()
    db = client['ProyectoDB2']
    conversations_collection = db.conversacion
    users_collection = db.usuarios
    #fs = GridFS(db)

    if not users_collection.find_one({"_id": user_id}):
        raise HTTPException(status_code=400, detail="El usuario no existe")

    conversations = conversations_collection.find({"personas": user_id})
    retrieved_conversations = []
    for conversation in conversations:
        other_person = conversation["personas"][0] if conversation["personas"][1] == user_id else conversation["personas"][1]
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
