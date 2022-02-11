import os
import re
import time
from unittest import result

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



def get_page(count=1):
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    pages = []
    
    for page_nb in range(1, count+1):
        page_url = f"https://www.logic-immo.com/location-immobilier-roubaix-59100,26345_2/options/groupprptypesids=1,2,6,7,12/page={page_nb}"
        driver.get(page_url)
        time.sleep(12)
        pages.append(driver.page_source.encode('utf-8'))
        
    return pages


def save_page(pages):
    os.makedirs("data", exist_ok=True)
    for page_nb,page in enumerate(pages):
        with open(f"data/page_{page_nb}.html", "wb") as f_out:
            f_out.write(page)
            
        
def parse_pages():
    page_paths = os.listdir("data")
    results = pd.DataFrame()
    for page_path in page_paths:   
        with open("data/" + page_path, "rb") as f_in:
            page = f_in.read().decode('utf-8')
            result = parse_page(page)
            results = results.append(result)
            
    return results


def parse_page(page):
    """Parses data from a HTML page and return it as a dataframe
    The parsed data for each property advertisement is :
    - loyer (€) (rent)
    - type
    - surface (m²) (area)
    - nb_pieces (room number)
    - emplacement (location)
    - description
    Args:
        page (bytes): utf-8 encoded HTML page
    Returns:
        pd.DataFrame: Parsed data
    """
    soup = BeautifulSoup(page, "html.parser")
    result = pd.DataFrame()

    result["loyer (€)"] = [
        clean_price(tag) for tag in soup.find_all(attrs={"class": "announceDtlPrice"})
    ]
    result["type"] = [
        clean_type(tag) for tag in soup.find_all(attrs={"class": "announceDtlInfosPropertyType"})
    ]
    result["surface (m²)"] = [
        clean_surface(tag)
        for tag in soup.find_all(attrs={"class": "announceDtlInfos announceDtlInfosArea"})
    ]
    result["nb_pieces"] = [
        clean_rooms(tag)
        for tag in soup.find_all(attrs={"class": "announceDtlInfos announceDtlInfosNbRooms"})
    ]
    result["emplacement"] = [
        clean_postal_code(tag) for tag in soup.find_all(attrs={"class": "announcePropertyLocation"})
    ]
    result["description"] = [
        tag.text.strip() for tag in soup.find_all(attrs={"class": "announceDtlDescription"})
    ]

    return result
            
            
def clean_price(tag):
    text = tag.text.strip()
    price = int(text.replace("€", "").replace(" ", ""))
    return price


def clean_type(tag):
    text = tag.text.strip()
    return text.replace("Location ", "")


def clean_surface(tag):
    text = tag.text.strip()
    return int(text.replace("m²", ""))


def clean_rooms(tag):
    text = tag.text.strip()
    rooms = int(text.replace("p.", "").replace(" ", ""))
    return rooms


def clean_postal_code(tag):
    text = tag.text.strip()
    match = re.match(".*\(([0-9]+)\).*", text)
    return match.groups()[0]

def main():
    pages = get_page(count=3)
    # save_page(pages)
    print(pages)

    
if __name__ == '__main__':
    main()


