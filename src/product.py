from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        """Абстрактный метод для строкового представления объекта"""
        pass


class Mixin:
    """Миксин для вывода информации о создании объекта."""

    def __init__(self):
        super().__init__()
        print(f"Создан объект {self.__class__.__name__} с параметрами: "
              f"'{self.name}', '{self.description}', {self.price}, {self.quantity}")


class Product(BaseProduct, Mixin):
    """Класс для продуктов."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        super().__init__(name, description, price, quantity)
        Mixin.__init__(self)

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."


class Smartphone(Product):
    """Класс для смартфонов."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 model: str, memory: str, color: str, efficiency: str):
        super().__init__(name, description, price, quantity)
        self.model = model
        self.memory = memory
        self.color = color
        self.efficiency = efficiency


class LawnGrass(Product):
    """Класс для газонной травы."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
