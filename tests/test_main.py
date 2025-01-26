import json
from unittest.mock import mock_open, patch

import pytest

from src.main import Category, Product, get_information_from_json, Smartphone, LawnGrass


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


def test_category_add_product_increments_count(sample_category, sample_product):
    """Тест на проверку увеличения счетчика продуктов при добавлении"""
    initial_total_count = Category.total_products_count
    sample_category.add_product(sample_product)
    assert Category.total_products_count == initial_total_count + 1


def test_product_str(sample_product):
    """Тест строкового представления продукта"""
    expected_output = "Laptop, 1000.99 руб. Остаток: 5 шт."
    assert str(sample_product) == expected_output


def test_category_str_with_no_products(sample_category):
    """Тест строкового представления категории без продуктов"""
    expected_output = "Electronics, количество продуктов: 0 шт."
    assert str(sample_category) == expected_output


def test_category_str_with_products(sample_category, sample_product):
    """Тест на строковый вывод категории с продуктами"""
    sample_category.add_product(sample_product)
    expected_output = "Electronics, количество продуктов: 5 шт."
    assert str(sample_category) == expected_output


def test_product_addition(sample_product):
    """Тест сложения продуктов для подсчета полной стоимости"""
    product_a = Product("PS4", "PS4 Mini", 499.99, 5)
    product_b = Product("Monitor", "Monitor Dell Vepro", 599.99, 10)
    total_cost = product_a + product_b
    expected_total = (499.99 * 5) + (599.99 * 10)
    assert total_cost == expected_total


def test_product_addition_type_error(sample_product):
    """Тест ошибки типа при сложении продукта с другим объектом"""
    with pytest.raises(TypeError, match="Сложение возможно только между объектами класса Product"):
        sample_product + "Not a Product"


def test_product_addition_same_class():
    """Тест сложения продуктов одного типа"""
    smartphone_a = Smartphone("iPhone 14", "Apple Smartphone", 1000.0, 3, "iPhone 14", "256GB", "Black", "High")
    smartphone_b = Smartphone(
        "Samsung Galaxy S23", "Samsung Smartphone", 900.0, 5, "Galaxy S23", "128GB", "Blue", "High"
    )
    total_cost = smartphone_a + smartphone_b
    expected_total = (1000.0 * 3) + (900.0 * 5)
    assert total_cost == expected_total


def test_product_addition_different_class():
    """Тест ошибки сложения продуктов разных типов"""
    smartphone = Smartphone("iPhone 14", "Apple Smartphone", 1000.0, 3, "iPhone 14", "256GB", "Black", "High")
    lawn_grass = LawnGrass("Kentucky Bluegrass", "Grass Seeds", 20.0, 100, "USA", "7-10 days", "Green")
    with pytest.raises(TypeError, match="Сложение возможно только между объектами класса Product"):
        _ = smartphone + lawn_grass


def test_category_add_product_valid_types():
    """Тест добавления корректных типов продуктов в категорию"""
    category = Category("Garden", "All garden-related products")
    smartphone = Smartphone("iPhone 14", "Apple Smartphone", 1000.0, 3, "iPhone 14", "256GB", "Black", "High")
    lawn_grass = LawnGrass("Kentucky Bluegrass", "Grass Seeds", 20.0, 100, "USA", "7-10 days", "Green")
    category.add_product(smartphone)
    category.add_product(lawn_grass)
    assert len(category._Category__products) == 2


def test_category_add_product_invalid_type():
    category = Category(name="Test ", description="Test ")

    with pytest.raises(TypeError, match="Должен быть объектом класса Product."):
        category.add_product("Не продукт")


def test_smartphone_properties():
    """Тест дополнительных свойств класса Smartphone"""
    smartphone = Smartphone("iPhone 14", "Apple Smartphones", 1000.0, 19, "iPhone 14", "256GB", "Pink", "High")
    assert smartphone.model == "iPhone 14"
    assert smartphone.memory == "256GB"
    assert smartphone.color == "Pink"
    assert smartphone.efficiency == "High"


def test_lawn_grass_properties():
    """Тест дополнительных свойств класса LawnGrass"""
    lawn_grass = LawnGrass("Grass", "Grass Green", 11.0, 101, "Canada", "7-9 days", "Red")
    assert lawn_grass.country == "Canada"
    assert lawn_grass.germination_period == "7-9 days"
    assert lawn_grass.color == "Red"
