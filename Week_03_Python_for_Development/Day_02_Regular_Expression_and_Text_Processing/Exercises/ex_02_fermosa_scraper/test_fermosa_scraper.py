import unittest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
import requests
from fermosa_scraper import FermosaCollectionsScraper


class TestFermosaCollectionsScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize the scraper."""
        collections_url = "https://fermosaplants.com/collections/sansevieria"
        pages = 2
        cls.scraper = FermosaCollectionsScraper(collections_url, pages)

    @patch("fermosa_scraper.requests.get")
    def test_cook_soup_success(self, mock_get):
        """Test if cook_soup correctly fetches and parses HTML."""
        mock_response = Mock()
        mock_response.text = "<html><body><h1>Test Page</h1></body></html>"
        mock_get.return_value = mock_response
        soup = self.scraper.cook_soup("https://example.com")

        mock_get.assert_called_with("https://example.com", timeout=10)
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertEqual(soup.find("h1").text, "Test Page")

    @patch("fermosa_scraper.requests.get")
    def test_cook_soup_failure(self, mock_get):
        """Test cook_soup handlin errors."""
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")
        soup = self.scraper.cook_soup("https://invalid-url.com")

        mock_get.assert_called_with("https://invalid-url.com", timeout=10)
        self.assertIsNone(soup)

    def test_extract_scientific_name(self):
        """Test extracting scientific name from product description."""
        product_desc = "Scientific Name- Sansevieria Moonshine"
        name = self.scraper.extract_scientific_name(product_desc)
        self.assertEqual(name, "Sansevieria Moonshine")

        product_desc = "Black Gold Compacta"
        name = self.scraper.extract_scientific_name(product_desc)
        self.assertEqual(name, "Black Gold Compacta")

        product_desc = "Scientific Name- SANSEVIERIA Moonshine"
        name = self.scraper.extract_scientific_name(product_desc)
        self.assertEqual(name, "Sansevieria Moonshine")

        product_desc = "No match case."
        name = self.scraper.extract_scientific_name(product_desc)
        self.assertEqual(name, "Sansevieria (Default)")

    def test_extract_combo_names(self):
        """Test extracting combo names from product description."""
        product_desc = "1. Mini Boncel, 2. Francisii, 3. Silver steel"
        names = self.scraper.extract_combo_names(product_desc)
        self.assertEqual(names, ["Mini Boncel", "Francisii", "Silver Steel"])

        product_desc = "1. Mini Boncel, 2. Francisii, 3. Silver steel"
        names = self.scraper.extract_combo_names(product_desc)
        self.assertEqual(names, ["Mini Boncel", "Francisii", "Silver Steel"])

        product_desc = "1.  Plant Name 2. Plant Name2 3. Plant Name34. Plant5. Plant 67. Last plantIncluding shipping 689. Last last plant Including shipping 8.Final Plant"
        names = self.scraper.extract_combo_names(product_desc)
        self.assertEqual(
            names,
            [
                "Plant Name",
                "Plant Name2",
                "Plant Name3",
                "Plant",
                "Plant",
                "Last Plant",
                "Last Last Plant",
                "Final Plant",
            ],
        )

        product_desc = "no plants here."
        names = self.scraper.extract_combo_names(product_desc)
        self.assertEqual(names, [])

    def test_extract_price(self):
        """Test extracting product price from HTML."""
        soup = BeautifulSoup('<ins class="enj-product-price">Rs. 1500</ins>', "lxml")
        price = self.scraper.extract_price(soup)
        self.assertEqual(price, "Rs. 1500")

        soup = BeautifulSoup('<ins class="product-price">Rs. 1500</ins>', "lxml")
        price = self.scraper.extract_price(soup)
        self.assertEqual(price, "N/A")

    def test_extract_url(self):
        """Test extracting product listing URL."""
        soup = BeautifulSoup(
            '<h4 class="title-product"><a href="/product-link"></a></h4>', "lxml"
        )
        url = self.scraper.extract_url(soup)
        self.assertEqual(url, "https://fermosaplants.com/product-link")

        soup = BeautifulSoup("<h1>Nothing here<h1>", "lxml")
        url = self.scraper.extract_url(soup)
        self.assertEqual(url, "https://fermosaplants.com/#")

        soup = BeautifulSoup('<h4 class="title-product">No href here</h4>', "lxml")
        url = self.scraper.extract_url(soup)
        self.assertEqual(url, "https://fermosaplants.com/#")

    # @patch("fermosa_scraper.requests.get")
    # def test_extract_urls_from_all_pages(self, mock_get):
    #     """Test extracting URLs from multiple pages."""
    #     mock_response = Mock()
    #     mock_response.text = '<div class="product-item-v5"><h4 class="title-product"><a href="/product1"></a></h4></div>'
    #     mock_get.return_value = mock_response

    #     urls = self.scraper.extract_urls_from_all_pages()
    #     self.assertEqual(urls, ["https://fermosaplants.com/product1"])

    @patch("fermosa_scraper.requests.get")
    def test_process_listing(self, mock_get):
        """Test processing a single product listing."""
        mock_response = Mock()
        mock_response.text = """
        <div class="tab-pd-details">
            <div class="product-desc">Scientific Name- Sansevieria Moonshine</div>
        </div>
        <h2 class="product-title">Sansevieria Plant</h2>
        <ins class="enj-product-price">Rs. 2000</ins>
        """
        mock_get.return_value = mock_response

        result = self.scraper.process_listing("https://fermosaplants.com/product1")
        self.assertEqual(result["Scientific Name"], "Sansevieria Moonshine")
        self.assertEqual(result["Price"], "Rs. 2000")
        self.assertEqual(result["Product Listing"], "Sansevieria Plant")

    @patch("fermosa_scraper.requests.get")
    def test_handle_missing_details(self, mock_get):
        """Test handling missing product details."""
        mock_response = Mock()
        mock_response.text = "<html><body>No details</body></html>"
        mock_get.return_value = mock_response

        result = self.scraper.process_listing("https://fermosaplants.com/product1")
        self.assertEqual(result["Product Listing"], "N/A")
        self.assertEqual(result["Price"], "N/A")
        self.assertEqual(result["Scientific Name"], "N/A")
        self.assertEqual(result["URL"], "https://fermosaplants.com/product1")


if __name__ == "__main__":
    unittest.main()
