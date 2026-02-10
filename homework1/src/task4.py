def calculate_discount(price,discount):
    """calculates final price of a product given price and discound in int or float"""
    savings = price * (discount / 100)
    return price - savings
