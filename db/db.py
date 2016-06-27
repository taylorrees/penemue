from pymongo import MongoClient

# database connection wrapper
DB = MongoClient("mongodb://localhost:27017")["media-monitor"]
