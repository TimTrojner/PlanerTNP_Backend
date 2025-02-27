from pymongo import MongoClient

class DB:
    def __init__(self):
        # MongoDB connection
        # connection_uri = "mongodb+srv://rene:CJW79XEHTXIWD9dp@planertnp.hul1s.mongodb.net/?retryWrites=true&w=majority&appName=planerTNP"
        connection_uri = "mongodb://admin:password@mongodb:27017/dsml"



        # connection_uri = os.getenv('DATABASE_URL')
        client = MongoClient(connection_uri)
        self.db = client.dsml

        # Ping MongoDB to check connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as ex:
            print(f"Could not connect to MongoDB: {ex}")
        
db=DB().db