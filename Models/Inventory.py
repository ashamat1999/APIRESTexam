import os
import json

from Models.Product import Product

# Class to model and manage inventory data
class Inventory:
    # Main list of the class, this list is in practice the inventory.
    # This list is a list of Products, at same time, it could be interpreted as a list of dictionaries.
    inventoryProducts=[]

    def __init__(self):

        cwd = os.getcwd()
        self.path=cwd+"\data\inventory.txt"

        self.load_data()

    # Function to load data from txt file.
    def load_data(self):
        self.inventoryProducts=[] # Clean inventoryProducts list to load data here.
        
        if os.path.exists(self.path):                                # Verify if inventory file is created.
            with open(self.path, 'r') as inventoryFile:              
                inventoryFile.seek(0)
                inventoryProductsRaw=inventoryFile.readlines()       # Read file lines once opened.

            if len(inventoryProductsRaw) != 0:                       # Verify if already exists some products in the inventory file.
                for productJSON in inventoryProductsRaw:
                    self.inventoryProducts.append(Product(json.loads(productJSON))) # Deserialize and add Product to instance inventoryProducts list

        else:                                                       # If inventory file was not created, create one.
            print("Inventory file not found, creating new one...")
            file=open(self.path, 'w')
            file.close()
            print("Inventory file created sucessfully")

    # Function to save inventoryProducts list to inventory txt file
    def save_data(self):
        
        print("----saveData-->", self.inventoryProducts)

        try:
            with open(self.path, 'w') as inventoryFile:

                for product in self.inventoryProducts:
                    
                    inventoryFile.write(product.__str__()) # Write product as string in inventory txt file
                    inventoryFile.write('\n')

        except FileNotFoundError:
            raise FileNotFoundError("Inventory file not found, can't save")

    # Function to add product to inventory list
    def add_product(self, product):
        self.load_data()

        if len(self.inventoryProducts)>0: # Verify if there is existing products to compare its skus

            skus=[productInventory.get_product_dict()['sku'] for productInventory in self.inventoryProducts] # Obtain list with all skus in inventory

            if product.get_product_dict()['sku'] in skus : # If sku is already in inventory, print a message and return false
                print("SKU: %s already exists!, can't save data." % (product.get_product_dict()['sku']))
                return False
            else:
                self.inventoryProducts.append(product)
                self.save_data() # If sku isn't in inventory, add product to inventory and save data.
                return True
        else:
            self.inventoryProducts.append(product) # If there isn't products in inventory, just add the product.
            self.save_data()
            return True
            
    # Function to delete a product from inventory list
    def delete_product(self, sku):
        self.load_data()
        index=-1

        for productInInventory in self.inventoryProducts:
            if productInInventory.get_product_dict()['sku'] == sku: 
                index=self.inventoryProducts.index(productInInventory) # Get index of inventory list in which is the product to be deleted.

        if index>=0:
            del self.inventoryProducts[index] 
            self.save_data() # Delete prouct and save data.
        else:
            print("Product was not found in the inventory")

    # Function to update a product in inventory list
    def update_product(self, sku, product):
        self.load_data()
        index=-1

        for productInInventory in self.inventoryProducts:
            if productInInventory.get_product_dict()['sku'] == sku:
                productInInventory.set_sku(product['sku'])
                productInInventory.set_name(product['name'])
                productInInventory.set_stock(product['stock'])
                productInInventory.set_price(product['price'])
                self.save_data()

                return True

        else:
            print("Product was not found in the inventory")
            self.save_data()

            return False
        
    # Getter to get list as a list of dictionaries
    def get_inventory_products(self):
        inventoryProductsDict=[product.get_product_dict() for product in self.inventoryProducts]
        return inventoryProductsDict

    # Getter to get list as a list of Products
    def get_inventory_products_nojson(self):
        inventoryProductsDict=[product for product in self.inventoryProducts]
        return inventoryProductsDict

    # Function to calculate use some product in an order. 
    # This function return price to calculate Order total   
    def use_product_in_order(self, sku):
        self.load_data()

        for productInInventory in self.inventoryProducts:
            if productInInventory.get_product_dict()['sku'] == sku:
                price=productInInventory.get_price()

                self.save_data()

                return price

        else:
            print("Product was not found in the inventory, not saving...")

            return False

            
    


    

    
        

    
