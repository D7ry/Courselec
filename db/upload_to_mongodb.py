import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

DB_URI:str = os.environ.get("MONGODB_URI")
DB_NAME:str = "BERKELEY_COURSES"
COLLECTION_NAME:str  = "COURSES_SP_24"
JSON_PATH = "all_courses_with_embedding.json"

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
"""
Update MongoDB with data from Berkeley
"""
def insert_berkeley_data():
    client = get_mongodb_client(DB_URI)
    if client is None:
        return

    # Get the database and collection objects
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    collection.delete_many({})

    json_file = open('db/berkeley/dump/all_courses_with_embedding.json')
    json_str = json_file.read()
    json_data = json.loads(json_str)
    for catagory in json_data['catagories']:
        for course in catagory['courses']:
            collection.insert_one(course)
            print(course['code'])
        
if __name__ == "__main__":
    insert_berkeley_data()