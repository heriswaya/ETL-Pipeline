# tests/test_load.py

import unittest
import pandas as pd
from utils.load import save_to_csv, save_to_gsheet, save_to_postgres
from unittest.mock import patch, MagicMock
import os

class TestLoad(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame([{
            "Title": "Mock T-Shirt",
            "Price": 160000.0,
            "Rating": 4.5,
            "Colors": "3",
            "Size": "M",
            "Gender": "Unisex",
            "Timestamp": "2025-05-13T10:00:00"
        }])

    def test_save_to_csv(self):
        filepath = "test_products.csv"
        save_to_csv(self.df, filepath=filepath)
        self.assertTrue(os.path.exists(filepath))
        os.remove(filepath)

    @patch("utils.load.build")
    @patch("utils.load.Credentials.from_service_account_file")
    def test_save_to_gsheet(self, mock_creds, mock_build):
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_sheet = mock_service.spreadsheets.return_value
        mock_sheet.values().update().execute.return_value = {"updatedCells": 7}

        try:
            save_to_gsheet(self.df, "dummy_spreadsheet_id")
        except Exception:
            self.fail("save_to_gsheet() raised Exception unexpectedly!")

    @patch("utils.load.create_engine")
    def test_save_to_postgres(self, mock_engine):
        mock_conn = mock_engine.return_value
        try:
            save_to_postgres(self.df, db_url="postgresql://dummy:pass@localhost/db", table_name="mock")
        except Exception:
            self.fail("save_to_postgres() raised Exception unexpectedly!")

if __name__ == "__main__":
    unittest.main()
