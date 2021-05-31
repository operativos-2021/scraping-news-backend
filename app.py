from flask import Flask, request
import socket
from flask_restful import Api, Resource, reqparse, abort
import sys
from controllers.news import news
from controllers.clasificator import clasificator


app = Flask(__name__)

api = Api(app)

api.add_resource(news,"/news/<int:quantity>")
api.add_resource(clasificator,"/clasificator")

if __name__ == "__main__":
        app. run(debug=False,port=int("5000"),host='0.0.0.0') #app.run(debug=False)