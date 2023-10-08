from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
def get_mongodb_client(uri:str) -> MongoClient:
    """Connect to MongoDB Atlas and return the client"""

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)
        return None
    return client