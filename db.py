from pymongo import MongoClient
from pymongo.server_api import ServerApi

class DB:
    def __init__(self):
        # MongoDB connection
        connection_uri = "mongodb+srv://username:password@cluster0.wertr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(connection_uri, server_api=ServerApi('1'))
        self.db = client.dsml

        # Ping MongoDB to check connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as ex:
            print(f"Could not connect to MongoDB: {ex}")
        
db=DB().db