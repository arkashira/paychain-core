from src.axentx_product.validation import Validator
from src.axentx_product.product import Product

def test_product_validation():
    validator = Validator()
    product = Product("Test Product", 10)
    assert validator.validate_product(product) == True

def test_product_validation_with_zero_demand():
    validator = Validator()
    product = Product("Test Product", 0)
    assert validator.validate_product(product) == False
