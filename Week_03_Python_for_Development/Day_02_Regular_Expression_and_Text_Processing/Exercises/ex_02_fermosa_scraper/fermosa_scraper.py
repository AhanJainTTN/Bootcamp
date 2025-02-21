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
import re
from typing import Dict, List

# Constants
PAGE_LIMIT = 7
BASE_URL = "https://fermosaplants.com/"
COLLECTIONS_URL = "https://fermosaplants.com/collections/sansevieria?page={}"

# Combo Names v1: \d+\.[  ]*[\w]+(?!\.)([  ]*(?!\d)[\w]*)*
# Combo Names v2 (https://regex101.com/r/gMwsUi/4): \d+\.[  ]*(?!\d)(?!Including shipping)([\w](?!ncluding shipping))+(?!\.)([  ]*(?!\d)(?!including shipping)([\w](?!ncluding shipping))*(?!\.))*
# Scientific Names v1: Scientific[ ]Name[-][  ]*[\w'"]+([  ]*[\w'"]*)*
# Scientific Names v2: (?<=Scientific[ ]Name[-])|Sansevieria|Moonshine)[  ]*[\w'"-]+([  ]*[\w'"-]*)*|Black Gold Compacta|S. Dragon Scales


def build_dataframe(plant_data: List[Dict[str, str]]):
    """Takes in plant data and builds a dataframe."""
    pass


def cook_soup(request_url: str):
    """Takes a request URL and returns a BeautifulSoup object."""
    source = requests.get(request_url).text
    return BeautifulSoup(source, "lxml")


def extract_combo_names(product_desc):
    """Takes a product link of a combo and returns all the names in the combo."""
    regex = re.compile(
        r"""\d+\.[  ]*(?!\d)(?!Including shipping)([\w](?!ncluding shipping))+(?!\.)([  ]*(?!\d)(?!including shipping)([\w](?!ncluding shipping))*(?!\.))*"""
    )
    matches = [
        match.group().split(".")[1].strip().title()
        for match in regex.finditer(product_desc)
    ]
    return matches


def extract_scientific_name(product_desc):
    """Takes a product link of a plant and returns the scientific name of the plant."""
    regex = re.compile(
        r"""((?<=Scientific[ ]Name[-])|Sansevieria|Moonshine)[  ]*[\w'"-]+([  ]*[\w'"-]*)*|Black Gold Compacta|S. Dragon Scales""",
        re.IGNORECASE,
    )
    match = regex.search(product_desc)
    if not match:
        return "Sansevieria (Default)"

    return match.group().title().strip().rstrip("-")


def extract_common_name(product_card):
    """Takes the product card html and extracts the common name of the plant."""
    return product_card.find("h4", class_="title-product").text.title().strip()


def extract_url(product_card):
    """Takes the product card html and extracts the url of the product page."""
    product_title = product_card.find("h4", class_="title-product")
    product_link = product_title.find("a")["href"]

    return urljoin(BASE_URL, product_link)


def extract_price(product_card):
    """Takes the product card html and extracts the price of the plant."""
    return (
        product_card.find("p", class_="price-product")
        .find("span", class_="price")
        .text.strip()
    )


def scrape_page_grid(page_number: int) -> List[Dict[str, str]]:
    """Scrapes a single page and returns a list of product details."""
    request_url = COLLECTIONS_URL.format(page_number)
    grid_soup = cook_soup(request_url)

    page_data = list()
    for product_card in grid_soup.find_all("div", class_="product-item-v5"):

        plant_url = extract_url(product_card)
        plant_common_name = extract_common_name(product_card)
        plant_price = extract_price(product_card)

        product_soup = cook_soup(plant_url)

        product_desc = (
            product_soup.find("div", class_="tab-pd-details")
            .find("div", class_="product-desc")
            .text
        )

        plant_scientific_name = (
            "Sansevieria (Combo)"
            if "combo" in plant_common_name.lower()
            else extract_scientific_name(product_desc)
        )

        plant_combo_names = (
            extract_combo_names(product_desc)
            if "combo" in plant_common_name.lower()
            else []
        )

        extracted_data = {
            "Page": page_number,
            "Product Listing": plant_common_name,
            "Scientific Name": plant_scientific_name,
            "Price": plant_price,
            "URL": plant_url,
            "Combo Names": plant_combo_names,
            "Units": len(plant_combo_names) if plant_combo_names else 1,
        }

        page_data.append(extracted_data)

    print(f"Finished scraping page {page_number}.")
    return page_data


def process_grid() -> List[Dict[str, str]]:
    """Scrapes multiple pages and returns combined product data."""
    scraped_data = list()
    for curr_page in range(1, PAGE_LIMIT + 1):
        page_data = scrape_page_grid(curr_page)
        scraped_data.extend(page_data)

    return scraped_data


def dump_to_excel(excel_path: str, plant_data: List[Dict[str, str]]) -> None:
    """Writes scraped data to an Excel file."""
    df_main = pd.DataFrame(plant_data)
    max_columns = max(len(row) for row in df_main["Combo Names"])
    column_headers = [f"Plant {i + 1}" for i in range(max_columns)]

    df_combo = pd.DataFrame(
        df_main["Combo Names"].tolist(), columns=column_headers
    ).fillna("N/A")
    df_combined = df_main.join(df_combo).drop(labels="Combo Names", axis=1)

    df_combined.to_excel(excel_path, index=False)
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

    scraped_data = process_grid()

    csv_path = "files/results.csv"
    dump_to_csv(csv_path, scraped_data)

    excel_path = "files/results.xlsx"
    dump_to_excel(excel_path, scraped_data)


if __name__ == "__main__":
    main()
