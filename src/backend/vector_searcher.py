"""
Perform vectorized search of a couse in a database of courses.
"""
# workaround python's antihuman import system
import sys
filepath = __file__
parent_dir = "/".join(filepath.split("/")[:-3])
sys.path.append(parent_dir)

from mongodb_utils import get_mongodb_client
from db.embedding_generator import EmbeddingGenerator
    

class VectorSearcher:
    """
    Perform a vectorized search on the database, returning k-nearest neighbors.
    Collection must have a field called "plot_embedding" that contains the embedding of the course.
    """
    def __init__(self, db_uri:str, db_name:str, collection_name:str):
        """
        db name corresponds to school, collection_name corresponds to semester
        """
        self.mongo_client = get_mongodb_client(db_uri)
        if self.mongo_client is None:
            raise Exception("Failed to connect to MongoDB Atlas")
            return
        # Get the database and collection
        self.db = self.mongo_client[db_name]
        self.collection = self.db[collection_name]
        
    def match(self, search_prompt:str, num_return:int) -> list[dict]:
        """
        Perform a vectorized search of a course in the database.
        search_prompt: the prompt to search for, in natural language or keywords.
        """
        QUERY_INSTRUCTION:str = "Represent this sentence for searching relevant passages: " # instruction for query

        aggregate_scheme = \
        [
            {
                "$search": {
                    "index": "courses_embedding_index", 
                    "knnBeta": {
                    "vector": EmbeddingGenerator.get_singleton().text_to_embedding(QUERY_INSTRUCTION + search_prompt),
                    "path": "plot_embedding",
                    "k": num_return * 5
                    }
                }
            },
            {
                "$limit": num_return
            },
            {
                 "$project": {"_id":0, "plot_embedding":0}
            }
        ]
        results = self.collection.aggregate(aggregate_scheme)
        return list(results)