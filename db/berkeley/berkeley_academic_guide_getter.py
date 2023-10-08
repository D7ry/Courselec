"""
Returns a list of all the courses in the Berkeley Academic Guide.
"""
import os
import requests
import json
import threading
from bs4 import BeautifulSoup


ACADEMIC_GUIDE_URL = "https://guide.berkeley.edu/courses/"
GLOBAL_LOCK = threading.Lock()

def get_one_course(course_block) -> dict:
    """
    Returns a dictionary containing information about a course.
    """
    try:
        ret:dict = {
            "code": None,
            "title": None,
            "hours": None,
            "term": None,
            "description": None,
            "objectives": None,
            "outcomes": None,
        }
        code = course_block.find("span", {"class" : "code"}).text
        code = code.replace("\u00a0", " ")
        ret["code"] = code
        ret["title"] = course_block.find("span", {"class" : "title"}).text
        ret['hours'] = course_block.find("span", {"class" : "hours"}).text
        
        term_and_description = course_block.find("p", {"class" : "courseblockdesc"})
        # term is the string before line break
        term_and_description = term_and_description.text.split("\n")
        term = term_and_description[0]
        description = term_and_description[1]
        
        if "2024" not in term:
            return None
        
        ret["term"] = term
        ret["description"] = description
        # TODO: add objectives and outcomes, hours, requirements, Grading options, Instrctor
        
        details_divs = course_block.find_all("div", {"class" : "course-section"})
        objective_outcome_div = None
        hours_format_div = None
        additional_details_div = None
        rules_reqs_div = None

        for detail_div in details_divs:
            div_text = detail_div.find("p", {"class" : "course-heading"}).text
            if "Objectives & Outcomes" in div_text:
                objective_outcome_div = detail_div
            elif "Hours & Format" in div_text:
                hours_format_div = detail_div
            elif "Additional Details" in div_text:
                additional_details_div = detail_div
            elif "Rules & Requirements" in div_text:
                rules_reqs_div = detail_div
        
        # populate objective and outcome
        if objective_outcome_div is not None:
            objective_outcome_paragraphs = objective_outcome_div.find_all("p")
            objective_p = objective_outcome_paragraphs[1] # first paragraph
            outcome_p = objective_outcome_paragraphs[2] # second paragraph 
            ret["objectives"] = objective_p.text
            ret["outcomes"] = outcome_p.text
        
        requirements = []
        # populate requirements
        if rules_reqs_div is not None:
            prerequisites_p = None
            for p in rules_reqs_div.find_all("p"):
                p_title = p.find("strong")
                if p_title.text == "Prerequisites:":
                    prerequisites_p = p
                    break
            if prerequisites_p is not None:
                reqs = prerequisites_p.find_all("a", {"class" : "bubblelink code"})
                for req in reqs:
                    requirements.append(req.text)
                
                
        return ret
    except Exception as e:
        return None


def get_one_catagory(url:str) -> dict:
    """
    Returns a list of all the courses in a catagory.
    {
        "courses": [
            {
                ...
            }
        ]
    }
    """
    ret:dict = {"courses": []}
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.reason}")
        raise Exception("Error")
    soup = BeautifulSoup(response.text, "html.parser")
    all_course_blocks = soup.find_all("div", {"class" : "courseblock"})
    for course_block in all_course_blocks:
        course = get_one_course(course_block)
        if course is not None:
            ret["courses"].append(course)
        
    return ret

def get_catagory_threadfunc(catagory_href, r_dict):
    catagory_location = catagory_href["href"]
    catagory_name = catagory_href.text
    catagory_site = "https://guide.berkeley.edu" + catagory_location
    try:
        catagory = get_one_catagory(catagory_site)
    except Exception as e:
        print(f"Error: {e}")
        return
    print(f"Catagory {catagory_name} done")
    catagory["name"] = catagory_name # Add catagory name to the catagory
    GLOBAL_LOCK.acquire()
    r_dict["catagories"].append(catagory)
    GLOBAL_LOCK.release()
    
def get_all_courses(url:str=ACADEMIC_GUIDE_URL) -> dict:
    """
    Returns a list of all the courses in the Berkeley Academic Guide.
    Return demo:
    {   
        "catagories": [
            {
                "name": "AERO ENG",
                "courses":
                [

                ]
            }
        ]
    }
    """
    ret:dict = {"catagories": []}
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.reason}")
        raise Exception("Error")
    soup = BeautifulSoup(response.text, "html.parser")

    indexes = soup.find("div", {"id" : "atozindex"})
    hrefs = indexes.find_all("a", href=True)
    
    threads = []
    
    for href in hrefs:
        t = threading.Thread(target=get_catagory_threadfunc, args=(href, ret))
        t.start()
        threads.append(t)
        
    for t in threads:
        t.join()
            
    return ret


def main():
    all_courses = get_all_courses()
    outfile_name = "out/all_courses.json"
    # Get the absolute path of the current file
    current_file_path = os.path.abspath(__file__)
    # Get the directory of the current file
    current_dir_path = os.path.dirname(current_file_path)
    # Get the absolute path of the output file
    output_file_path = os.path.join(current_dir_path, outfile_name)
    # Open the output file
    with open(output_file_path, "w") as outfile:
        # Write the JSON data to the output file
        json.dump(all_courses, outfile)
    


        
if __name__ == "__main__":
    main()