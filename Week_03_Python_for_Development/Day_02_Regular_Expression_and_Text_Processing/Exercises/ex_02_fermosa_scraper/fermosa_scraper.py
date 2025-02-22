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


class FermosaCollectionsScraper:
    """Class to extract data from Fermosa Plants website."""

    BASE_URL = "https://fermosaplants.com/"

    def __init__(self, collections_url: str, page_limit: int):
        # Constants
        self.PAGE_LIMIT = page_limit
        self.COLLECTIONS_URL = collections_url.rstrip("/") + "?page={}"

        # Precompiled regular expressions
        self.REGEX_SCIENTIFIC_NAME = re.compile(
            r"""((?<=Scientific[ ]Name[-])|Sansevieria|Moonshine)[  ]*[\w'"-]+([  ]*[\w'"-]*)*|Black Gold Compacta|S. Dragon Scales""",
            re.IGNORECASE,
        )
        self.REGEX_COMBO_NAMES = re.compile(
            r"""\d+\.[  ]*(?!\d)(?!Including shipping)([\w](?!ncluding shipping))+(?!\.)([  ]*(?!\d)(?!including shipping)([\w](?!ncluding shipping))*(?!\.))*""",
            re.IGNORECASE,
        )
        self.REGEX_VARIEGATED = re.compile(r"Variegate[d]?", re.IGNORECASE)
        self.REGEX_PLANT_TYPE = re.compile(r"Clump|Single[ ]*Leaf|Pup", re.IGNORECASE)
        self.listing_count = 1

    def scrape_plant_data(self) -> List[Dict[str, str]]:
        """Scrapes plant data from all pages."""
        self.listing_count = 1
        extracted_data = list()
        for url in self.extract_urls_from_all_pages():
            extracted_data.append(self.process_listing(url))
            self.listing_count += 1

        return extracted_data

    def extract_urls_from_all_pages(self) -> List[str]:
        """Extracts product URLs from all pages in the grid."""
        return [
            self.extract_url(product_card)
            for curr_page in range(1, self.PAGE_LIMIT + 1)
            for product_card in self.cook_soup(
                self.COLLECTIONS_URL.format(curr_page)
            ).find_all("div", class_="product-item-v5")
        ]

    def process_listing(self, listing_url: str) -> Dict[str, str]:
        """Takes in a listing URL and extracts Product Title, Price, Scientific Name, Units and Combo Names (if applicable)."""
        print(f"Processing listing {self.listing_count}...")
        product_soup = self.cook_soup(listing_url)
        if not product_soup:
            return self.handle_missing_details(listing_url)

        product_details = product_soup.find("div", class_="tab-pd-details")
        if not product_details:
            return self.handle_missing_details(listing_url)

        product_desc = product_details.find("div", class_="product-desc")
        if not product_desc:
            return self.handle_missing_details(listing_url)

        product_desc = product_desc.text
        plant_combo_names = self.extract_combo_names(product_desc)
        product_title = self.extract_product_title(product_soup)

        plant_type = self.extract_type(product_title)

        return {
            "S.No": self.listing_count,
            "Product Listing": self.extract_product_title(product_soup),
            "Scientific Name": (
                self.extract_scientific_name(product_desc)
                if not "combo" in product_title.lower()
                else "Sansevieria (Combo)"
            ),
            "Price": self.extract_price(product_soup),
            "URL": listing_url,
            "Variegated": plant_type["Variegated"],
            "Type": (
                plant_type["Type"] if not "combo" in product_title.lower() else "Combo"
            ),
            "Combo Names": plant_combo_names,
            "Units": len(plant_combo_names) if plant_combo_names else 1,
        }

    def extract_product_title(self, product_page: BeautifulSoup) -> str:
        """Extracts product listing title from product page."""
        product_title = product_page.find("h2", class_="product-title")
        return product_title.text.title() if product_title else "N/A"

    def extract_scientific_name(self, product_desc: str) -> str:
        """Extracts the scientific name of the plant from product description."""
        match = self.REGEX_SCIENTIFIC_NAME.search(product_desc)
        scientific_name = (
            match.group().title().strip().rstrip("-")
            if match
            else "Sansevieria (Default)"
        )

        return scientific_name

    def extract_price(self, product_page: BeautifulSoup) -> str:
        """Extracts product price prefixed with Rs. from product page."""
        product_price = product_page.find("ins", class_="enj-product-price")
        return product_price.text if product_price else "N/A"

    def extract_combo_names(self, product_desc: str) -> List[str]:
        """Extracts all the plant names in the combo from product description."""
        combo_names = list()
        for match in self.REGEX_COMBO_NAMES.finditer(product_desc):
            try:
                plant_name = match.group().split(".")[1].strip().title()
                combo_names.append(plant_name)
            except IndexError as e:
                combo_names.append("Name extraction error.")

        return combo_names

    def extract_type(self, product_title: str) -> Dict:
        """Classifies plant as variegated and determines its type."""
        is_variegated = bool(self.REGEX_VARIEGATED.search(product_title))
        match = self.REGEX_PLANT_TYPE.search(product_title)
        plant_type = match.group().title() if match else "Plant"

        return {"Variegated": is_variegated, "Type": plant_type}

    def extract_url(self, product_card: BeautifulSoup) -> str:
        """Extracts product listing URL."""
        product_title = product_card.find("h4", class_="title-product")
        product_link = (
            product_title.find("a").get("href", self.BASE_URL)
            if product_title
            else self.BASE_URL
        )
        return urljoin(self.BASE_URL, product_link)

    def cook_soup(self, request_url: str) -> BeautifulSoup:
        """Fetches a URL and returns a BeautifulSoup object."""
        try:
            response = requests.get(request_url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {request_url}: {e}")
            return None

    def handle_missing_details(
        self, listing_url: str, listing_count: int
    ) -> Dict[str, str]:
        """Handles missing details in the HTML response."""
        print(f"Missing product details: {listing_url}")
        return {
            "S.No": self.listing_count,
            "Product Listing": "N/A",
            "Scientific Name": "N/A",
            "Price": "N/A",
            "URL": listing_url,
            "Variegated": "N/A",
            "Type": "N/A",
            "Combo Names": [],
            "Units": "N/A",
        }

    @staticmethod
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

    @staticmethod
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
    collections_url = "https://fermosaplants.com/collections/sansevieria"
    pages = 7

    scraper = FermosaCollectionsScraper(collections_url, pages)
    scraped_data = scraper.scrape_plant_data()

    excel_path = r"files\results.xlsx"
    FermosaCollectionsScraper.dump_to_excel(excel_path, scraped_data)

    csv_path = r"files\results.csv"
    FermosaCollectionsScraper.dump_to_csv(csv_path, scraped_data)


if __name__ == "__main__":
    main()
