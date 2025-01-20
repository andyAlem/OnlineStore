import json
from unittest.mock import mock_open, patch

import pytest

from src.main import Category, Product, get_information_from_json


def test_product_price_setter_positive(sample_product):
    """Тест на успешное изменение цены"""
    sample_product.price = 2000.99
    assert sample_product.price == 2000.99


def test_product_price_setter_negative(sample_product):
    """Тест на установку отрицательной цены"""
    sample_product.price = -500
    assert sample_product.price == 1000.99


def test_product_price_setter_zero(sample_product):
    """Тест на установку нулевой цены"""
    sample_product.price = 0
    assert sample_product.price == 1000.99


def test_category_product_list_empty(sample_category):
    """Тест геттера списка продуктов, если список пуст"""
    assert sample_category.product == "В категории нет товаров."


def test_category_product_list_with_products(sample_category, sample_product):
    """Тест геттера списка продуктов с товарами"""
    sample_category.add_product(sample_product)
    expected_output = "Laptop, 1000.99 руб. Остаток: 5 шт."
    assert sample_category.product == expected_output


def test_product_new_product_valid():
    """Тест класс-метода new_product с валидными данными"""
    product_data = {
        "name": "Smartphone",
        "description": "High-end smartphone",
        "price": 500.0,
        "quantity": 10,
    }
    product = Product.new_product(product_data)
    assert product.name == "Smartphone"
    assert product.description == "High-end smartphone"
    assert product.price == 500.0
    assert product.quantity == 10


def test_product_new_product_invalid():
    """Тест класс-метода new_product с отсутствующим полем"""
    product_data = {
        "name": "Smartphone",
        "description": "High-end smartphone",
        "price": 500.0,
    }
    with pytest.raises(ValueError, match="Отсутствует обязательное поле: quantity"):
        Product.new_product(product_data)


def test_get_information_from_json_incomplete_product():
    """Тест обработки категории с продуктами, у которых не хватает полей"""
    incomplete_data = json.dumps(
        [
            {
                "name": "Category 1",
                "description": "Description for Category 1",
                "products": [
                    {"name": "Incomplete Product", "description": "Missing price and quantity"}
                ],
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


def test_category_add_product_increments_count(sample_category, sample_product):
    """Проверка увеличения счетчика продуктов при добавлении"""
    initial_total_count = Category.total_products_count
    sample_category.add_product(sample_product)
    assert Category.total_products_count == initial_total_count + 1
