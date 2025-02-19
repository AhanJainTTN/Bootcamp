"""
Learn about “National Provider Identifier (NPI)” https://en.wikipedia.org/wiki/National_Provider_Identifier on the portal https://npiregistry.cms.hhs.gov/search, one can search for details associated with an NPI. For example, use 1114473527 for the 'NPI Number' input field and click on the “Search” button The task in this assignment is to create a Python API to fetch details corresponding to an NPI as JSON. 

On the search result page, details are displayed as a table with a column name, and its value should form a JSON key-value pair. If a column has a subfield field, for example, Taxonomy, then create a nested JSON object. 

On the result page, there is 2 address fields “Mailing Address” and “Primary Practice Address”, parse the address field into JSON as Stree-1, Stree-2, state, city, pin, phone, fax, zip as nested field. 

Example list of NPI numbers: "1275568826" "1356637649" "1841383767" "1275928012" "9000000006" ...
"""

import requests
import pickle
import json
from typing import Dict, List

# Constants
REQUEST_URL = "https://npiregistry.cms.hhs.gov/api/?number={}&enumeration_type=&taxonomy_description=&name_purpose=&first_name=&use_first_name_alias=&last_name=&organization_name=&address_purpose=&city=&state=&postal_code=&country_code=&limit=&skip=&pretty=on&version=2.1"


class InvalidNPIIDError(Exception):
    """Error class to handle invalid NPI IDs."""

    def __str__(self) -> str:
        return f"Invalid NPI ID. An NPI is a unique 10-digit number used to identify health care providers. Please recheck entered ID."


def process_id(npi_id: int) -> Dict[str, str]:
    """Takes in an NPI ID as input and gets returns data from NPI registry API in dictionary format."""
    try:
        # NPI ID must contain only 10 digits - no more no less
        if not npi_id.isdigit() or len(npi_id) != 10:
            raise InvalidNPIIDError

        id_data = requests.get(REQUEST_URL.format(npi_id))
        id_data = id_data.json()

        # only add non empty results
        if id_data["result_count"] > 0:
            print(f"Processed {npi_id}.")
            return id_data["results"]

    except InvalidNPIIDError as e:
        print(e)


def process_all_ids(npi_ids: List[int]) -> List[Dict[str, str]]:
    """Takes in a list of NPI IDs and returns corresponding data as a list of dictionaries."""
    extracted_data = list()
    for npi_id in npi_ids:
        npi_data = process_id(npi_id)
        if npi_data is not None:
            extracted_data.extend(npi_data)

    return extracted_data
    # return [process_id(npi_id) for npi_id in npi_ids]


def load_ids(id_path: str) -> List[int]:
    """Loads IDs from id_path."""
    with open(id_path, "rb") as file:
        npi_ids = pickle.load(file)
        print("Loaded all NPI IDs.")

        return npi_ids


def dump_to_json(json_path, data) -> None:
    """Writes scraped data to a JSOn file."""
    with open(json_path, "w") as json_output_file:
        json.dump(data, json_output_file)
        print(f"Output data dumped to {json_path}.")


def main() -> None:
    """Entry point of the script."""
    id_path = "/home/ahan/Documents/Bootcamp/Week_03_Python_for_Development/Day_02_Regular_Expression_and_Text_Processing/Exercises/ex_01_NPI_scraper/files/npi_ids.pkl"
    npi_ids = load_ids(id_path)

    extracted_data = process_all_ids(npi_ids)

    json_path = "/home/ahan/Documents/Bootcamp/Week_03_Python_for_Development/Day_02_Regular_Expression_and_Text_Processing/Exercises/ex_01_NPI_scraper/files/results.json"
    dump_to_json(json_path, extracted_data)


if __name__ == "__main__":
    main()
