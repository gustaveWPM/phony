import pymongo
from config import DB_CONFIG as DB_CONF

MONGO_CLIENT = pymongo.MongoClient(DB_CONF["MONGO_DB_CONNECTION_ROUTE"])
DB = MONGO_CLIENT["phone_book"]
DB_TABLE = DB["france"]

def _retrieve_last_saved_phone_number_entry():
    try:
        last_saved_phone_number_entry = DB_TABLE.find_one(sort=[( "_id", pymongo.DESCENDING )])
        return last_saved_phone_number_entry
    except:
        return None

def _retrieve_last_saved_phone_operator_code(entry) -> str:
    data = entry["operator_code"]
    return data

def _retrieve_last_saved_phone_country_code(entry) -> str:
    data = entry["country_code"]
    return data

def _retrieve_last_saved_phone_number_suffix(entry) -> str:
    data = entry["generated_suffix"]
    return data

def retrieve_last_saved_phone_metadatas():
    entry = _retrieve_last_saved_phone_number_entry()
    if (entry is None):
        return None
    metadatas = {}
    metadatas["phone_number_suffix"] = _retrieve_last_saved_phone_number_suffix(entry)
    metadatas["phone_number_country_code"] = _retrieve_last_saved_phone_country_code(entry)
    metadatas["phone_number_operator_code"] = _retrieve_last_saved_phone_operator_code(entry)
    return metadatas
