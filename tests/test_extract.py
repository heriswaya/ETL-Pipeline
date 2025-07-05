# tests/test_extract.py

import unittest
from unittest.mock import patch
from utils.extract import extract_product_data

# Mock response HTML untuk satu produk
MOCK_HTML = """
<div class="collection-card">
  <div class="product-details">
    <h3 class="product-title">Mock T-Shirt</h3>
    <div class="price-container"><span class="price">$10.00</span></div>
    <p style="font-size: 14px;">Rating: ⭐ 4.5 / 5</p>
    <p style="font-size: 14px;">3 Colors</p>
    <p style="font-size: 14px;">Size: M</p>
    <p style="font-size: 14px;">Gender: Unisex</p>
  </div>
</div>
"""

class TestExtract(unittest.TestCase):
    @patch("utils.extract.requests.get")
    def test_extract_product_data_returns_valid_data(self, mock_get):
        # Mock hanya satu halaman
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = MOCK_HTML

        data = extract_product_data()

        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        product = data[0]
        self.assertIn("Title", product)
        self.assertIn("Price", product)
        self.assertIn("Rating", product)
        self.assertIn("Colors", product)
        self.assertIn("Size", product)
        self.assertIn("Gender", product)
        self.assertIn("Timestamp", product)

        self.assertEqual(product["Title"], "Mock T-Shirt")
        self.assertEqual(product["Price"], "10.00")
        self.assertEqual(product["Rating"], 4.5)
        self.assertEqual(product["Colors"], "3")
        self.assertEqual(product["Size"], "M")
        self.assertEqual(product["Gender"], "Unisex")

    @patch("utils.extract.requests.get")
    def test_extract_handles_invalid_page(self, mock_get):
        # Simulasikan request error (contoh: 404)
        mock_get.side_effect = Exception("Network error")

        data = extract_product_data()
        self.assertEqual(data, [])  # Harus kembalikan list kosong jika gagal semua

if __name__ == "__main__":
    unittest.main()
