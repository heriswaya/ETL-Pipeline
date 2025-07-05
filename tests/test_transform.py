# tests/test_transform.py

import unittest
from utils.transform import transform_data

class TestTransform(unittest.TestCase):

    def test_transform_valid_data(self):
        raw_data = [
            {
                "Title": "Kaos Keren",
                "Price": "100.0",
                "Rating": 4.2,
                "Colors": "3",
                "Size": "M",
                "Gender": "Unisex",
                "timestamp": "2025-05-13T10:00:00"
            }
        ]

        df = transform_data(raw_data)

        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["Title"], "Kaos Keren")
        self.assertEqual(df.iloc[0]["Price"], 1600000.0)  # 100 * 16000

    def test_transform_removes_unknown_and_nulls(self):
        raw_data = [
            {
                "Title": "Unknown Product",
                "Price": "100.0",
                "Rating": 4.2,
                "Colors": "3",
                "Size": "M",
                "Gender": "Unisex",
                "Timestamp": "2025-05-13T10:00:00"
            },
            {
                "Title": "Produk Kosong",
                "Price": None,
                "Rating": 3.0,
                "Colors": "2",
                "Size": "L",
                "Gender": "Men",
                "Timestamp": "2025-05-13T10:00:00"
            }
        ]

        df = transform_data(raw_data)
        self.assertEqual(len(df), 0)

    def test_transform_handles_invalid_input(self):
        # Masukkan data yang bukan list (simulasi error)
        df = transform_data("bukan list")
        self.assertTrue(df.empty)

if __name__ == "__main__":
    unittest.main()
