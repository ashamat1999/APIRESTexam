from Models.Inventory import Inventory

# Class to represent an Order 
class Order:


    def __init__(self, order):
        self.id=order['id']
        self.table=order['table']
        self.productsSKUS=order['productsSKUS'] # Should be a list object.
        self.status=order['status']

        inventory=Inventory()
        skus=[productInventory.get_product_dict()['sku'] for productInventory in inventory.inventoryProducts ]
        total=0
        
        # Calculate total of Order and initialize it.
        for productSku in self.productsSKUS:
            if productSku in skus:
                price=inventory.use_product_in_order(productSku)
                total += price


        self.total=total

    # Method to return instance data as string in a dictionary form.
    def __str__(self):
        
        listSkus=[]

        for productSKU in self.productsSKUS:
            listSkus.append(f'"{productSKU}"') # Get all productSKUS into a list

        stringProductsSkus = ",".join(listSkus) # Convert productsSKUS into string

        return '{ "id" : "%s", "table" : %i, "productsSKUS" : [%s], "status" : "%s", "total": %f}' % (self.id, self.table, stringProductsSkus, self.status, self.total)

    # Function to get order as dictionary
    def get_order(self):
        order={
            "id" : self.id,
            "table" : self.table,
            "productsSKUS" : self.productsSKUS,
            "total" : self.total,
            "status" : self.status
        }

        return order

    # Necessary setters    
    def set_status(self, status):
        self.status=status

    def set_id(self, id):
        self.id=id
