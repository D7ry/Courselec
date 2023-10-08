"""
Uploads all metadata.json in the folder hierarchy to MongoDB.
"""

import os
import json
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


DB_URI:str = os.environ.get("MONGODB_URI")
DB_NAME:str = "SCHOOL_METADATA"
COLLECTION_NAME:str  = "SCHOOLS"

def main():
    db_client = get_mongodb_client(DB_URI)
    if db_client is None:
        raise Exception("Failed to connect to MongoDB")
    db = db_client[DB_NAME]
    collection = db[COLLECTION_NAME]
    # iterate through all the folders in the directory
    for folder in os.listdir('db'):
        # check for metadata.json
        if os.path.isfile('db/' + folder + '/metadata.json'):
            # open metadata.json
            metadata_file = open('db/' + folder + '/metadata.json')
            # read metadata.json
            metadata_str = metadata_file.read()
            # convert metadata.json to json object
            metadata_json = json.loads(metadata_str)
            collection.insert_one(metadata_json)
            print(metadata_json['school_name'])
            

if __name__ == "__main__":
    main()