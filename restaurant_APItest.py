import os

from flask import Flask
from flask import jsonify,redirect, render_template, request, url_for

from Models.Inventory import Inventory
from Models.OrderList import OrderList
from Models.Product import Product
from Models.Order import Order

app = Flask(__name__)

# Endpoint to home, in this case redirect to pending_orders
@app.route('/', methods=['GET'])
def home():

    return redirect(url_for('pending_orders'))

# Endpoint to get inventory or products list
@app.route('/products', methods=['GET'])
def get_products():
    inventory=Inventory()
    return jsonify(inventory.get_inventory_products())

# Endpoint to get a specific product from inventory
@app.route('/products/<string:sku>' , methods=['GET'])
def get_product(sku):
    inventory=Inventory()
    product=[product for product in inventory.inventoryProducts if product.get_product_dict()['sku']==sku]
    return jsonify(product[0].get_product_dict())

# Endpoint to post a product into inventory through json request
@app.route('/products', methods=['POST'])
def add_products():
    inventory=Inventory()
    product={
        "sku" : request.json["sku"],
        "name" : request.json["name"],
        "stock" : request.json["stock"],
        "price" : request.json["price"]
    }

    added=inventory.add_product(Product(product))
    if added: # Get if the product was added, in case no it is because it has duplicated SKU
        return jsonify({"message":"Product added succesfully", "list":inventory.get_inventory_products()})
    else:
        return jsonify({"message":"SKU already added, cannot save data."})

# Endpoint to update a product into inventory through json request
@app.route('/products/<string:sku>', methods=['PUT'])
def update_product(sku):
    inventory=Inventory()
    product={
        "sku" : request.json["sku"],
        "name" : request.json["name"],
        "stock" : request.json["stock"],
        "price" : request.json["price"]
    }

    updated=inventory.update_product(sku,product)
    if updated:
        return jsonify({"message" : "Product updated sucessfully", 
                        "list":inventory.get_inventory_products()})
    else:
        return jsonify({"message" : "Error. Product cannot be updated."})

# Endpoint to delete a product by its sku
@app.route('/products/<string:sku>' , methods=['DELETE'])
def delete_product(sku):
    inventory=Inventory()
    inventory.delete_product(sku)
    return jsonify({"message" : "Product deleted sucessfully"})

# Endpoint to get all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orderList=OrderList()
    return jsonify(orderList.get_order_list_json())

# Endpoint to create orders through json
@app.route('/orders' , methods=['POST'])
def create_orders():

    orderList=OrderList()
    if len(orderList.get_order_list())>0:
        last=orderList.get_order_list()[-1]
        lastId=last.get_order()['id']
        newId=(int(lastId)+1)
    else:
        newId=0
    order={
        "id" : newId,
        "table" : request.json["table"],
        "productsSKUS" : request.json["productsSKUS"],
        "status" : "pending"
    }
    orderO,alert=orderList.add_order(Order(order))
    return jsonify({"message" : "Order created sucessfully", "order": orderO.get_order(), "alert" : alert})

# Endpoint to get and post pending orders, if post then the order change to processing
@app.route('/orders/pending', methods=['GET','POST'])
def pending_orders():
    if request.method == 'GET': 
        orderList=OrderList()
        return render_template("/orders_menu/pendingOrders.html", data = orderList.get_pending_order_list_json())

    elif(request.method == 'POST'):
        if request.form["submit_btn"] == "Start order":
            orderId = request.form.get('pressed')
            orderList=OrderList()
            orderList.begin_order(orderId)
            return render_template("/orders_menu/pendingOrders.html", data = orderList.get_pending_order_list_json())
            
        elif request.form["submit_btn"] == "Cancel order":
            orderId = request.form.get('pressed')
            orderList=OrderList()
            orderList.cancel_order(orderId)
            return render_template("/orders_menu/pendingOrders.html", data = orderList.get_pending_order_list_json())

# Endpoint to get cancelled orders
@app.route('/orders/cancelled', methods=['GET'])
def cancelled_orders():
    if request.method == 'GET':
        orderList=OrderList()
        return render_template("/orders_menu/cancelledOrders.html", data = orderList.get_cancelled_order_list_json())

# Endpoint to get and post processing orders, if post then the order change to completed
@app.route('/orders/processing', methods=['GET','POST'])
def processing_orders():
    if request.method == 'GET':
        orderList=OrderList()
        print(orderList.get_order_list())
        return render_template("/orders_menu/processingOrders.html", data = orderList.get_processing_order_list_json())

    elif(request.method == 'POST'):
        if request.form["submit_btn"] == "Complete order":
            orderId = request.form.get('pressed')
            orderList=OrderList()
            orderList.complete_order(orderId)
            return render_template("/orders_menu/processingOrders.html", data = orderList.get_processing_order_list_json())
            
        elif request.form["submit_btn"] == "Cancel order":
            orderId = request.form.get('pressed')
            orderList=OrderList()
            orderList.cancel_order(orderId)
            return render_template("/orders_menu/processingOrders.html", data = orderList.get_processing_order_list_json())

# Endpoint to get and post completed orders, if post then the order change to delivered
@app.route('/orders/completed', methods=['GET','POST'])
def completed_orders():
    if request.method == 'GET':
        orderList=OrderList()
        print(orderList.get_order_list())
        return render_template("/orders_menu/completedOrders.html", data = orderList.get_completed_order_list_json())

    elif(request.method == 'POST'):
        if request.form["submit_btn"] == "Deliver order":
            orderId = request.form.get('pressed')
            orderList=OrderList()
            orderList.deliver_order(orderId)
            return render_template("/orders_menu/completedOrders.html", data = orderList.get_completed_order_list_json())
            
        elif request.form["submit_btn"] == "Cancel order":
            orderId = request.form.get('pressed')
            orderList=OrderList()
            orderList.deliver_order(orderId)
            return render_template("/orders_menu/completedOrders.html", data = orderList.get_completed_order_list_json())

# Endpoint to get delivered orders
@app.route('/orders/delivered', methods=['GET'])
def delivered_orders():
    if request.method == 'GET':
        orderList=OrderList()
        print(orderList.get_order_list())
        return render_template("/orders_menu/deliveredOrders.html", data = orderList.get_delivered_order_list_json())
