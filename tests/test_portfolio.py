from src.axentx_product.portfolio import Portfolio
from src.axentx_product.product import Product

def test_portfolio_creation():
    portfolio = Portfolio()
    assert portfolio.products == []

def test_add_product_to_portfolio():
    portfolio = Portfolio()
    product = Product("Test Product", 10)
    portfolio.add_product(product)
    assert len(portfolio.products) == 1
    assert portfolio.products[0].name == "Test Product"

def test_get_products_from_portfolio():
    portfolio = Portfolio()
    product1 = Product("Test Product 1", 10)
    product2 = Product("Test Product 2", 20)
    portfolio.add_product(product1)
    portfolio.add_product(product2)
    products = portfolio.get_products()
    assert len(products) == 2
    assert products[0].name == "Test Product 1"
    assert products[1].name == "Test Product 2"
