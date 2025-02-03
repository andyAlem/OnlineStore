import json
import os
from unittest.mock import mock_open, patch

import pytest

from src.main import get_information_from_json


def test_load_valid_data(mock_json_data):
    """Тест для загрузки корректных данных"""
    filepath = os.path.join(os.path.dirname(__file__), "..", "data", "products.json")

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        categories = get_information_from_json(filepath)

        assert len(categories) == 2
        assert categories[0].name == "Смартфоны"
        assert len(categories[0].product.split("\n")) == 3
        assert categories[1].name == "Телевизоры"
        assert len(categories[1].product.split("\n")) == 1


def test_file_not_found():
    """Тест для случая, когда файл не существует."""
    filepath = "/path/to/nonexistent/file.json"

    with patch("builtins.open", mock_open(read_data="")):
        with pytest.raises(FileNotFoundError):
            get_information_from_json(filepath)


def test_missing_required_fields():
    """Тест для случая, когда в JSON отсутствуют обязательные поля."""
    invalid_json = """[
        {
            "name": "Смартфоны",
            "description": "Смартфоны, как средство не только коммуникации, но и получение дополнительных функций для удобства жизни",
            "products": [
                {"name": "Samsung Galaxy", "description": "Без камеры", "quantity": 5},
                {"name": "Iphone", "description": "Без цены", "price": 1000}
            ]
        }
    ]"""

    with patch("builtins.open", mock_open(read_data=invalid_json)):
        with patch("os.path.exists", return_value=True):
            categories = get_information_from_json("/path/to/invalid_file.json")

            assert len(categories) == 1
            assert len(categories[0].product.split("\n")) == 1
