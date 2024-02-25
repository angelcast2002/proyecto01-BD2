from pymongo import MongoClient


# Connection to MongoDB
def connect():
    connection_string = "mongodb+srv://azu21242:TopoMorado2@aleazurdia.ueyomqq.mongodb.net/?retryWrites=true&w=majority&appName=aleazurdia"
    client = MongoClient(connection_string)
    try:
        client.admin.command('ping')
        print('MongoDB connection: Success')
    except Exception as e:
        print(f'MongoDB connection: Failed {e}')
    return client

def disconnect(client):
    client.close()
