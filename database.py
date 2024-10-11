from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv("./config/.env")

DATABASE_URI = os.getenv('DATABASE_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')

class Database:
    def __init__(self):
      self.client = MongoClient(DATABASE_URI)
      self.database = self.client[DATABASE_NAME]
        
    def getCollection(self, name):
        return self.database[name]
