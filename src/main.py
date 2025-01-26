import json
import os


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict):
        """Класс-метод принимает на вход параметры товара в словаре и возвращать созданный объект класса"""
        required_keys = ["name", "description", "price", "quantity"]
        for k in required_keys:
            if k not in product_data:
                raise ValueError(f"Отсутствует обязательное поле: {k}")

        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    @property
    def price(self):
        """Геттер для получения значения цены"""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """Сеттер устанавливает новую цену"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    def __str__(self):
        """Строковое представление продукта для класса Product"""
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Сложение продуктов для подсчета общей стоимости"""
        if type(self) == type(other):  # проверка через type()
            return self.price * self.quantity + other.price * other.quantity
        else:
            raise TypeError("Сложение возможно только между объектами класса Product.")


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        model: str,
        memory: str,
        color: str,
        efficiency: str,
    ):
        super().__init__(name, description, price, quantity)
        self.model = model
        self.memory = memory
        self.color = color
        self.efficiency = efficiency


class LawnGrass(Product):
    """Класс для газонной травы?"""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    category_count = 0
    total_products_count = 0

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1

    def add_product(self, product):
        """Специальный метод для добавления продукта в категорию."""
        if isinstance(product, Product):
            self.__products.append(product)
            Category.total_products_count += 1
        else:
            raise TypeError("Должен быть объектом класса Product.")  # через if и еlse

    @property
    def product(self):
        """Геттер выводит список товаров в формате строки."""
        if not self.__products:
            return "В категории нет товаров."
        return "\n".join(
            [f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт." for product in self.__products]
        )

    def __str__(self):
        """Строковое представление категории для класса Category"""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


### Дополнительное задание


def get_information_from_json(filepath: str):
    """Функция для загрузки данных по категориям и товарам из файла JSON"""
    categories = []
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл {filepath} не найден.")
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            for category_data in data:
                name = category_data.get("name", "Unknown Category")
                description = category_data.get("description", "")
                category = Category(name=name, description=description)

                for product_data in category_data.get("products", []):
                    try:
                        price = product_data["price"]
                        quantity = product_data["quantity"]
                    except KeyError as e:
                        print(f"Пропущено обязательное поле: {e}")
                        continue

                    product = Product(
                        name=product_data["name"],
                        description=product_data["description"],
                        price=price,
                        quantity=quantity,
                    )
                    category.add_product(product)

                categories.append(category)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки данных из файла: {e}")
    return categories


# if __name__ == "__main__":
#     filepath = "/home/andrej/Poetry_homework/OOP/data/products.json"
#     categories = get_information_from_json(filepath)
#
#     for category in categories:
#         print(f"\nКатегория: {category.name}")
#         print(f"Описание: {category.description}")
#         print("Список товаров:")
#         print(category.product)
#
#     if categories and categories[0].product:
#
#         first_product = categories[0]._Category__products[0]
#         print(f"\nТекущая цена первого товара: {first_product.price} руб.")
#
#         first_product.price = 200
#         print(f"Обновленная цена первого товара: {first_product.price} руб.")
#
#         first_product.price = 50
#         print(f"Цена после изменения : {first_product.price} руб.")
