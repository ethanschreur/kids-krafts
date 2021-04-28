def filter_products(column, value, products):
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
