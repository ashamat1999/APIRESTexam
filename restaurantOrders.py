from flask import Flask
from flask import abort, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hola():
    return "Hola mundo"

