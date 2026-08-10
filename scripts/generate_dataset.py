import pandas as pd 
import random as rd
from datetime import datetime, timedelta

data = []
NUMBER_OF_ROWS = 10_000
PRODUCTS = {
    "Laptop": {
        "category": "Electronics",
        "min_price": 25000,
        "max_price": 40000,
    },
    "Mouse": {
        "category": "Electronics",
        "min_price": 150,
        "max_price": 800,
    },
    "Keyboard": {
        "category": "Electronics",
        "min_price": 400,
        "max_price": 2000,
    },
    "Monitor": {
        "category": "Electronics",
        "min_price": 3000,
        "max_price": 12000,
    },
    "Headphones": {
        "category": "Electronics",
        "min_price": 500,
        "max_price": 5000,
    },
}
for order_id in range(1, NUMBER_OF_ROWS + 1):
    product = rd.choice(list(PRODUCTS.keys()))
    product_info = PRODUCTS[product]
    category = product_info["category"]
    unit_price = rd.randint(
        product_info["min_price"],
        product_info["max_price"]
    )
    quantity = rd.randint(1, 5)
    total_price = unit_price * quantity
    row = {
        "order_id": order_id,

        "customer_name": rd.choice(
            ["Ahmed", "Sara", "Omar", "Mona", "Ali", "Youseef", "Nada", "Laila"]
        ),
        "customer_age": rd.randint(18, 65),
        "customer_gender": rd.choice(["male", "female"]),
        "city": rd.choice(
            [
            "Cairo",
            "Alexandria",
            "Giza",
            "Mansoura",
            "Tanta",
            "Aswan",
            "Luxor",
            "Suez",
            ]

        ),
        "product": product,
        "category": category,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_price": total_price,

    }
    data.append(row)

df = pd.DataFrame(data)
df.to_csv("data/raw/sales_data.csv", index=False)
print("Dataset generated successfully")
