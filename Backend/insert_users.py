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
    ## Solo fechas del 80 al 80 y del 2008 al 2010. 3 por cada año
    "1980-01-01", "1980-02-02", "1980-03-03", "2008-01-01", "2008-02-02", "2008-03-03",
    "1981-01-01", "1981-02-02", "1981-03-03", "2009-01-01", "2009-02-02", "2009-03-03",
    "1982-01-01", "1982-02-02", "1982-03-03", "2010-01-01", "2010-02-02", "2010-03-03",
    "1983-01-01", "1983-02-02", "1983-03-03", "1984-01-01", "1984-02-02", "1984-03-03",
    "1985-01-01", "1985-02-02", "1985-03-03", "1986-01-01", "1986-02-02", "1986-03-03",
    "1987-01-01", "1987-02-02", "1987-03-03", "1988-01-01", "1988-02-02", "1988-03-03",
    "1989-01-01", "1989-02-02", "1989-03-03", "1990-01-01", "1990-02-02", "1990-03-03"
    
]
generos = [False, False, True, True, True, False, True, False, True, False, True, False, True]
emails = ["gmail.com", "outlook.com", "icloud.com", "yahoo.com", "hotmail.com", "live.com", "aol.com", "protonmail.com", "zoho.com", "gmx.com", "uvg.edu.gt", "ufm.gt"]
contrasenas = ["53h7f9gd", "7r3j5b2k", "9p1s6t8m", "4a2x8c7v", "6z9w4q3e", "1y8h5n2u", "3i5o7l6p", "8f4g2k9d", "2r5v6m3n", "9s7w4q3e", "5b4x3w2d", "2s4d6g8h", "7r5e2w8q", "3q7e9z2x", "8c5v3b1n", "1m8n2b4v", "6c3x9v7b", "4l6o9p1i", "9q8w7e2r", "5p2o4i6u"]


cont = 0
# Insertar datos aleatorios
for _ in range(10000):  # Insertar 100 usuarios
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    email = f"{nombre.lower()[1]}.{apellido.lower()}.{random.choice([55, 66, 77, 88, ''])}@{random.choice(emails)}"
    fecha_nacimiento = random.choice(fechas_nacimiento)
    genero = random.choice(generos)
    contrasena = random.choice(contrasenas)
    hashed_password = hashpw(contrasena.encode('utf-8'), gensalt())
    

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
            "profilepic": ObjectId('65e212709342dd97c5fda05d'),  # ObjectId de la imagen en GridFS
            "gender": genero
        }))


print("Datos insertados con éxito.")
