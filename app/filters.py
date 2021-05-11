from operator import attrgetter

def filter_products(column, value, products):
    """Filter products table."""
    prods=[]
    if value == "selling":
        value = "Selling"
    if value == "not_selling":
        value = "Not Selling"
    if column == "selling_status":
        for prod in products:
            if prod.category == value:
                prods.append(prod)
    return prods

def filter_orders(column, value, orders):
    """Filter orders table."""
    ords=[]
    value = value.replace("_", " ")
    if column == "name":
        ords = sorted(orders, key=attrgetter("name"))
    elif column == "email":
        ords = sorted(orders, key=attrgetter("email"))
    elif column == "order_status":
        for order in orders:
            if order.status == value:
                ords.append(order)
    elif column == "payment_type":
        for order in orders:
            if order.payment_type == value:
                ords.append(order)
    elif column == "payment_status":
        for order in orders:
            if order.payment_status == value:
                ords.append(order)
    return ords

def search_orders(column, value, orders):
    """Search through orders."""
    ords=[]
    if column == "pickup_time":
        for order in orders:
            if order.status != 'fulfilled' and order.pickup_time == value:
                ords.append(order)
    return ords
