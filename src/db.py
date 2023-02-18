import pymongo
from config import DB_CONFIG as DB_CONF

MONGO_CLIENT = pymongo.MongoClient(DB_CONF["MONGO_DB_CONNECTION_URI"])

DB_NAME_KEY = DB_CONF["MONGO_DB_NAME"]
DB_TABLE_KEY = DB_CONF["MONGO_DB_TABLE"]

DB = MONGO_CLIENT[DB_NAME_KEY]
DB_TABLE = DB[DB_TABLE_KEY]

def _retrieve_last_saved_phone_number_entry():
    try:
        last_saved_phone_number_entry = DB_TABLE.find_one(sort=[( "_id", pymongo.DESCENDING )])
        return last_saved_phone_number_entry
    except:
        return None

def _retrieve_last_saved_phone_operator_code(entry: dict) -> str:
    data = entry["operator_code"]
    return data

def _retrieve_last_saved_phone_country_code(entry: dict) -> str:
    data = entry["country_code"]
    return data

def _retrieve_last_saved_phone_number_suffix(entry: dict) -> str:
    data = entry["generated_suffix"]
    return data


def save_phone_number(phone_number: str, country_code: str, operator_code: str, phone_number_suffix: str):
    database_entry = {
        "phone_number": phone_number,
        "country_code": country_code,
        "operator_code": operator_code,
        "generated_suffix": phone_number_suffix
    }

    DB_TABLE.update_one({"phone_number": phone_number}, {"$set": database_entry}, upsert=True)

def retrieve_last_saved_phone_metadatas():
    entry = _retrieve_last_saved_phone_number_entry()
    if (entry is None):
        return None
    metadatas = {}
    metadatas["phone_number_suffix"] = _retrieve_last_saved_phone_number_suffix(entry)
    metadatas["phone_number_country_code"] = _retrieve_last_saved_phone_country_code(entry)
    metadatas["phone_number_operator_code"] = _retrieve_last_saved_phone_operator_code(entry)
    return metadatas
