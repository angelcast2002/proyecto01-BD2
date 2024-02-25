from typing import Union

import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile
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
@app.post("/users/")
async def create_user(user: User):
    client = mm.connect()
    db = client['ProyectoDB2']
    users_collection = db.usuarios
    #fs = GridFS(db)
    # Verificar si el usuario ya existe
    if users_collection.find_one({"_id": user.id}):
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Guardar la imagen en GridFS
    #profile_pic_id = fs.put(profile_pic.file, filename=profile_pic.filename)


    # Hashear la contraseña antes de almacenarla
    hashed_password = hashpw(user.password.encode('utf-8'), gensalt())

    # Insertar el nuevo usuario en la base de datos
    user_data = user.dict()
    user_data["birthdate"] = datetime.strptime(user_data["birthdate"], "%Y-%m-%d")
    user_data['password'] = hashed_password.decode('utf-8')
    #user_data['profilepic'] = profile_pic_id
    user_data['_id'] = user_data.pop('id')

    inserted_user = users_collection.insert_one(user_data)
    mm.disconnect(client)


    #Return status code 200 and message: "User created"
    return {"status": 200, "message": "User created"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)