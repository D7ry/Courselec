"""
Source UCLA course website and dumps all courses into a nosql json file to be uploaded to mongodb.
"""
import requests
from bs4 import BeautifulSoup

CATALOGUE_SITE:str = "https://catalog.registrar.ucla.edu/"

def main():
    ret:dict = {"catagories": []}
    response = requests.get(CATALOGUE_SITE)
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.reason}")
        raise Exception("Error")
    soup = BeautifulSoup(response.text, "html.parser")
    
    catagory_blocks = soup.find_all("li", {"class" : "css-1ym8evj-Tile--STileItem-Tile--STile e1mix0ja3"})
    
    for catagory_block in catagory_blocks:
        catagory_title = catagory_block.find("h4").text
        print(f"Indexing {catagory_title}")
    
    pass


if __name__ == "__main__":
    main()