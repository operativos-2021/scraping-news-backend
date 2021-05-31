from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import multiprocessing
import os
import json
from scraping.scraper import doScraping
from clasificator.clasificator import classifyNews

actual_path = os.path.dirname(os.path.abspath(__file__))
news_path = actual_path + "/news_list.json"

final_data = {}
class news(Resource):
    def get(self, quantity):
        # doScraping()
        print("getting info")
        news = classifyNews()
        return {"data":news}


