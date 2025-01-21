import json
from products import Product, get_product
from cart import dao


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @classmethod
    def load(cls, data):
        # Deserialize JSON contents into Product objects
        contents = [Product(**item) for item in json.loads(data['contents'])]
        return cls(data['id'], data['username'], contents, data['cost'])


def get_cart(username: str) -> list[Product]:
    """
    Retrieve the cart contents for a given username.

    Args:
        username (str): The username whose cart needs to be retrieved.

    Returns:
        list[Product]: A list of Product objects in the cart.
    """
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        # Parse JSON instead of using eval() for security
        contents = json.loads(cart_detail['contents'])
        items.extend(contents)

    # Retrieve full product details for each item
    return [get_product(product_id) for product_id in items]


def add_to_cart(username: str, product_id: int):
    """
    Add a product to the user's cart.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    """
    Remove a product from the user's cart.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    """
    Delete the entire cart for a user.
    """
    dao.delete_cart(username)

