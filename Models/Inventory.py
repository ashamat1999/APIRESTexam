import os
import json

from Models.Product import Product

class Inventory:
    inventoryProducts=[]

    def __init__(self):

        cwd = os.getcwd()
        self.path=cwd+"\data\inventory.txt"

        self.load_data()

    def load_data(self):
        self.inventoryProducts=[]
        
        if os.path.exists(self.path):
            with open(self.path, 'r') as inventoryFile:
                inventoryFile.seek(0)
                inventoryProductsRaw=inventoryFile.readlines()
                print("---loadData1---->",inventoryFile.readlines())

            if len(inventoryProductsRaw) != 0:
                for productJSON in inventoryProductsRaw:
                    print('---loadData-->',type(json.loads(productJSON)))
                    self.inventoryProducts.append(Product(json.loads(productJSON)))

                #print('---loadData-->',type(self.inventoryProducts[0]))
                #print('---loadData-->',(self.inventoryProducts))

        else:
            print("Inventory file not found, creating new one...")
            file=open(self.path, 'w')
            file.close()
            print("Inventory file created sucessfully")

    def save_data(self):
        
        print("----saveData-->", self.inventoryProducts)

        try:
            with open(self.path, 'w') as inventoryFile:

                for product in self.inventoryProducts:
                    
                    inventoryFile.write(product.__str__())
                    inventoryFile.write('\n')

        except FileNotFoundError:
            raise FileNotFoundError("Inventory file not found, can't save")

    def add_product(self, product):
        self.load_data()
        print("---addProduct--->",(product))

        if len(self.inventoryProducts)>0:

            skus=[productInventory.get_product_dict()['sku'] for productInventory in self.inventoryProducts]

            print("---addProductSkus--->", skus)
            print("---addProductSku--->", product.get_product_dict()['sku'])
            if product.get_product_dict()['sku'] in skus : 
                print("SKU: %s already exists!, can't save data." % (product.get_product_dict()['sku']))
                return False
            else:
                self.inventoryProducts.append(product)
                self.save_data()
                return True
        else:
            self.inventoryProducts.append(product)
            self.save_data()
            return True
            

    def delete_product(self, sku):
        self.load_data()
        index=-1

        for productInInventory in self.inventoryProducts:
            if productInInventory.get_product_dict()['sku'] == sku:
                index=self.inventoryProducts.index(productInInventory)

        if index>=0:
            del self.inventoryProducts[index]
            self.save_data()
        else:
            print("Product was not found in the inventory")

    def update_product(self, sku, product):
        self.load_data()
        index=-1

        for productInInventory in self.inventoryProducts:
            if productInInventory.get_product_dict()['sku'] == sku:
                print("--->updateProduct--->", productInInventory)
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
        
        
    def get_inventory_products(self):
        inventoryProductsDict=[product.get_product_dict() for product in self.inventoryProducts]
        return inventoryProductsDict

    def get_inventory_products_nojson(self):
        inventoryProductsDict=[product for product in self.inventoryProducts]
        return inventoryProductsDict
        
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

            
    


    

    
        

    
