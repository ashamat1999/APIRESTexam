import os
import json

from Models.Inventory import Inventory
from Models.Order import Order

# Class to model and manage inventory data
class OrderList:
    # Main list of the class.
    # This list is a list of Orders, at same time, it could be interpreted as a list of dictionaries.
    orderList=[]

    def __init__(self):

        cwd = os.getcwd()
        self.path=cwd+"\data\orderList.txt"

        self.load_data()

    # Function to load data from txt file.
    def load_data(self):
        self.orderList=[]
        
        if os.path.exists(self.path): # Verify if OrderList txt file exists
            with open(self.path, 'r') as orderFile:
                orderFile.seek(0)
                orderListRaw=orderFile.readlines() # If exists, read lines of file

            if len(orderListRaw) != 0:  # Verify if exist lines in file
                for productJSON in orderListRaw:
                    self.orderList.append(Order(json.loads(productJSON))) # Deserialize and add Order to instance orders list


        else:
            print("Order List file not found, creating new one...")
            file=open(self.path, 'w') # If txt file dont exist, create one.
            file.close()
            print("Order List file created sucessfully")

    # Function to save data to ordersList txt file
    def save_data(self):

        try:
            with open(self.path, 'w') as orderListFile:

                for order in self.orderList:
                    
                    orderListFile.write(order.__str__())
                    orderListFile.write('\n')

        except FileNotFoundError:
            raise FileNotFoundError("Inventory file not found, can't save")

    # Function to add order into ordersList
    def add_order(self, order):
        self.load_data()
        print("---addOrder--->",(order))
        inventory=Inventory()

        alert = ""

        for productInInventory in inventory.get_inventory_products_nojson():
            if productInInventory.get_product_dict()['sku'] in order.get_order()['productsSKUS']:
                stock=productInInventory.substract() # Because we are adding Orders into list, we need to substract 1 from stock of products in orders
                inventory.save_data()
                if stock < 3: # Verify if we need to alert about inventory stock
                    alert += " Stock <= 2 Units, consider to provide sku:" + productInInventory.get_product_dict()['sku'] +" "


        self.orderList.append(order)
        self.save_data()
        return order,alert
        
    # Necessary functions to manage order status
    def begin_order(self, orderId):
        self.load_data()
        for order in self.get_order_list():
            print(type(order))
            if order.get_order()['id'] == orderId:
                order.set_status('processing')
        
        self.save_data()

    def cancel_order(self, orderId):
        self.load_data()
        for order in self.get_order_list():
            print(type(order))
            if order.get_order()['id'] == orderId:
                order.set_status('cancelled')
        
        self.save_data()

    def complete_order(self, orderId):
        self.load_data()
        for order in self.get_order_list():
            print(type(order))
            if order.get_order()['id'] == orderId:
                order.set_status('completed')
        
        self.save_data()

    def deliver_order(self, orderId):
        self.load_data()
        for order in self.get_order_list():
            print(type(order))
            if order.get_order()['id'] == orderId:
                order.set_status('delivered')
        
        self.save_data()
    
    # Necessary getters of list.
    # "Normal" getters (ex. get_order_list) return the list as a list of orders
    # Getters "_json" (ex. get_order_list_json) return the list as a list of dictionaries
    def get_order_list(self):
        self.load_data()
        orderListDict=[order for order in self.orderList]
        return orderListDict

    def get_order_list_json(self):
        self.load_data()
        orderListDict=[order.get_order() for order in self.orderList]
        return orderListDict

    def get_pending_order_list_json(self):
        self.load_data()
        orderListDict=[]
        for order in self.orderList:
            if order.get_order()['status']=='pending':
                orderListDict.append(order.get_order())

        return orderListDict

    def get_cancelled_order_list_json(self):
        self.load_data()
        orderListDict=[]
        for order in self.orderList:
            if order.get_order()['status']=='cancelled':
                orderListDict.append(order.get_order())
                
        return orderListDict

    def get_processing_order_list_json(self):
        self.load_data()
        orderListDict=[]
        for order in self.orderList:
            if order.get_order()['status']=='processing':
                orderListDict.append(order.get_order())
                
        return orderListDict

    def get_completed_order_list_json(self):
        self.load_data()
        orderListDict=[]
        for order in self.orderList:
            if order.get_order()['status']=='completed':
                orderListDict.append(order.get_order())
                
        return orderListDict

    def get_delivered_order_list_json(self):
        self.load_data()
        orderListDict=[]
        for order in self.orderList:
            if order.get_order()['status']=='delivered':
                orderListDict.append(order.get_order())
                
        return orderListDict