from src.product import Product


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
