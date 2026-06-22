from src.axentx_product.product import Product

def test_product_creation():
    product = Product("Test Product", 10)
    assert product.name == "Test Product"
    assert product.demand == 10

def test_product_string_representation():
    product = Product("Test Product", 10)
    assert str(product) == "Product 'Test Product' with demand 10"
