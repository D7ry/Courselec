import os
from vector_searcher import VectorSearcher
from llm_ai import LLM_OpenAI
from mongodb_utils import get_mongodb_client
class CourseAdvisor:
    """
    Gives single-course or multi-course(TBD) recommendations based on NLP inputs from user.
    """
        
    class AdvisorResult:
        def __init__(self, courses:'list[dict]'):
            self.courses = courses
            # each course should have a "reason" field

    def __init__(self, school_db_id:str, academic_phase_collection_id:str):
        """
        Initialize the CourseAdvisor.
        """
        db_uri = os.environ.get("MONGODB_URI")
        self.__vector_searcher = VectorSearcher(db_uri=db_uri, db_name=school_db_id, collection_name=academic_phase_collection_id)
        self.__llm = LLM_OpenAI()
        self.__llm_cache_collection = get_mongodb_client(db_uri)["LLM_CACHE"]["OPENAI"]
        pass
    
    def query(self, prompt:str) -> AdvisorResult:
        """
        Returns an AdvisorResult that matches the prompt.
        school_db_name: name of the school's database to query from.
        academic_period: the academic period to search, corresponds to collection id in the db.
        prompt: the natural langauge prompt.
        """
        prompt = prompt.lower()
        print("User prompt: " + prompt)
        
        nlp_generated_prompt:str = None
        
        llm_cache = self.__llm_cache_collection.find_one({"prompt": prompt})
        
        if llm_cache is not None:
            nlp_generated_prompt = llm_cache["result"]
            print("NLP generated prompt from cache: " + nlp_generated_prompt)
        else:
        # run prompt through NLP model to generate a better prompt
            nlp_generated_prompt = self.__llm.query(
                """
                I want to learn about {}, give me 10 relevant topics, subjects and skills related to it, separated by commas. DO NOT say anything else.
                """.format(prompt)   
            )
            self.__llm_cache_collection.insert_one({"prompt": prompt, "result": nlp_generated_prompt})
            
        print("NLP generated prompt: " + nlp_generated_prompt)
        
        print("Searching database...")
        courses = self.__vector_searcher.match(f"{prompt}, {nlp_generated_prompt}", 50) # get 50 nearest results
        
        return courses

        # run not_filter pass
        
        # run LLM pass
        
        
        