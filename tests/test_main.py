import json
from unittest.mock import mock_open, patch

from src.main import Category, get_information_from_json


def test_product_init(sample_product):
    """Проверка, что класс Product инициализируется с правильными значениями"""
    assert sample_product.name == "Laptop"
    assert sample_product.description == "High-performance laptop"
    assert sample_product.price == 1000.99
    assert sample_product.quantity == 5


def test_category_init(sample_category):
    """Проверка, что класс Product инициализируется с правильными значениями"""
    assert sample_category.name == "Electronics"
    assert sample_category.description == "Category for electronic products"
    assert len(sample_category.products) == 0


def test_add_product(sample_category, sample_product):
    """При добавлении продукта в категорию, продукт правильно добавляется в список
    продуктов категории."""
    sample_category.add_product(sample_product)
    assert len(sample_category.products) == 1
    assert sample_category.products[0] == sample_product


def test_category_count():
    """Проверка счетчика категорий"""
    Category.category_count = 0
    Category("Electronics", "Category for electronic products")
    Category("Books", "Category for books")
    assert Category.category_count == 2


def test_total_products_count(sample_category, sample_product):
    """Проверка счетчика продуктов"""
    Category.total_products_count = 0
    sample_category.add_product(sample_product)
    sample_category.add_product(sample_product)
    assert Category.total_products_count == 2


def test_get_information_from_json_valid(mock_sample_json):
    """Тест на корректную загрузку json и обработку"""
    file_path = "test_valid.json"
    with patch("builtins.open", mock_open(read_data=mock_sample_json)):
        with patch("os.path.exists", return_value=True):
            categories = get_information_from_json(file_path)

    assert len(categories) == 2
    assert categories[0].name == "Смартфоны"
    assert (
        categories[0].description
        == "Смартфоны, как средство не только коммуникации, но и получение дополнительных функций для удобства жизни"
    )
    assert len(categories[0].products) == 3
    assert categories[0].products[0].name == "Samsung Galaxy C23 Ultra"
    assert categories[0].products[0].price == 180000.0
    assert categories[0].products[2].name == "Xiaomi Redmi Note 11"
    assert categories[0].products[2].quantity == 14

    assert categories[1].name == "Телевизоры"
    assert (
        categories[1].description
        == "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником"
    )
    assert len(categories[1].products) == 1
    assert categories[1].products[0].name == '55" QLED 4K'
    assert categories[1].products[0].price == 123000.0
    assert categories[1].products[0].quantity == 7


def test_get_information_from_json_file_not_found():
    file_path = "non_existent_file.json"
    with patch("os.path.exists", return_value=False):
        categories = get_information_from_json(file_path)

    assert categories == []


def test_get_information_from_json_invalid_json():
    """JSON файл не найден"""
    invalid_json = '{ "name": "Category 1", "products": [ ] '
    file_path = "test_invalid.json"
    with patch("builtins.open", mock_open(read_data=invalid_json)):
        with patch("os.path.exists", return_value=True):
            categories = get_information_from_json(file_path)

    assert categories == []


def test_get_information_from_json_empty_file():
    """JSON файл пустой"""
    empty_json = "[]"
    file_path = "test_empty.json"
    with patch("builtins.open", mock_open(read_data=empty_json)):
        with patch("os.path.exists", return_value=True):
            categories = get_information_from_json(file_path)

    assert categories == []


def test_get_information_from_json_missing_fields():
    """Тест на работу функции с пустыми полями, функция заполняет их пустыми значениями"""
    invalid_data = json.dumps(
        [
            {
                "name": "Category 1",
            }
        ]
    )
    file_path = "test_missing_fields.json"
    with patch("builtins.open", mock_open(read_data=invalid_data)):
        with patch("os.path.exists", return_value=True):
            categories = get_information_from_json(file_path)

    assert len(categories) == 1
    assert categories[0].name == "Category 1"
    assert categories[0].description == ""
    assert len(categories[0].products) == 0


def test_get_information_from_json_category_without_products():
    """Проверка работы функции на обработку категорий с пустыми продуктами"""
    invalid_data = json.dumps([{"name": "Category 1", "description": "Description for Category 1", "products": []}])
    file_path = "test_category_without_products.json"
    with patch("builtins.open", mock_open(read_data=invalid_data)):
        with patch("os.path.exists", return_value=True):
            categories = get_information_from_json(file_path)

    assert len(categories) == 1
    assert categories[0].name == "Category 1"
    assert categories[0].description == "Description for Category 1"
    assert len(categories[0].products) == 0
