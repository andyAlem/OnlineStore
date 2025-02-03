import json
from unittest.mock import mock_open, patch

from src.category import Category
from src.main import get_information_from_json


def test_category_product_list_empty(sample_category):
    """Тест геттера списка продуктов, если список пуст"""
    assert sample_category.product == "В категории нет товаров."


def test_category_product_list_with_products(sample_category, sample_product):
    """Тест геттера списка продуктов с товарами"""
    sample_category.add_product(sample_product)
    expected_output = "Laptop, 1000.99 руб. Остаток: 5 шт."
    assert sample_category.product == expected_output


def test_category_add_product_increments_count(sample_category, sample_product):
    """Тест на проверку увеличения счетчика продуктов при добавлении"""
    initial_total_count = Category.total_products_count
    sample_category.add_product(sample_product)
    assert Category.total_products_count == initial_total_count + 1


def test_category_str_with_no_products(sample_category):
    """Тест строкового представления категории без продуктов"""
    expected_output = "Electronics, количество продуктов: 0 шт."
    assert str(sample_category) == expected_output


def test_category_str_with_products(sample_category, sample_product):
    """Тест на строковый вывод категории с продуктами"""
    sample_category.add_product(sample_product)
    expected_output = "Electronics, количество продуктов: 5 шт."
    assert str(sample_category) == expected_output


def test_get_information_from_json_incomplete_product():
    """Тест обработки категории с продуктами, у которых не хватает полей"""
    incomplete_data = json.dumps(
        [
            {
                "name": "Category 1",
                "description": "Description for Category 1",
                "products": [{"name": "Incomplete Product", "description": "Missing price and quantity"}],
            }
        ]
    )
    file_path = "test_incomplete_product.json"
    with patch("builtins.open", mock_open(read_data=incomplete_data)):
        with patch("os.path.exists", return_value=True):
            categories = get_information_from_json(file_path)

    assert len(categories) == 1
    assert categories[0].name == "Category 1"
    assert str(categories[0].product) == "В категории нет товаров."
