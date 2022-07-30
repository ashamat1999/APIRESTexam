# Class to represent a Product
class Product:

    def __init__(self, productraw):
        self.sku=productraw['sku']
        self.name=productraw['name']
        self.stock=productraw['stock']
        self.price=productraw['price']
    
    # Method to return instance data as string in a dictionary form.
    def __str__(self):
        return '{ "sku" : "%s", "name" : "%s", "stock" : %i, "price" : %f}' % (self.sku, self.name, self.stock, self.price)

    # Method to return instance data as a dictionary.
    def get_product_dict(self):
        product={
            "sku":self.sku, 
            "name":self.name, 
            "stock":self.stock, 
            "price":self.price
        }
        return product

    # Necessary setters
    def set_sku(self, sku):
        self.sku=sku

    def set_name(self, name):
        self.name=name
    
    def set_stock(self, stock):
        self.stock=stock
    
    def set_price(self, price):
        self.price=price
        
    # Necessary getters
    def get_price(self):
        return self.price

    # Function to substract from stock n or 1 if n is not given.
    def substract(self, n=1):
        self.stock -= n
        return self.stock
        