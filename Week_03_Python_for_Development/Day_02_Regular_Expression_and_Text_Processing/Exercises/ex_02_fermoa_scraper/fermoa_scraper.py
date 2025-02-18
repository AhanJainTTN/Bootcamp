"""
Fermoa Plant is an online portal from where one can order different types of sansevierias, either in combo or as individual: https://fermosaplants.com/collections/sansevieria 

This assignment is about scrapping the portal to prepare an Excel (not CSV) dataset. Go through all pages of items: “https://fermosaplants.com/collections/sansevieria?page=<number>”

Visit each item and download the following information in Excel.
* 1 Item in 1 row* 
Columns: <URL> <TYPE> <Price> <Number> <Verigated> <name1> <name2> <name3>……<nameN> 
URL: link of page 
Type: combo, clump, Leaf, plant, pub 
Price: Price in rupees
Number: number of plant in combo 
Name: Plant names (one plant name in one column)
"""

import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from typing import List, Dict

# Constants
PAGE_LIMIT = 7
BASE_URL = "https://fermosaplants.com/"
COLLECTIONS_URL = "https://fermosaplants.com/collections/sansevieria?page={}"


def scrape_page(page_number: int) -> List[Dict[str, str]]:
    """Scrapes a single page and returns a list of product details."""
    request_url = COLLECTIONS_URL.format(page_number)
    source = requests.get(request_url).text
    soup = BeautifulSoup(source, "lxml")

    page_data = list()
    for product_card in soup.find_all("div", class_="product-item-v5"):

        extracted_data = {
            "Name": "",
            "URL": "",
            "Price": "",
            "Combo": "",
        }

        product_title = product_card.find("h4", class_="title-product")
        product_link = product_title.find("a")["href"]
        product_price = product_card.find("p", class_="price-product")

        product_title = product_title.text.strip()
        extracted_data["Name"] = product_title

        product_link = urljoin(BASE_URL, product_link)
        extracted_data["URL"] = product_link

        product_price = product_price.text.strip()
        extracted_data["Price"] = product_price

        combo = "combo" in product_title.lower()
        extracted_data["Combo"] = combo

        page_data.append(extracted_data)

    print(f"Finished scraping page {page_number}.")

    return page_data


def process_pages() -> List[Dict[str, str]]:
    """Scrapes multiple pages and returns combined product data."""
    scraped_data = list()
    for curr_page in range(1, PAGE_LIMIT + 1):
        page_data = scrape_page(curr_page)
        scraped_data.extend(page_data)

    return scraped_data


def dump_to_excel(excel_path: str, data: List[Dict[str, str]]) -> None:
    """Writes scraped data to an Excel file."""
    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)
    print(f"Finished writing to {excel_path}")


def dump_to_csv(csv_path: str, data: List[Dict[str, str]]) -> None:
    """Writes scraped data to a CSV file."""
    with open(csv_path, "w", newline="") as csv_file:
        headers = data[0].keys() if data else []
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        print(f"Finished writing to {csv_path}.")


def main() -> None:
    """Entry point for the script."""
    scraped_data = process_pages()

    csv_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_03_Python_for_Development/Day_02_Regular_Expression_and_Text_Processing/Exercises/ex_02_fermoa_scraper/files/results.csv"
    dump_to_csv(csv_path, scraped_data)

    excel_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_03_Python_for_Development/Day_02_Regular_Expression_and_Text_Processing/Exercises/ex_02_fermoa_scraper/files/results.xlsx"
    dump_to_excel(excel_path, scraped_data)


if __name__ == "__main__":
    main()
