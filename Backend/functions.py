import pymongo
from pymongo import MongoClient
from gridfs import GridFS
from PIL import Image
import io

# Conectar a MongoDB
client = MongoClient("mongodb+srv://azu21242:TopoMorado2@aleazurdia.ueyomqq.mongodb.net/?retryWrites=true&w=majority&appName=aleazurdia")
db = client.ProyectoDB2

# Acceder a la colección GridFS
fs = GridFS(db)


from pymongo import MongoClient
import gridfs
from datetime import datetime
import uuid

# Conexión a MongoDB
client = MongoClient("mongodb+srv://azu21242:TopoMorado2@aleazurdia.ueyomqq.mongodb.net/?retryWrites=true&w=majority&appName=aleazurdia")
db = client.ProyectoDB2
fs = gridfs.GridFS(db)

# Función para añadir un usuario
def anadir_usuario(correo, nombre, apellido, birthdate, password, profile_pic_path):
    usuarios_col = db['usuarios']  # Accede a la colección directamente
    with open(profile_pic_path, 'rb') as profile_pic:
        profile_pic_id = fs.put(profile_pic, filename=correo)
    usuario = {
        "_id": correo,
        "nombre": nombre,
        "apellido": apellido,
        "birthdate": birthdate,
        "password": password,  # Considerar hash de contraseña para seguridad
        "profilepic": profile_pic_id
    }
    return usuarios_col.insert_one(usuario).inserted_id

# Función para crear una conversación entre dos usuarios
def crear_conversacion(id_usuario1, id_usuario2):
    conversaciones_col = db['conversacion']  # Accede a la colección directamente
    conversacion = {
        "_id": str(uuid.uuid4()),
        "arr_mensajes": [],
        "personas": [id_usuario1, id_usuario2]
    }
    return conversaciones_col.insert_one(conversacion).inserted_id

# Función para añadir un mensaje a una conversación
def anadir_mensaje(id_conversacion, emisor, receptor, mensaje, es_archivo=False):
    conversaciones_col = db['conversacion']  # Accede a la colección directamente
    if es_archivo:
        with open(mensaje, 'rb') as archivo:
            mensaje_id = fs.put(archivo, filename=f"msg_{datetime.now().timestamp()}")
            mensaje = str(mensaje_id)
    
    mensaje_doc = {
        "emisor": emisor,
        "receptor": receptor,
        "id_mensaje": str(uuid.uuid4()),
        "mensaje": mensaje,
        "fechahora": datetime.now()
    }
    return conversaciones_col.update_one({"_id": id_conversacion}, {"$push": {"arr_mensajes": mensaje_doc}})

from bson.objectid import ObjectId
from IPython.display import display

# Conexión a MongoDB

# Función para recuperar la información del usuario y su foto de perfil
# Función para recuperar la información del usuario y su foto de perfil
def recuperar_usuario_y_foto(correo):
    # Asegúrate de que aquí usas el nombre correcto de la colección
    usuario = db['usuarios'].find_one({"_id": correo})  # Asegúrate de que 'usuarios' es el nombre correcto de la colección
    if usuario:
        print(f"Nombre: {usuario['nombre']}")
        print(f"Apellido: {usuario['apellido']}")
        print(f"Correo: {usuario['_id']}")  # Usar '_id' para ser consistente con el campo usado en la inserción
        print(f"Fecha de nacimiento: {usuario['birthdate']}")

        # Recuperar y mostrar la foto de perfil
        profile_pic = fs.get(usuario['profilepic']).read()
        image = Image.open(io.BytesIO(profile_pic))
        image.show()  # Cambiado a show() para compatibilidad fuera de Jupyter
    else:
        print("Usuario no encontrado.")


if __name__ == "__main__":
    # Prueba de añadir usuario
    #anadir_usuario("prueba2@gmail.com", "Prueba", "Dos", "1999-11-11", "password", "foto.png")
    #recuperar_usuario_y_foto("prueba1@gmail.com")

    # Prueba de crear conversación
    crear_conversacion("prueba1@gmail.com", "prueba2@gmai.com")