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
nombres = ["Juan", "Carlos", "Pedro", "Luis", "José", "Manuel", "Jesús", "Javier", "Francisco", "Daniel", "Alejandro", "Miguel", "Rafael", "Fernando", "Sergio", "Arturo", "Eduardo", "Jorge", "Ricardo", "Emilio", "Antonio", "Roberto", "Guillermo", "Héctor", "Mauricio", "Rodrigo", "Humberto", "Armando", "Alberto", "Enrique", "Gustavo", "Adrián", "Oscar", "Salvador", "Víctor", "Ernesto", "Fernando", "Raúl", "Martín", "Alfredo", "Leonardo", "Eduardo", "Luis", "Ricardo", "Javier", "Héctor", "Miguel", "Roberto", "Francisco", "José", "Manuel", "Jesús", "Alejandro", "Daniel", "Guillermo", "Rafael", "Sergio", "Arturo", "Fernando", "Eduardo", "Jorge", "Ricardo", "Emilio", "Antonio", "Roberto", "Guillermo", "Héctor", "Mauricio", "Rodrigo", "Humberto", "Armando", "Alberto", "Enrique", "Gustavo", "Adrián", "Oscar", "Salvador", "Víctor", "Ernesto", "Fernando", "Raúl", "Martín", "Alfredo", "Leonardo", "Eduardo", "Luis", "Ricardo", "Javier", "Héctor", "Miguel", "Roberto", "Francisco", "José", "Manuel", "Jesús", "Alejandro", "Daniel", "Guillermo", "Rafael", "Sergio", "Arturo", "Fernando", "Eduardo", "Jorge", "Ricardo", "Emilio", "Antonio", "Roberto", "Guillermo", "Héctor", "Mauricio", "Rodrigo"]
apellidos = ["González", "Rodríguez", "Gómez", "Fernández", "López", "Díaz", "Martínez", "Pérez", "García", "Sánchez", "Romero", "Sosa", "Álvarez", "Torres", "Ruiz", "Ramírez", "Flores", "Acosta", "Benítez", "Medina", "Herrera", "Suárez", "Aguirre", "Jiménez", "Molina", "Ortiz", "Silva", "Gutiérrez", "Rojas", "Núñez", "Cabrera", "Chávez", "Vargas", "Mendoza", "Ramos", "Blanco", "Méndez", "Guerrero", "Suárez", "Aguirre", "Jiménez", "Molina", "Ortiz", "Silva", "Gutiérrez", "Rojas", "Núñez", "Cabrera", "Chávez", "Vargas", "Mendoza", "Ramos", "Blanco", "Méndez", "Guerrero", "Suárez", "Aguirre", "Jiménez", "Molina", "Ortiz", "Silva", "Gutiérrez", "Rojas", "Núñez", "Cabrera", "Chávez", "Vargas", "Mendoza", "Ramos", "Blanco", "Méndez", "Guerrero", "Suárez", "Aguirre", "Jiménez", "Molina", "Ortiz", "Silva", "Gutiérrez", "Rojas", "Núñez", "Cabrera", "Chávez", "Vargas", "Mendoza", "Ramos", "Blanco", "Méndez", "Guerrero", "Suárez", "Aguirre", "Jiménez", "Molina", "Ortiz", "Silva", "Gutiérrez", "Rojas", "Núñez", "Cabrera", "Chávez", "Vargas", "Mendoza", "Ramos", "Bladimir"]
fechas_nacimiento = [
    "1990-01-01", "1990-04-15", "1990-07-29", "1990-11-10", "1991-02-23", "1991-06-08", "1991-09-21", "1991-12-31", "1992-04-14", "1992-07-28",
    "1992-11-09", "1993-02-22", "1993-06-07", "1993-09-20", "1993-12-31", "1994-04-15", "1994-07-29", "1994-11-10", "1995-02-23", "1995-06-08",
    "1995-09-21", "1995-12-31", "1996-04-14", "1996-07-28", "1996-11-09", "1997-02-22", "1997-06-07", "1997-09-20", "1997-12-31", "1998-04-15",
    "1999-07-23", "1999-11-05", "2000-02-18", "2000-06-02", "2000-09-15", "2000-12-29", "2001-04-13", "2001-07-27", "2001-11-09", "2002-02-22",
    "2002-06-07", "2002-09-20", "2002-12-31", "2003-04-14", "2003-07-28", "2003-11-10", "2004-02-23", "2004-06-07", "2004-09-20", "2004-12-31",
    "2005-04-15", "2005-07-29", "2005-11-10", "2006-02-23", "2006-06-08", "2006-09-21", "2006-12-31", "2007-04-16", "2007-07-30", "2007-11-11"
]
generos = [False, False, True]
emails = ["gmail.com", "outlook.com", "icloud.com", "yahoo.com", "hotmail.com", "live.com"]
contrasenas = ["53h7f9gd", "7r3j5b2k", "9p1s6t8m", "4a2x8c7v", "6z9w4q3e", "1y8h5n2u", "3i5o7l6p", "8f4g2k9d", "2r5v6m3n", "9s7w4q3e", "5b4x3w2d", "2s4d6g8h", "7r5e2w8q", "3q7e9z2x", "8c5v3b1n", "1m8n2b4v", "6c3x9v7b", "4l6o9p1i", "9q8w7e2r", "5p2o4i6u"]

# Ruta a la imagen que quieres subir
ruta_imagen = r"C:\Users\pacay\Downloads\response.png"

cont = 0
# Insertar datos aleatorios
for _ in range(1000):  # Insertar 100 usuarios
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    email = f"{nombre.lower()[1]}{apellido.lower()}{random.choice([0, 1, 2, 3, 4, 5])}@{random.choice(emails)}"
    fecha_nacimiento = random.choice(fechas_nacimiento)
    genero = random.choice(generos)
    contrasena = random.choice(contrasenas)
    hashed_password = hashpw(contrasena.encode('utf-8'), gensalt())
    

    if usuarios_collection.find_one({"_id": email}):
        print("Usuario ya existe")
        continue
    else:
        # Leer la imagen desde la ruta especificada
        with open(ruta_imagen, 'rb') as f:
            # Subir la imagen a GridFS y obtener su ObjectId
            imagen_id = fs.put(f)

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
