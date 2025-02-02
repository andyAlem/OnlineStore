import json
import os
from src.product import Product
from src.category import Category

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


if __name__ == "__main__":
    filepath = "/home/andrej/Poetry_homework/OOP/data/products.json"
    categories = get_information_from_json(filepath)

    for category in categories:
        print(f"\nКатегория: {category.name}")
        print(f"Описание: {category.description}")
        print("Список товаров:")
        print(category.product)

    if categories and categories[0].product:

        first_product = categories[0]._Category__products[0]
        print(f"\nТекущая цена первого товара: {first_product.price} руб.")

        first_product.price = 200
        print(f"Обновленная цена первого товара: {first_product.price} руб.")

        first_product.price = 50
        print(f"Цена после изменения : {first_product.price} руб.")
