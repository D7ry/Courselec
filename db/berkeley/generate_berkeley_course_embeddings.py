import json
import threading
import copy
import time
import sys

# append the root directory to the path
sys.path.append("c:\\Users\\Ty\\repo\\Courselec\\")
from db.embedding_generator import EmbeddingGenerator

SRC = "db/berkeley/dump/all_courses.json"
DST = "db/berkeley/dump/all_courses_with_embedding.json"

lock = threading.Lock()
thread_limit = 10

embedding_generator = EmbeddingGenerator()

# read in src
with open(SRC, "r") as f:
    src = json.load(f)
    dst = {"catagories": []}
    catagories = src["catagories"]
    for catagory in catagories:
        dst_catagory = {"name": catagory["name"], "courses": []}
        courses = catagory["courses"]
        for course in courses:
            print(f"Processing {course['code']}")
            dst_course = copy.deepcopy(course)
            dst_course["plot_embedding"] = embedding_generator.json_to_embedding(course, {"description", "objectives", "outcomes", "title"})
            dst_catagory["courses"].append(dst_course)
        dst["catagories"].append(dst_catagory)

       
# write to dst
with open(DST, "w") as f:
    json.dump(dst, f, indent=4)