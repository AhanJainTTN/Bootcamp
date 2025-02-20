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
import re
from typing import Dict, List

# Constants
PAGE_LIMIT = 7
BASE_URL = "https://fermosaplants.com/"
COLLECTIONS_URL = "https://fermosaplants.com/collections/sansevieria?page={}"
curr_count = 1


# \d\.[\s ]?([\w]*[\s ]?)*
# \d+\.[\s ]?([A-Za-z]*[\s ]?)*
# \d+\.[\s ]?([A-Za-z]*[\s ]?)*.*
# \d+\.[  ]?([A-Za-z]*[\s ]?)*.*
# \d+\.[  ]*[A-Za-z]+([  ]*[A-Za-z]*)*
# \d+\.[  ]*[A-Za-z]+([  ]*[A-Za-z]*)*
# \d+\.[  ]*[A-Za-z]+([  ]*[A-Za-z]*)*
# \d+\.[ \\u00A0 ]*[A-Za-z]+([  \\u00A0]*[A-Za-z]*)*
# \d+\.[ ]*[\w]+[ ]*(?!\d)[\w]*
# \d+\.[  ]*[\w]+([  ]*(?!\d)[\w]*)*
# Combo Names: \d+\.[  ]*[\w]+(?!\.)([  ]*(?!\d)[\w]*)*
# Scientific Names v2: Scientific[ ]Name[-][  ]*[\w'"]+([  ]*[\w'"]*)*
# (?:Scientific[ ]Name[-][  ]*)[\w'"]+([  ]*[\w'"]*)*


def build_dataframe(plant_data: List[Dict[str, str]]):
    """Takes in plant data and builds a dataframe."""
    pass


def extract_combo_names(product_link):
    """Takes a product link of a combo and returns all the names in the combo."""
    source = requests.get(product_link).text
    soup = BeautifulSoup(source, "lxml")

    product_details = soup.find("div", class_="tab-pd-details")
    product_desc = product_details.find("div", class_="product-desc").text
    regex = re.compile(r"\d+\.[  ]*[\w]+(?!\.)([  ]*(?!\d)[\w]*)*")
    matches = [
        match.group().split(".")[1].strip().title()
        for match in regex.finditer(product_desc)
    ]
    return matches


def extract_scientific_name(product_link):
    """Takes a product link of a combo and returns the scientific name of the plant."""
    pass


def extract_common_name(product_card):
    """Takes the source html and extracts the common name of the plant."""
    return product_card.find("h4", class_="title-product").text.strip()


def extract_url(product_card):
    """Takes the source html and extracts the url of the product page."""
    product_title = product_card.find("h4", class_="title-product")
    product_link = product_title.find("a")["href"]

    return urljoin(BASE_URL, product_link)


def extract_price(product_card):
    """Takes the source html and extracts the price of the plant."""
    return product_card.find("p", class_="price-product").text.strip()


def scrape_page_grid(page_number: int) -> List[Dict[str, str]]:
    """Scrapes a single page and returns a list of product details."""
    request_url = COLLECTIONS_URL.format(page_number)
    source = requests.get(request_url).text
    soup = BeautifulSoup(source, "lxml")

    page_data = list()
    for product_card in soup.find_all("div", class_="product-item-v5"):
        plant_url = extract_url(product_card)
        plant_common_name = extract_common_name(product_card)
        plant_price = extract_price(product_card)
        plant_scientific_name = plant_common_name
        plant_common_names = []

        if "combo" in plant_common_name.lower():
            plant_scientific_name = extract_scientific_name(plant_url)
            plant_combo_names = extract_combo_names(plant_url)

        source = requests.get(product_link).text
        soup = BeautifulSoup(source, "lxml")

        product_details = soup.find("div", class_="tab-pd-details")
        product_desc = product_details.find("div", class_="product-desc").text
        # product_details = soup.find("div", class_="tab-pd-details")
        # product_desc = product_details.find("div", class_="product-desc").text

        if combo:
            # print("Scientific Name (Combo - Default): Sansevieria")
            # global curr_count
            # print(f"Combo {curr_count}, Page: {page_number}: {product_title}\n")
            # curr_count += 1
            # get_names(product_link)
            pass
        else:
            print(f"Normal Name: {product_title}")
            try:
                regex = re.compile(r"""Sansevieria[  ]*[\w'"]+([  ]*[\w'"]*)*""")
                scientific_name = regex.search(product_desc)
                print(f"Scientific Name: {scientific_name.group()}")
            except AttributeError:
                print(f"Scientific Name (Default): Sansevieria")

        extracted_data["Combo"] = combo
        page_data.append(extracted_data)

    # print(f"Finished scraping page {page_number}.")

    return page_data


def scrape_page_grid(page_number: int) -> List[Dict[str, str]]:
    """Scrapes a single page and returns a list of product details."""
    request_url = COLLECTIONS_URL.format(page_number)
    source = requests.get(request_url).text
    soup = BeautifulSoup(source, "lxml")

    page_data = list()
    for product_card in soup.find_all("div", class_="product-item-v5"):

        extracted_data = {
            "Title": "",
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

        source = requests.get(product_link).text
        soup = BeautifulSoup(source, "lxml")

        product_details = soup.find("div", class_="tab-pd-details")
        product_desc = product_details.find("div", class_="product-desc").text
        # print(product_desc + "\n")
        # try:
        #     regex = re.compile(
        #         r"""(?:Scientific[ ]Name[-][  ]*)[\w'"]+([  ]*[\w'"]*)*"""
        #     )
        #     scientific_name = regex.search(product_desc)
        #     print(
        #         f"Scientific Name: {scientific_name.group().split('Scientific Name-')[1].strip()}"
        #     )
        # except AttributeError:
        #     print(f"Scientific Name (Default): Sansevieria")

        # print("")

        product_price = product_price.text.strip()
        extracted_data["Price"] = product_price

        combo = "combo" in product_title.lower()

        # product_details = soup.find("div", class_="tab-pd-details")
        # product_desc = product_details.find("div", class_="product-desc").text

        if combo:
            # print("Scientific Name (Combo - Default): Sansevieria")
            # global curr_count
            # print(f"Combo {curr_count}, Page: {page_number}: {product_title}\n")
            # curr_count += 1
            # get_names(product_link)
            pass
        else:
            print(f"Normal Name: {product_title}")
            try:
                regex = re.compile(r"""Sansevieria[  ]*[\w'"]+([  ]*[\w'"]*)*""")
                scientific_name = regex.search(product_desc)
                print(f"Scientific Name: {scientific_name.group()}")
            except AttributeError:
                print(f"Scientific Name (Default): Sansevieria")

        extracted_data["Combo"] = combo
        page_data.append(extracted_data)

    # print(f"Finished scraping page {page_number}.")

    return page_data


def process_grid() -> List[Dict[str, str]]:
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
    # get_names(
    #     "https://fermosaplants.com/collections/sansevieria/products/sansevieria-combo-offer-of-6"
    # )
    scraped_data = process_pages()

    # csv_path = "/home/ahan/Documents/Bootcamp/Week_03_Python_for_Development/Day_02_Regular_Expression_and_Text_Processing/Exercises/ex_02_fermosa_scraper/files/results.csv"
    # dump_to_csv(csv_path, scraped_data)

    # excel_path = "/home/ahan/Documents/Bootcamp/Week_03_Python_for_Development/Day_02_Regular_Expression_and_Text_Processing/Exercises/ex_02_fermosa_scraper/files/results.xlsx"
    # dump_to_excel(excel_path, scraped_data)


if __name__ == "__main__":
    main()
