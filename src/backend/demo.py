from course_advisor import CourseAdvisor

# a demo doing query on berkeley database
if __name__ == "__main__":
    DB_URI:str = os.environ.get("MONGODB_URI")
    DB_NAME:str = "BERKELEY_COURSES"
    COLLECTION_NAME:str  = "COURSES_SP_24"
    NUM_RETURN:int = 50 # number of courses to return
    
    advisor = CourseAdvisor(school_db_id=DB_NAME, academic_phase_collection_id=COLLECTION_NAME)
    
    while 1:
        print("Enter a search prompt: ")
        prompt = input()
        res = advisor.query(prompt)
        
        for one_course in res[0:20]:
            print(one_course['code'])
            print(one_course['title'])
            print(one_course['description']) if 'description' in one_course else None
            print(one_course['objectives']) if 'objectives' in one_course else None
            print(one_course['outcomes']) if 'outcomes' in one_course else None
            print()
        