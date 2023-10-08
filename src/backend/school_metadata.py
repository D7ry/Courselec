from mongodb_utils import get_mongodb_client
DB_URI:str = os.environ.get("MONGODB_URI")
DB_NAME:str = "SCHOOL_METADATA"
COLLECTION_NAME:str  = "SCHOOLS"

def get_all_schools_metadata() -> 'list[dict]':
    """
    Returns a list of all school metadata.
    """
    db_client = get_mongodb_client(DB_URI)
    if db_client is None:
        raise Exception("Failed to connect to MongoDB")
    db = db_client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return list(collection.find({}))


if __name__ == "__main__":
    print(get_all_schools_metadata())