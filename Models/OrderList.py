import os
from Models.Inventory import Inventory

from Models.Order import Order

import json

class OrderList:
    orderList=[]

    def __init__(self):

        cwd = os.getcwd()
        self.path=cwd+"\data\orderList.txt"

        self.load_data()

    def load_data(self):
        self.orderList=[]
        
        if os.path.exists(self.path):
            with open(self.path, 'r') as orderFile:
                orderFile.seek(0)
                orderListRaw=orderFile.readlines()
                print("---loadData1---->",orderFile.readlines())

            if len(orderListRaw) != 0:
                for productJSON in orderListRaw:
                    self.orderList.append(Order(json.loads(productJSON)))
                    print('---loadData-->',type(Order(json.loads(productJSON))))


        else:
            print("Order List file not found, creating new one...")
            file=open(self.path, 'w')
            file.close()
            print("Order List file created sucessfully")

    def save_data(self):
        
        print("----saveData-->", self.orderList)

        try:
            with open(self.path, 'w') as orderListFile:

                for order in self.orderList:
                    
                    orderListFile.write(order.__str__())
                    orderListFile.write('\n')

        except FileNotFoundError:
            raise FileNotFoundError("Inventory file not found, can't save")

    def add_order(self, order):
        self.load_data()
        print("---addOrder--->",(order))
        inventory=Inventory()

        alert = "0"

        for productInInventory in inventory.get_inventory_products_nojson():
            if productInInventory.get_product_dict()['sku'] in order.get_order()['productsSKUS']:
                stock=productInInventory.substract()
                inventory.save_data()
                if stock < 3:
                    alert="Stock in 2 Units, consider to provide"


        self.orderList.append(order)
        self.save_data()
        return order,alert
        

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