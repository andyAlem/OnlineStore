import json

import pytest

from src.main import Category, Product


@pytest.fixture
def sample_product():
    return Product("Laptop", "High-performance laptop", 1000.99, 5)


@pytest.fixture
def sample_category():
    return Category("Electronics", "Category for electronic products")


@pytest.fixture
def mock_sample_json():
    return json.dumps(
        [
            {
                "name": "Смартфоны",
                "description": (
                    "Смартфоны, как средство не только коммуникации, "
                    "но и получение дополнительных функций для удобства жизни"
                ),
                "products": [
                    {
                        "name": "Samsung Galaxy C23 Ultra",
                        "description": "256GB, Серый цвет, 200MP камера",
                        "price": 180000.0,
                        "quantity": 5,
                    },
                    {"name": "Iphone 15", "description": "512GB, Gray space", "price": 210000.0, "quantity": 8},
                    {"name": "Xiaomi Redmi Note 11", "description": "1024GB, Синий", "price": 31000.0, "quantity": 14},
                ],
            },
            {
                "name": "Телевизоры",
                "description": (
                    "Современный телевизор, который позволяет наслаждаться просмотром, "
                    "станет вашим другом и помощником"
                ),
                "products": [
                    {"name": '55" QLED 4K', "description": "Фоновая подсветка", "price": 123000.0, "quantity": 7}
                ],
            },
        ]
    )
