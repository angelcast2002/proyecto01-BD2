from bcrypt import gensalt, hashpw
import pymongo
import random
from datetime import datetime
from bson import ObjectId
import os
from gridfs import GridFS

# Conexión a la base de datos
client = pymongo.MongoClient("mongodb+srv://azu21242:TopoMorado2@aleazurdia.ueyomqq.mongodb.net/?retryWrites=true&w=majority&appName=aleazurdia")
db = client["ProyectoDB2"]
usuarios_collection = db.usuarios
fs = GridFS(db)  # Inicializar GridFS

# Arrays generados
nombres = ["Juan", "Ana", "María", "Pedro", "Luisa", "José", "Carlos", "Laura", "Miguel", "Sofía", "Lucía", "Jorge", "Elena", "Andrés", "Beatriz", "Diego", "Carmen", "Roberto", "Isabel", "Antonio"]
apellidos = ["García", "López", "Martínez", "Rodríguez", "González", "Fernández", "Pérez", "Sánchez", "Romero", "Díaz", "Torres", "Ruiz", "Hernández", "Dominguez", "Vázquez", "Jiménez", "Moreno", "Álvarez", "Gómez", "Navarro"]
fechas_nacimiento = ["1992-04-15", "1995-07-28", "1998-09-10", "2001-12-03", "1991-05-20", "1993-08-02", "1996-10-18", "1999-03-11", "2003-06-24", "1994-09-05", "1997-11-13", "2000-02-26", "2002-04-07", "2005-08-15", "2008-01-29", "2009-05-12", "2010-09-23", "2004-11-30", "2007-03-08", "2006-06-17"]
generos = [False, True]
emails = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com"]
contrasenas = ["53h7f9gd", "7r3j5b2k", "9p1s6t8m", "4a2x8c7v", "6z9w4q3e", "1y8h5n2u", "3i5o7l6p", "8f4g2k9d", "2r5v6m3n", "9s7w4q3e", "5b4x3w2d", "2s4d6g8h", "7r5e2w8q", "3q7e9z2x", "8c5v3b1n", "1m8n2b4v", "6c3x9v7b", "4l6o9p1i", "9q8w7e2r", "5p2o4i6u"]

# Ruta a la imagen que quieres subir
ruta_imagen = r"C:\Users\pacay\Downloads\response.png"

cont = 0
# Insertar datos aleatorios
for _ in range(1000):  # Insertar 100 usuarios
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    email = f"{nombre.lower()}.{apellido.lower()}@{random.choice(emails)}"
    fecha_nacimiento = random.choice(fechas_nacimiento)
    genero = random.choice(generos)
    contrasena = random.choice(contrasenas)
    hashed_password = hashpw(contrasena.encode('utf-8'), gensalt())
    
    # Leer la imagen desde la ruta especificada
    with open(ruta_imagen, 'rb') as f:
        # Subir la imagen a GridFS y obtener su ObjectId
        imagen_id = fs.put(f)
    if usuarios_collection.find_one({"_id": email}):
        print("Usuario ya existe")
        continue
    else:
        cont += 1

        # Insertar el documento en la colección
        print(usuarios_collection.insert_one({
            "_id": email,
            "password": hashed_password.decode('utf-8'),
            "nombre": nombre,
            "apellido": apellido,
            "birthdate": datetime.strptime(fecha_nacimiento, "%Y-%m-%d"),
            "profilepic": imagen_id,  # ObjectId de la imagen en GridFS
            "gender": genero
        }))


print("Datos insertados con éxito.")
