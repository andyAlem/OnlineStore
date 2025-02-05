from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
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
        print(
            f"Создан объект {self.__class__.__name__} с параметрами: "
            f"'{self.name}', '{self.description}', {self.price}, {self.quantity}"
        )


class Product(BaseProduct, Mixin):
    """Класс для продуктов."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        super().__init__(name, description, price, quantity)
        Mixin.__init__(self)

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value > 0:
            self._price = value
        else:
            print("Цена не может быть отрицательной или равной нулю. Значение остается прежним.")

    @classmethod
    def new_product(cls, data):
        required_fields = ["name", "description", "price", "quantity"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Отсутствует обязательное поле: {field}")
        return cls(data["name"], data["description"], data["price"], data["quantity"])

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError("Сложение возможно только между объектами класса Product")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    """Класс для смартфонов."""

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
    """Класс для газонной травы."""

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
