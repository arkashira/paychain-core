from .product import Product

class Validator:
    def __init__(self):
        pass

    def validate_product(self, product):
        # Simple validation: demand should be greater than 0
        return product.demand > 0
