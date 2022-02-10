import os
import re
import time

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
    os.makedirs("data",existing=True)
    for page_nb,page in enumerate(pages):
        with open(f"data/pages/{page_nb}.html", "wb") as f_out:
            
        

def main():
    pages = get_page()
    print(pages)
    
if __name__ == '__main__':
    main()


