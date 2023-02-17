import pymongo
from config import DB_CONFIG as DB_CONF

MONGO_CLIENT = pymongo.MongoClient(DB_CONF["MONGO_DB_CONNECTION_ROUTE"])
DB = MONGO_CLIENT["phone_book"]
DB_TABLE = DB["france"]
