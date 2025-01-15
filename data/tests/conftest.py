@pytest.fixture
def sample_product():
    return Product("Laptop", "High-performance laptop", 1000.99, 5)


@pytest.fixture
def sample_category():
    return Category("Electronics", "Category for electronic products")