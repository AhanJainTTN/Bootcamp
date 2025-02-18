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

page_limit = 7
base_url = "https://fermosaplants.com/"

data = list()

for curr_page in range(1, page_limit + 1):

    request_url = f"https://fermosaplants.com/collections/sansevieria?page={curr_page}"
    source = requests.get(request_url).text
    print(source)

    soup = BeautifulSoup(source, "lxml")

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
        # print(f"Title: {product_title}")

        product_price = product_price.text.strip()
        extracted_data["Price"] = product_price
        # print(f"Price: {product_price}")

        product_link = urljoin(base_url, product_link)
        extracted_data["URL"] = product_link
        # print(f"URL: {product_link}")

        combo = "combo" in product_title.lower()
        extracted_data["Combo"] = combo
        # print(f"Combo: {combo}")

        data.append(extracted_data)

        # print("")

print(data)

csv_path = "/home/ahan/Documents/Bootcamp/Week_03_Python_for_Development/Day_02_Regular_Expression_and_Text_Processing/Exercises/output.csv"

with open(csv_path, "w", newline="") as csv_file:
    headers = data[0].keys() if data else []
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

import pandas as pd

df_new = pd.read_csv(csv_path)
excel_writer = pd.ExcelWriter("output.xlsx")
df_new.to_excel(excel_writer, index=False)
excel_writer.save()
