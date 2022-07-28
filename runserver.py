"""
This script runs the application using a development server.
"""
# -*- coding: utf-8 -*-
from os import environ
import restaurantOrders

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '9090'))
    except ValueError:
        PORT = 9090
    restaurantOrders.app.run(HOST, PORT, debug = True) # Establecer en 'False' al trabajar en producción
