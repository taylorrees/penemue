from pymongo import MongoClient

# database connection wrapper
db = MongoClient("mongodb://localhost:27017")["media-monitor"]
