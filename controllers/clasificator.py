from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import os
from clasificator.clasificator import initClassifier

actual_path = os.path.dirname(os.path.abspath(__file__))
news_path = actual_path + "/news_list.json"

final_data = {}
class clasificator(Resource):
    def post(self):
        initClassifier()
        print("getting info")
        return 'success',201
