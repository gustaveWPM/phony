# coding: utf-8

from generator.metaprog.types import Void
from generator.config.rules.dev.database import DB as DATABASE_CONFIG
import pymongo
from typing import Optional

DISABLE_PERSISTENCE = DATABASE_CONFIG["DISABLE_PERSISTENCE"]

MONGO_CLIENT = pymongo.MongoClient(DATABASE_CONFIG["MONGO_DB_CONNECTION_URI"])

DB_NAME_KEY = DATABASE_CONFIG["MONGO_DB_NAME"]
DB_TABLE_KEY = DATABASE_CONFIG["MONGO_DB_TABLE"]

DB = MONGO_CLIENT[DB_NAME_KEY]
DB_TABLE = DB[DB_TABLE_KEY]


def _retrieve_last_saved_phone_number_entry() -> Optional[dict]:
    try:
        last_saved_phone_number_entry: dict = DB_TABLE.find_one(
            sort=[("_id", pymongo.DESCENDING)])
        return last_saved_phone_number_entry
    except:
        return None


def _retrieve_last_saved_phone_operator_code(entry: dict) -> str:
    data: str = entry["operator_code"]
    return data


def _retrieve_last_saved_phone_country_code(entry: dict) -> str:
    data: str = entry["country_code"]
    return data


def _retrieve_last_saved_phone_number_suffix(entry: dict) -> str:
    data: str = entry["generated_suffix"]
    return data


def save_phone_number(phone_number: str, country_code: str, operator_code: str, phone_number_suffix: str) -> Void:
    if DISABLE_PERSISTENCE:
        return
    database_entry: dict = {
        "phone_number": phone_number,
        "country_code": country_code,
        "operator_code": operator_code,
        "generated_suffix": phone_number_suffix
    }

    DB_TABLE.update_one({"phone_number": phone_number}, {
                        "$set": database_entry}, upsert=True)


def retrieve_last_saved_phone_metadatas() -> Optional[dict]:
    if DISABLE_PERSISTENCE:
        return None
    entry: Optional[dict] = _retrieve_last_saved_phone_number_entry()
    if entry is None:
        return None
    metadatas: dict = {}
    metadatas["phone_number_suffix"] = _retrieve_last_saved_phone_number_suffix(
        entry)
    metadatas["phone_number_country_code"] = _retrieve_last_saved_phone_country_code(
        entry)
    metadatas["phone_number_operator_code"] = _retrieve_last_saved_phone_operator_code(
        entry)
    return metadatas


def append_finite_collection_indicator() -> Void:
    save_phone_number("-1", "-1", "-1", "-1")


def is_finite_collection(data: dict) -> bool:
    for key in data:
        if data[key] != "-1":
            return False
    return True
