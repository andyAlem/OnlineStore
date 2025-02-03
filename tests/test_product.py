import pytest

from src.product import BaseProduct, LawnGrass, Product, Smartphone


def test_baseproduct_instantiation_fails():
    """Тест: попытка создания экземпляра абстрактного класса BaseProduct должна вызвать TypeError"""
    with pytest.raises(
        TypeError, match="Can't instantiate abstract class BaseProduct with abstract methods __init__, __str__"
    ):
        BaseProduct("Test", "Test description", 100.0, 10)


def test_product_is_subclass_of_baseproduct():
    """Тест: класс Product должен быть подклассом BaseProduct"""
    assert issubclass(Product, BaseProduct), "Класс Product должен наследоваться от BaseProduct"


def test_smartphone_is_subclass_of_product():
    """Тест: класс Smartphone должен быть подклассом Product"""
    assert issubclass(Smartphone, Product), "Класс Smartphone должен наследоваться от Product"


def test_lawngrass_is_subclass_of_product():
    """Тест: класс LawnGrass должен быть подклассом Product"""
    assert issubclass(LawnGrass, Product), "Класс LawnGrass должен наследоваться от Product"


def test_product_price_setter_positive(sample_product):
    """Тест: успешное изменение цены у продукта"""
    sample_product.price = 2000.99
    assert sample_product.price == 2000.99


def test_product_price_setter_negative(sample_product):
    """Тест: установка отрицательной цены должна оставлять старое значение"""
    sample_product.price = -500
    assert sample_product.price == 1000.99, "Цена не должна быть отрицательной, должно сохраняться старое значение."


def test_product_price_setter_zero(sample_product):
    """Тест: установка нулевой цены должна оставлять старое значение"""
    sample_product.price = 0
    assert sample_product.price == 1000.99, "Цена не должна быть нулевой, должно сохраняться старое значение."


def test_product_new_product_valid():
    """Тест: класс-метод new_product должен корректно создавать объект Product при валидных данных"""
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
    """Тест, класс-метод new_product должен выбрасывать ValueError при отсутствии обязательного поля"""
    product_data = {
        "name": "Smartphone",
        "description": "High-end smartphone",
        "price": 500.0,
    }
    with pytest.raises(ValueError, match="Отсутствует обязательное поле: quantity"):
        Product.new_product(product_data)


def test_product_str(sample_product):
    """Тест: строковое представление продукта должно соответствовать ожидаемому формату"""
    expected_output = "Laptop, 1000.99 руб. Остаток: 5 шт."
    assert str(sample_product) == expected_output


def test_product_addition():
    """Тест: сложение двух объектов Product должно возвращать корректную сумму стоимости всех товаров"""
    product_a = Product("PS4", "PS4 Mini", 499.99, 5)
    product_b = Product("Monitor", "Monitor Dell Vepro", 599.99, 10)
    total_cost = product_a + product_b
    expected_total = (499.99 * 5) + (599.99 * 10)
    assert total_cost == expected_total, "Сумма стоимости товаров рассчитана неверно."


def test_product_addition_type_error(sample_product):
    """Тест: сложение объекта Product с не-Product должно вызывать TypeError"""
    with pytest.raises(TypeError, match="Сложение возможно только между объектами класса Product"):
        sample_product + "Not a Product"
