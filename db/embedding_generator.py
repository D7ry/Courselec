from langchain.embeddings import HuggingFaceBgeEmbeddings

class EmbeddingGenerator:
    
    __singleton:'EmbeddingGenerator' = None
    
    @classmethod
    def get_singleton(cls) -> 'EmbeddingGenerator':
        if cls.__singleton is None:
            cls.__singleton = EmbeddingGenerator()
        return cls.__singleton
    
    """Generate embeddings for text and json"""
    def __init__(self):
        # set embedding model here
        self.model_name = "BAAI/bge-small-en"
        self.model_kwargs = {'device': 'cpu'}
        self.encode_kwargs = {'normalize_embeddings': False}
        self.hf = HuggingFaceBgeEmbeddings(
            model_name=self.model_name,
            model_kwargs=self.model_kwargs,
            encode_kwargs=self.encode_kwargs
        )

    def text_to_embedding(self, text:str) -> list[float]:
        """Return the embedding of the text"""
        return self.hf.embed_query(text)

    def json_to_embedding(self, json:dict, fields:set[str]) -> list[float]:
        """Return the embedding of the json"""
        text:str = ""
        for field in fields:
            if field in json and json[field] != "" and json[field] is not None:
                text += json[field] + "\n\n"
        return self.text_to_embedding(text)